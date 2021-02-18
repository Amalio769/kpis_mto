# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:02:54 2021

@author: c48142
"""

import kpis.sap as sap
import kpis.informes.costes.preparacion_datos as datos
import kpis.configuracion.config as cfg
import datetime
import pandas as pd

year = 2021

hr301 = 82.19
hr211 = 70.00
hr215 = 72.25

#sap.me2k.me2k_year(year)
#sap.zps_capp.zps_capp_year(year)


df=datos.combinar_pep_ceco_orden(year)
df=df.drop_duplicates()
#df['coste_total']=df['coste_total'].div(1000).round(2)
#df['coste_por_entregar']=df['coste_por_entregar'].div(1000).round(2)
#df['coste_por_facturar']=df['coste_por_facturar'].div(1000).round(2)
df=df.fillna(' ')
df=df[['ceco', 'centro', 'cl_po', 'coste_por_entregar','coste_por_facturar',
       'coste_total','descripcion_material', 'elemento_pep','fecha_pedido',
       'grupo_articulo', 'imputacion', 'material', 'mes','nombre_proveedor',
       'orden', 'pedido', 'posicion_po']]
df['pedido_pos']= df['pedido']+"-"+ df['posicion_po'].str.lstrip('0')
df['clase_coste']="PO"
df = df.drop('posicion_po', axis=1)
df.rename(columns={'elemento_pep':'pep'}, inplace=True)
df.rename(columns={'coste_total':'coste'}, inplace=True)
df.rename(columns={'cl_po':'po_grafo'}, inplace=True)
df.rename(columns={'fecha_pedido':'fecha'}, inplace=True)

for idx in range(1,13):
    linea_dummy = {'ceco':'', 'centro':'', 'po_grafo':'', 'coste_por_entregar':0,
       'coste_por_facturar':0, 'coste':0, 'descripcion_material':'', 'pep':'', 'fecha':'',
       'grupo_articulo':'', 'imputacion':'', 'material':'', 'mes':idx, 'nombre_proveedor':'',
       'orden':'', 'pedido':'', 'pedido_pos':'', 'clase_coste':''}
    df = df.append(linea_dummy, ignore_index=True)


#datos.df_pco2excel_app(df,year)
#datos.df_pco2excel_kpisites(df,year)

df1=datos.procesar_allzpscapp2df(year)
df1['mes']= pd.DatetimeIndex(df1['fecha']).month
df1['coste']=df1[['ceco','horas']].apply(lambda x: x['horas']*hr301 if x['ceco']==13301410 else (x['horas']*hr211 if x['ceco']==13211410 else (x['horas']*hr215 if x['ceco']==13215410 else x['horas']*0)),axis=1).round(2)
df1['clase_coste']="GRAFO"
df1.rename(columns={'grafo':'po_grafo'}, inplace=True)


df_total=pd.merge(df,df1, how='outer', on=['pep','clase_coste','po_grafo','coste','ceco','mes','fecha'])
df_total.reset_index(drop = True, inplace = True)

df_total_1 = df_total[['pep','ceco','clase_coste','po_grafo','mes','coste']]
#df_total_1['coste'] = df_total_1['coste'].div(1000).round(2)
df_total_1_gby = df_total_1.groupby(['pep','ceco','clase_coste','po_grafo','mes'], as_index=False).sum()
pivot_total1=pd.pivot_table(df_total_1_gby,\
                            index=['pep','ceco','clase_coste','po_grafo'],\
                            columns='mes',\
                            values='coste',\
                            aggfunc=sum,\
                            margins=False)

with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year) + '.xlsx') as output:
    df_total.to_excel(output, sheet_name='total', index= False)
    df_total_1.to_excel(output, sheet_name='total_1', index=False)
    df_total_1_gby.to_excel(output, sheet_name='gby', index=False)
    pivot_total1.to_excel(output, sheet_name='pivot', index=True)

#datos.df_zpscapp2excel_app(df,year)
#datos.df_zpscapp2excel_kpisites(df,year)


