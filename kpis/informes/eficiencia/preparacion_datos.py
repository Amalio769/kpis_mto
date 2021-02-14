# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 14:51:30 2021

@author: C48142
"""

import os, sys
import pandas as pd
import kpis.configuracion.config as cfg

#------------------------------------------------------------------------------
def hotcsv2df(path_file_name):
    """ Procesa los archivos de Historicos Ot para convertirlos en DataFrame
    
    Detallar la funcion....
    """
    if os.path.isfile(path_file_name):
        df=pd.read_csv(path_file_name, sep='|', index_col= None, encoding = 'latin-1')
    else:
        sys.exit("Error. No se puede abrir el fichero " + path_file_name)
    return df
#------------------------------------------------------------------------------
def hottxt2csv(path_file_name):
    """ Convierte archivo de hot txt en csv, eliminando cabecera, pie y blancos

    Hay que tener en cuenta que el metodo de extraer ficheros planos de  SAP
    no asegura que los encabezados sean siempre los mismos. Por ese motivo
    en el proceso de esta función cambiamos la cabecera de los titulos por uno
    predefinido en el fichero de configuracion. Esta función tambien cambia el
    formato de los numeros, eliminando el '.' de los millares y cambiando la
    ',' de los decimales por el '.'
    Parametros:
      path_file_name :  (string) Directorio donde se ubican los ficheros txt de
                        historicos de OT
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
                    if linea[0:6] == '|  Cl.':
                        linea = cfg.CABECERA_TXT_HOT
                    # Divide la linea, usando como division el simbolo '|'
                    lst_temp=linea.split('|')
                    # Elimina los espacios en blanco
                    for columna in lst_temp:
                        modificacion.append(columna.lstrip().rstrip())
                    # Cuando no es cabecera corrige el formato de los numeros
                    if linea[0:6] != '|  Cl.':
                        for x in range(15,24):
                            modificacion[x]=modificacion[x].replace('.','').replace(',','.')
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
def hotborrarcsvs(path):
    """ Borrar archivos csv antes de comenzar la preparacion
    
    Detallar función.
    """
    contenido=os.listdir(path)  
    for file_name in contenido:
        if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
            os.remove(path + file_name)
        
#------------------------------------------------------------------------------
def procesar_allhto2df():        
    """ Procesa todos los ficheros de hto y obtiene un dataframe
    
    Detallar la funcion....
    """
    path = cfg.PATH_EFICIENCIA_HOT
    hotborrarcsvs(path)
    df = pd.DataFrame()      
    contenido=os.listdir(path)  
    for file_name in contenido:
        hottxt2csv(path + file_name)
        temp_df=hotcsv2df(path + file_name.replace('.txt','.csv'))
        df=pd.concat([df,temp_df])
    for columna in df.columns:
        df=df.rename(columns={columna : cfg.NOMBRE_COLUMNAS_ZPM_HTO[columna]})
    columnas = list(df.columns)
    for columna in columnas:
        if columna.startswith('fecha'):
            df[columna]=pd.to_datetime(df[columna], format='%d.%m.%Y')

 
    return df
#------------------------------------------------------------------------------
def df_hot2excel_app(df):
    """ Convierte el dataframe de historico OT's en excel en la APP
    
    Detallar funcion.
    """
    path = cfg.PATH_EFICIENCIA_HOT
    with pd.ExcelWriter(path + 'hot.xlsx') as output:
        df.to_excel(output, sheet_name='hot', index = None)
#------------------------------------------------------------------------------
def df_hot2excel_kpisites(df):
    """ Convierte el dataframe de historico OT's en excel en DRIVE
    
    Detallar funcion.
    """
    with pd.ExcelWriter(cfg.PATH_KPI_SITES_HOT + 'HISTORICO_OTs.xlsx') as output:
        df.to_excel(output, sheet_name='hot', index = None)       
#------------------------------------------------------------------------------
def tiempo_prod2df():
    """ Procesa los datos de tiempos de produccion y obtiene un dataframe
    
    Detallar la función
    """
    import pandas as pd
    import kpis.configuracion.config as cfg
    
    file_name = cfg.PATH_KPI_SITES_TPO_PRODUCCION + "CALENDARIOS.xlsx"

    
    dfc2019=pd.read_excel(file_name,'CALENDAR.2019',index_col=None)
    dftp2019=pd.melt(dfc2019,id_vars=['programa','ubicacion_tecnica'],\
                     var_name='fecha', value_name='tpo_produccion')
    
    dfc2020=pd.read_excel(file_name,'CALENDAR.2020',index_col=None)
    dftp2020=pd.melt(dfc2020,id_vars=['programa','ubicacion_tecnica'],\
                     var_name='fecha', value_name='tpo_produccion')
    
    dfc2021=pd.read_excel(file_name,'CALENDAR.2021',index_col=None)
    dftp2021=pd.melt(dfc2021,id_vars=['programa','ubicacion_tecnica'],\
                     var_name='fecha', value_name='tpo_produccion')
    
    df_total=pd.concat([dftp2019,dftp2020,dftp2021], ignore_index = True)
    df_total=df_total.drop('programa', axis=1)
    return df_total

def df_tiempo_prod2excel(df):
    """ Convierte el Dataframe de tiempo de producción en un fichero excel
    
    Detallar función
    """
    file_name_output = cfg.PATH_KPI_SITES_TPO_PRODUCCION + "TIEMPO-PRODUCCION.xlsx"
    file_name_output1 = cfg.PATH_TIEMPO_PRODUCCION + "TIEMPO-PRODUCCION.xlsx"
    
    with pd.ExcelWriter(file_name_output) as output:
        df.to_excel(output, sheet_name='tp', index=False)
    with pd.ExcelWriter(file_name_output1) as output:
        df.to_excel(output, sheet_name='tp', index=False)    
    
#------------------------------------------------------------------------------
