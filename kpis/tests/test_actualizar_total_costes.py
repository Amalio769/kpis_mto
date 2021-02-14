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

year = 2020
dpto = 'ODRM'
hr301 = 82.19
hr211 = 70.00
hr215 = 72.25

#sap.me2k.me2k_year_dpto(year,dpto)
#sap.zps_capp.zps_capp_year_dpto(year,dpto)


df=datos.combinar_pep_ceco_orden(year, dpto)
df=df.drop_duplicates()
df['coste_total']=df['coste_total'].div(1000).round(2)
df['coste_por_entregar']=df['coste_por_entregar'].div(1000).round(2)
df['coste_por_facturar']=df['coste_por_facturar'].div(1000).round(2)
df=df.fillna(' ')

datos.df_pco2excel_app(df,year, dpto)
datos.df_pco2excel_kpisites(df,year, dpto)

df1=datos.procesar_allzpscapp2df(year, dpto)
df1['mes']= pd.DatetimeIndex(df1['fecha']).month
df1['coste']=df1[['ceco','horas']].apply(lambda x: x['horas']*hr301 if x['ceco']==13301410 else (x['horas']*hr211 if x['ceco']==13211410 else x['horas']*hr215),axis=1)

datos.df_zpscapp2excel_app(df,year, dpto)
datos.df_zpscapp2excel_kpisites(df,year, dpto)


df_po_gby=df.groupby(['elemento_pep','ceco','mes'], as_index=False).sum()
with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT+'df_po_gby'+'.xlsx') as output:
        df_po_gby.to_excel(output, sheet_name='df_po_gby')

pivot_pep_ceco=pd.pivot_table(df_po_gby,\
                              index=['elemento_pep','ceco'],\
                              columns='mes',\
                              values='coste_total',\
                              aggfunc=sum,\
                              margins=False)
with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT+'pivot_pep_ceco'+'.xlsx') as output:
        pivot_pep_ceco.to_excel(output, sheet_name='pivot_pep_ceco')

#df_po_gby.groupby(['elemento_pep','ceco'])[('coste_total')].sum()
out=df_po_gby.groupby('elemento_pep').apply(lambda sub: sub.pivot_table(
                              index=['elemento_pep','ceco'],\
                              columns='mes',\
                              values='coste_total',\
                              aggfunc=sum,\
                              margins=True))
out.loc[('','Total','')]=(out.sum())/2
out.index=out.index.droplevel(0)
out.fillna('', inplace=True)
#pivot_pep_ceco['YtD']=pivot_pep_ceco.sum(axis=1)

pivot_pep_ceco=pivot_pep_ceco.fillna(' ')
#html_pep_ceco=pivot_pep_ceco.to_html()
html_pep_ceco=out.to_html()
f=open("Prueba_pep_ceco.html","w")
f.write(html_pep_ceco)
f.close()
