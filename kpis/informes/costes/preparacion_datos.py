# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 08:29:20 2020

@author: C48142
"""
import os, sys
import pandas as pd
import datetime
import kpis.configuracion.config as cfg


#------------------------------------------------------------------------------
def zpscapptxt2csv(path_file_name):
    """ Convierte archivo de incurridos txt en csv, eliminando cabecera, pie y 
    
    blancos.
    Hay que tener en cuenta que el metodo de extraer ficheros planos de  SAP
    no asegura que los encabezados sean siempre los mismos y las columnas
    tengan el mismo ancho. Por ese motivo en el proceso de esta función 
    cambiamos la cabecera de los titulos por uno predefinido en el fichero de 
    configuracion. Esta función tambien cambia el formato de los numeros, 
    eliminando el '.' de los millares y cambiando la ',' de los decimales por 
    el '.'
    Parametros:
      path_file_name :  (string) Directorio donde se ubican los ficheros txt
    """
    output = []
    modificacion = []
    
    if os.path.isfile(path_file_name):
        with open(path_file_name) as f:
            for linea in f:
                # Solo las lineas que empiezan por '|  ' son procesadas
                if linea[0:3] == '|  ':
                    # Si la linea es la correspondiente a la cabecera
                    # la sustituye por la predefinida en cfg.
                    if linea.find('CeCo emis.') != -1:
                        linea = cfg.CABECERA_TXT_GRAFOS
                    # Divide la linea, usando como division el simbolo '|'
                    lst_temp=linea.split('|')
                    # Elimina los espacios en blanco
                    for columna in lst_temp:
                        modificacion.append(columna.lstrip().rstrip())
                    # Cuando no es cabecera corrige el formato de los numeros
                    # de la columna 'horas'
                    if linea.find('CeCo emis.') == -1:
                        modificacion[8]=modificacion[8].replace('.','').replace(',','.')
                    # Recompone en un string usando como separador '|'
                    linea = "|".join(modificacion)
                    modificacion=[]
                    output.append(linea.lstrip('|').rstrip().rstrip('|')+'\n')
        if len(output) != 0:
            f=open(path_file_name.replace('.txt','.csv'), "w")
            f.writelines(output)
            f.close()
    else:
        sys.exit("Error. No se puede abrir el fichero " + path_file_name)
#------------------------------------------------------------------------------
def zpscappcsv2df(path_file_name):
    """ Procesa un archivo de grafo y lo convierte en DataFrame
    
    Detallar la funcion....
    """
    if os.path.isfile(path_file_name):
        df=pd.read_csv(path_file_name, sep='|', index_col= None, encoding = 'latin-1')
    else:
        sys.exit("Error. No se puede abrir el fichero " + path_file_name)
    return df
#------------------------------------------------------------------------------
def procesar_allzpscapp2df(year):        
    """ Procesa todos los ficheros de grafos y obtiene un dataframe
    
    Detallar la funcion....
    """
    import kpis.configuracion.gestion_archivos as files
    
    path = cfg.PATH_COSTES_GRAFOS
    # Borra los archivos '.csv' previos
    files.delete_list_ficheros(path,year,'.csv')
    df = pd.DataFrame()      
    contenido=files.list_ficheros(path,year,'.txt')  
    for file_name in contenido:
        zpscapptxt2csv(path + file_name)
        temp_df=zpscappcsv2df(path + file_name.replace('.txt','.csv'))
        df=pd.concat([df,temp_df])
#    for columna in df.columns:
#        df=df.rename(columns={columna : cfg.NOMBRE_COLUMNAS_ZPM_HTO[columna]})
    columnas = list(df.columns)
    for columna in columnas:
        if columna.startswith('fecha'):
            df[columna]=pd.to_datetime(df[columna], format='%d.%m.%Y')
    return df
#------------------------------------------------------------------------------
def df_zpscapp2excel_app(df,year):
    """ Convierte el dataframe en un fichero excel en el directorio de la APP
    
    Detallar función
    """
    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT+'Datos-Grafos-'+ str(year) +\
                        '.xlsx') as output:
        df.to_excel(output, sheet_name='total grafos')
#------------------------------------------------------------------------------
def df_zpscapp2excel_kpisites(df,year):
    """ Convierte el dataframe en un fichero excel en el directorio de Drive
    
    Detallar función
    """
    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT_KPISITES + 'OP' + str(year)+\
                '/Datos-Grafos-'+ str(year) + '.xlsx') as output:
        df.to_excel(output, sheet_name='total grafos')
#------------------------------------------------------------------------------
def me2ktxt2df(path_file_name,tipo_me2k,year):
    """ Procesa archivo txt del PEP en un DataFrame
    
    Explicar.......
    """

    if tipo_me2k not in['pep','ceco','orden']:
        sys.exit("Error. Hay que elegir al menos un parámetro entre ceco, "+ \
               "pep y orden")
    # Creación del DataFrame con los datos de los pedidos asociados al PEP.
    # También se han incluido los columnas de 'ceco' y 'orden' (aunque se vayan
    # a quedar en blanco) para que el Dataframe tenga la misma estructura que
    # los datafraqmes del ceco y orden.
    col_names = ['pedido',\
                 'cl_po',\
                 'proveedor',\
                 'nombre_proveedor',\
                 'ogc',\
                 'fecha_pedido',\
                 'posicion_po',\
                 'material',\
                 'descripcion_material',\
                 'grupo_articulo',\
                 'imputacion',\
                 'centro',\
                 'almacen',\
                 'ctd_pedido',\
                 'und_ctd_pedido',\
                 'precio_neto_por',\
                 'moneda_precio_neto_por',\
                 'ctd_precio_neto_por',\
                 'und_ctd_precio_neto_por',\
                 'ctd_medida_almacen',\
                 'und_ctd_medida_almacen',\
                 'precio_neto_por_medida_almacen',\
                 'moneda_precio_neto_por_medida_almacen',\
                 'ctd_precio_por_medida_almacen',\
                 'und_ctd_precio_por_medida_almacen',\
                 'elemento_pep',\
                 'ceco',\
                 'orden',\
                 'ctd_por_entregar',\
                 'und_ctd_por_entregar',\
                 'coste_por_entregar',\
                 'moneda_coste_por_entregar',\
                 'porcentaje_por_entregar',\
                 'ctd_por_facturar',\
                 'und_ctd_por_facturar',\
                 'coste_por_facturar',\
                 'moneda_coste_por_facturar',\
                 'porcentaje_por_facturar',\
                 'mes',\
                 'coste_total']
    
    datos = []
    if tipo_me2k == 'pep':
        _ceco=""
        _orden=""
    if tipo_me2k == 'ceco':
        _elemento_pep=""
        _orden=""
    if tipo_me2k == 'orden':
        _ceco=""
        _elemento_pep=""
    # Las siguientes variables se inicializan ya que la línea de almacén no 
    # aparece en todas las iteraciones.
    _ctd_medida_almacen = ""
    _und_ctd_medida_almacen = ""
    _precio_neto_por_medida_almacen = ""
    _moneda_precio_neto_por_medida_almacen = ""
    _ctd_precio_por_medida_almacen = ""
    _und_ctd_precio_por_medida_almacen = ""
    
    if os.path.isfile(path_file_name):
        with open(path_file_name) as f:
            for linea in f:
                if linea[0]=='|' and linea[1]!=' ' and linea[7]!=' ':
                    _pedido = str(linea[1:11].strip())
                    _cl_po = linea[12:16].strip()
                    _proveedor = linea[17:27].strip()
                    _nombre_proveedor = linea[28:64].strip()
                    _ogc = linea[65:68].strip()
                    _fecha_pedido = datetime.datetime.strptime(linea[69:80].strip(),"%d.%m.%Y")
                    if _fecha_pedido < datetime.datetime.strptime('01.01.'+str(year),"%d.%m.%Y"):
                        _fecha_pedido = datetime.datetime.strptime('01.01.'+str(year),"%d.%m.%Y")
                    _mes = _fecha_pedido.month
                if linea[0:5]=='|  00':
                    _posicion_po = linea[3:8].strip()
                    _material = linea[9:20].strip()
                    _descripcion_material = linea[63:103].strip()
                    _grupo_articulo = linea[104:114].strip()
                if linea[9:13] == '2013':
                    _imputacion = linea[6:8].strip()
                    _centro = linea[9:13].strip()
                    _almacen = linea[14:31].strip()
                    _ctd_pedido = round(float(linea[32:43].strip().replace('.','').replace(',','.')),2)
                    _und_ctd_pedido = linea[45:48].strip()
                    _precio_neto_por = round(float(linea[49:63].strip().replace('.','').replace(',','.')),2)
                    _moneda_precio_neto_por = linea[65:68].strip()
                    _ctd_precio_neto_por = int(linea[69:76].strip().replace('.','').replace(',','.'))
                    _und_ctd_precio_neto_por = linea[77:80].strip()
                if linea[0:27] == '|     en unidad medida alm.':
                    _ctd_medida_almacen = int(float(linea[32:43].strip().replace('.','').replace(',','.')))
                    _und_ctd_medida_almacen = linea[45:48].strip()
                    _precio_neto_por_medida_almacen = round(float(linea[49:63].strip().replace('.','').replace(',','.')),2)
                    _moneda_precio_neto_por_medida_almacen = linea[65:68].strip()
                    _ctd_precio_por_medida_almacen = round(float(linea[69:76].strip().replace('.','').replace(',','.')),2)
                    _und_ctd_precio_por_medida_almacen = linea[77:80].strip()
                if linea[0:18] == '|     Elemento PEP':
                    _elemento_pep = linea[19:114].strip()
                if linea[0:11] == '|     Orden':
                    _orden = linea[14:31].strip()
                if linea[0:21] == '|     Centro de coste':
                    _ceco = linea[22:31].strip()
                if linea[0:18] == '|     por entregar':
                    _ctd_por_entregar = round(float(linea[20:43].strip().replace('.','').replace(',','.')),2)
                    _und_ctd_por_entregar = linea[45:48].strip()
                    _coste_por_entregar = round(float(linea[49:63].strip().replace('.','').replace(',','.')),2)
                    _moneda_coste_por_entregar = linea[65:68].strip()
                    _porcentaje_por_entregar = round(float(linea[69:77].strip().replace('.','').replace(',','.')),2)
                if linea[0:18] == '|     por facturar':    
                    _ctd_por_facturar = round(float(linea[20:43].strip().replace('.','').replace(',','.')),2)
                    _und_ctd_por_facturar = linea[45:48].strip()
                    _coste_por_facturar = round(float(linea[49:63].strip().replace('.','').replace(',','.')),2)
                    _moneda_coste_por_facturar = linea[65:68].strip()
                    _porcentaje_por_facturar = round(float(linea[69:77].strip().replace('.','').replace(',','.')),2)
                    if _und_ctd_pedido == _und_ctd_precio_neto_por:
                        _coste_total = _precio_neto_por / _ctd_precio_neto_por * _ctd_pedido
                    if _und_ctd_pedido != _und_ctd_precio_neto_por and _ctd_medida_almacen != '':
                        _coste_total = _precio_neto_por / _ctd_precio_neto_por * _ctd_medida_almacen
                        
                    datos.append([_pedido,\
                                  _cl_po,\
                                  _proveedor,\
                                  _nombre_proveedor,\
                                  _ogc,\
                                  _fecha_pedido,\
                                  _posicion_po,\
                                  _material,\
                                  _descripcion_material,\
                                  _grupo_articulo,\
                                  _imputacion,\
                                  _centro,\
                                  _almacen,\
                                  _ctd_pedido,\
                                  _und_ctd_pedido,\
                                  _precio_neto_por,\
                                  _moneda_precio_neto_por,\
                                  _ctd_precio_neto_por,\
                                  _und_ctd_precio_neto_por,\
                                  _ctd_medida_almacen,\
                                  _und_ctd_medida_almacen,\
                                  _precio_neto_por_medida_almacen,\
                                  _moneda_precio_neto_por_medida_almacen,\
                                  _ctd_precio_por_medida_almacen,\
                                  _und_ctd_precio_por_medida_almacen,\
                                  _elemento_pep,\
                                  _ceco,\
                                  _orden,\
                                  _ctd_por_entregar,\
                                  _und_ctd_por_entregar,\
                                  _coste_por_entregar,\
                                  _moneda_coste_por_entregar,\
                                  _porcentaje_por_entregar,\
                                  _ctd_por_facturar,\
                                  _und_ctd_por_facturar,\
                                  _coste_por_facturar,\
                                  _moneda_coste_por_facturar,\
                                  _porcentaje_por_facturar,\
                                  _mes,\
                                  _coste_total])
                    
                    # Reinicia las variables para el siguiente ciclo.
                    # Esto es debido a que no siempre existe al linea
                    # |     en unidad medida alm.......
                    _ctd_medida_almacen = ""
                    _und_ctd_medida_almacen = ""
                    _precio_neto_por_medida_almacen = ""
                    _moneda_precio_neto_por_medida_almacen = ""
                    _ctd_precio_por_medida_almacen = ""
                    _und_ctd_precio_por_medida_almacen = ""
                                                    
    datos_df = pd.DataFrame(datos, columns=col_names, index = None)
    return datos_df

#------------------------------------------------------------------------------
def me2ktxt2df_year(year, tipo_me2k):
    """ Iteración de la funcion me2ktxt2df para la configuración costes
    
    Detallar funcionalidad
    """
    import pandas as pd
    import kpis.configuracion.config as cfg
    
    if tipo_me2k not in['pep','ceco','orden']:
        sys.exit("Error. Hay que elegir al menos un parámetro entre ceco, "+ \
               "pep y orden")
    if tipo_me2k == 'pep':
        path = cfg.PATH_COSTES_PEP
        datos_df = pd.DataFrame()
        df_pep = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='pep')
        for row in df_pep.itertuples():
            temp_df = me2ktxt2df(path + str(year) + '-' + \
                                 str(row.pep).replace('/', '-') + \
                                 '.txt', tipo_me2k, year)
            datos_df = pd.concat([datos_df, temp_df])
        return datos_df

    if tipo_me2k == 'ceco':
        path = cfg.PATH_COSTES_CECO
        datos_df = pd.DataFrame()
        #TODO: version Pandas, cambiar parámetro sheet_name
        df_ceco = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', 'ceco')
        for row in df_ceco.itertuples():
            temp_df = me2ktxt2df(path + str(year) + '-' + \
                                 str(row.ceco).replace('/', '-') + \
                                 '.txt', tipo_me2k, year)
            datos_df = pd.concat([datos_df, temp_df])
        return datos_df

    if tipo_me2k == 'orden':
        path = cfg.PATH_COSTES_ORDEN
        datos_df = pd.DataFrame()
        #TODO: version Pandas, cambiar parámetro sheet_name

        df_orden = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', 'orden')
        for row in df_orden.itertuples():
            temp_df = me2ktxt2df(path + str(year) + '-' + \
                                 str(row.orden).replace('/', '-') + \
                                 '.txt', tipo_me2k, year)
            datos_df = pd.concat([datos_df, temp_df])
        return datos_df
    
#------------------------------------------------------------------------------
def combinar_pep_ceco_orden(year):
    """ Combina los dataframes de Pep, Ceco y Orden y devuelve el resultado
    
    Detallar funcionalidad
    """
    import kpis.informes.costes.preparacion_datos as costes
    
    df_pep   = costes.me2ktxt2df_year(year, 'pep')
    df_ceco  = costes.me2ktxt2df_year(year, 'ceco')
    df_orden = costes.me2ktxt2df_year(year, 'orden')
    
    df_pep_ceco = pd.merge(df_pep.drop('ceco',axis=1),\
                           df_ceco[['pedido','posicion_po','ceco']],\
                           how='left',\
                           on = ['pedido',\
                                 'posicion_po'])

    df_pep_ceco_orden = pd.merge(df_pep_ceco.drop('orden',axis=1),\
                                 df_orden[['pedido','posicion_po','orden']],\
                                 how='left',\
                                 on = ['pedido',\
                                       'posicion_po'])
      
    df_orden_ceco = pd.merge(df_orden.drop('ceco',axis=1),\
                             df_ceco[['pedido','posicion_po','ceco']],\
                             how='left',\
                             on = ['pedido',\
                                   'posicion_po'])
      
    df_orden_ceco_pep = pd.merge(df_orden_ceco.drop('elemento_pep',axis=1),\
                                 df_pep[['pedido','posicion_po','elemento_pep']],\
                                 how='left',\
                                 on = ['pedido',\
                                       'posicion_po'])
    df_ocp_pep_nan = df_orden_ceco_pep.loc[df_orden_ceco_pep['elemento_pep'].isnull()]
    df_total = pd.concat([df_pep_ceco_orden, df_ocp_pep_nan])
    

    
    return df_total
#------------------------------------------------------------------------------
def df_pco2excel_app(df,year):
    """ Convierte el dataframe en un fichero excel en el directorio de la APP
    
    Detallar función
    """
    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT+'Datos-PO-'+ str(year) +\
                        '.xlsx') as output:
        df.to_excel(output, sheet_name='total')
#------------------------------------------------------------------------------
def df_pco2excel_kpisites(df,year):
    """ Convierte el dataframe en un fichero excel en el directorio de Drive
    
    Detallar función
    """
    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT_KPISITES + 'OP' + str(year)+\
                        '/Datos-PO-'+ str(year) + '.xlsx') as output:
        df.to_excel(output, sheet_name='total')
#------------------------------------------------------------------------------



