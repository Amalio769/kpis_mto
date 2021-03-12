# -*- coding: utf-8 -*-
"""
Created on 27/02/2021

@author: C48142
"""
def coste_po_grafo_year(year):
    """Calcula el coste total de PO y Grafos para el año indicado

    Ampliar descripcion función.
    """
    import kpis.informes.costes.preparacion_datos as datos
    import kpis.configuracion.config as cfg
    import datetime
    import pandas as pd


    #TODO: Misma actualización de Pandas y cambiar la llamada a la función read_excel (añadir sheet_name)
    # Del fichero excel de configuración de costes lee los valores de tarifa horaria
    # por cada ceco
    df_ceco_grafo = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', 'ceco-grafo')
    for row in df_ceco_grafo.itertuples():
        if row.ceco_grafo == 13301410:
            hr301 = row.hr
        if row.ceco_grafo == 13211410:
            hr211 = row.hr
        if row.ceco_grafo == 13215410:
            hr215 = row.hr
    # Del fichero excel de configuración de costes lee los valores de los pep con sus
    # descripciones
    df_pep = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', 'pep')

    # Del fichero excel de configuración de costes lee los valores de las propuestas de
    # gastos con sus descripciones
    df_orden = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', 'orden')

    df = datos.combinar_pep_ceco_orden(year)
    df = df.drop_duplicates()
    df = df.fillna(' ')
    #df = df[['ceco', 'centro', 'cl_po', 'coste_por_entregar','coste_por_facturar',
           #'coste_total', 'descripcion_material', 'elemento_pep', 'fecha_pedido',
           #'grupo_articulo', 'imputacion', 'material', 'mes', 'nombre_proveedor',
           #'orden', 'pedido', 'posicion_po']]
    df['pedido_pos'] = df['pedido'] + "-" + df['posicion_po'].str.lstrip('0')
    df['clase_coste'] = "PO"
    df = df.drop('posicion_po', axis=1)
    df.rename(columns={'elemento_pep':'pep'}, inplace=True)
    df.rename(columns={'coste_total':'coste'}, inplace=True)
    df.rename(columns={'cl_po':'po_grafo'}, inplace=True)
    df.rename(columns={'fecha_pedido' : 'fecha'}, inplace=True)

    # Añade datos dummy para los 12 meses, para que cuando se realice un pivot table
    # aparezcan las 12 columnas de mes.
    #for idx in range(1,13):
    #    linea_dummy = {'ceco':'', 'centro':'', 'po_grafo':'', 'coste_por_entregar':0,
    #       'coste_por_facturar':0, 'coste':0, 'descripcion_material':'', 'pep':'',
    #       'fecha' : datetime.datetime.strptime("01/" + str(idx) + "/" + str(year), "%d/%m/%Y"),
    #       'grupo_articulo':'', 'imputacion':'', 'material':'', 'mes':idx, 'nombre_proveedor':'',
    #       'orden':'', 'pedido':'', 'pedido_pos':'', 'clase_coste':''}
    #    df = df.append(linea_dummy, ignore_index=True)


    df1=datos.procesar_allzpscapp2df(year)
    df1['mes']= pd.DatetimeIndex(df1['fecha']).month
    df1['coste']=df1[['ceco','horas']].apply(lambda x: x['horas']*hr301 if x['ceco']==13301410 else (x['horas']*hr211 if x['ceco']==13211410 else (x['horas']*hr215 if x['ceco']==13215410 else x['horas']*0)),axis=1).round(2)
    df1['clase_coste']="GRAFO"
    df1.rename(columns={'grafo':'po_grafo'}, inplace=True)
    df1['po_grafo'] = round(df1['po_grafo'], 0)
    df1['po_grafo'] = df1['po_grafo'].astype(str)
    #TODO: regex=False no soportado en version Pandas 0.19, nuevo desde version 0.23.0
    df1['po_grafo'] = df1['po_grafo'].str.replace('.0', '')
    df1['ceco'] = df1['ceco'].astype(str)


    df_total=pd.merge(df,df1, how='outer', on=['pep','clase_coste','po_grafo','coste','ceco','mes','fecha'])
    df_total.reset_index(drop = True, inplace = True)
    df_total = pd.merge(df_total, df_pep, how='left', on='pep')
    df_total = pd.merge(df_total, df_orden, how='left', on='orden')


    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year) + '.xlsx') as output:
        df_total.to_excel(output, sheet_name='total', index= False)
#-----------------------------------------------------------------------------------------------------------------------