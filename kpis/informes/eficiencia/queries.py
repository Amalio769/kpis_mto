# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:47:08 2021

@author: C48142
"""

import sys
import pandas as pd
import kpis.configuracion.config as cfg
from datetime import datetime


#------------------------------------------------------------------------------
def select_col_df(df, columnas):
    """ Seleccionar un determinado listado de columnas del dataframe df
    
    Detallar la función.
    """
    df_output=pd.DataFrame()
    columnas_df= list(df.columns)
    
    for new_col_df in columnas:
        if new_col_df in columnas_df:
            df_output[new_col_df]=df[[new_col_df]]
        else:
            sys.exit("Error al pasar argumentos 'columnas' en la función "+\
                     "select_col_df()")
    
    return df_output
#------------------------------------------------------------------------------
def query_hot(df, p_clase_orden="", p_tipo_trabajo="", p_ubicacion_tecnica="",\
              p_equipo="", p_f_entrada_ini="", p_f_entrada_fin="",\
              p_not_status="", p_status="", p_not_CACL= False,\
              p_not_CTEC= False, p_not_CERR= False, p_fallo="", p_problema="",\
              p_programa=""):
    """ Query sobre el DataFrame de Historico OTs
    
    La query utiliza los campos principales del dataframe, y se detallan a 
    continuación.
    
    Parámetros:
    df            : (DataFrame) Obligatorio. Dataframe con los datos
    p_clase_orden : (string/array)[Opcional]. Ejemplos: 'MC', ['MP','MC','MM']
                    Si se deja en blanco se seleccionan todos los registros.
    p_tipo_trabajo: (string/array)[Opcional]. Ejemplos: 'A', ['A','T']
                    Si se deja en blanco se seleccionan todos los registros.
    p_ubicacion_tecnica: (string/array)[Opcional]. Ejemplos:
                    'P-A320-TIMA-ST10',
                    ['P-A320-TIMA-ST10','P-A320-TIMA-ST30_1']
    p_equipo      : (string/array)[Opcional].
    P_f_entrada_ini : (datetime)[opcional] Fecha de entrada desde
    P_f_entrada_fin : (datetime)[opcional] Fecha de entrada hasta
    p_not_status  : (string)[Opcional]. Ejemplo: 'MOVM', 'CPLA',...
                    Si se deja en blanco se seleccionan todos los registros
    p_status      : (string)[Opcional]. Ejemplo: 'MOVM', 'CPLA',...
                    Si se deja en blanco se seleccionan todos los registros
    p_not_CACL    : [True/False][Opcional]. True = se excluyen los registros
                    con status CACL. False = No se excluyen estos registros.
    p_not_CTEC    : [True/False][Opcional]. True = se excluyeb los registros
                    con status CTEC. False = No se excluyen estos registros.
    p_not_CERR    : [True/False][Opcional]. True = se excluyeb los registros
                    con status CERR. False = No se excluyen estos registros.
    p_fallo       :
    p_problema    :
    """
    JOIN_AND = ' & '
    lst_query =[]
    
    # Comprobación de los parámetros
    if p_f_entrada_ini != "" and type(p_f_entrada_ini) != datetime:
        sys.exit("Función query_hot. El parámetro p_f_entrada_ini no es "+\
                 "del tipo datetime.")
    if p_f_entrada_fin != "" and type(p_f_entrada_fin) != datetime:
        sys.exit("Función query_hot. El parámetro p_f_entrada_fin no es "+\
                 "del tipo datetime.")
    if p_not_status != "" and p_not_status not in cfg.STATUS_OT:
        sys.exit("Función query_hot. Parámetro p_not_status no correcto.")
    if p_status != "" and p_status not in cfg.STATUS_OT:
        sys.exit("Función query_hot. Parámetro p_status no correcto.")
    if p_not_CACL not in [True,False]:
        sys.exit("Función query_hot. Parámetro p_not_CACL no correcto.")
    if p_not_CTEC not in [True,False]:
        sys.exit("Función query_hot. Parámetro p_not_CTEC no correcto.")
    if p_not_CERR not in [True,False]:
        sys.exit("Función query_hot. Parámetro p_not_CERR no correcto.")
    if p_programa != "" and p_programa not in cfg.PROGRAMAS:
        sys.exit("Función query_hot. Parámetro p_programa no correcto.")
    
    # Condiciones de la query
    if p_clase_orden != "":
        lst_query.append('clase_orden in @p_clase_orden')
    if p_tipo_trabajo != "":
        lst_query.append('tipo_trabajo in @p_tipo_trabajo')
    if p_ubicacion_tecnica != "":
        lst_query.append('ubicacion_tecnica in @p_ubicacion_tecnica')
    if p_equipo != "":
        lst_query.append('equipo in @p_equipo')
    if p_f_entrada_ini != "":
        lst_query.append('fecha_entrada >= @p_f_entrada_ini')
    if p_f_entrada_fin != "":
        lst_query.append('fecha_entrada <= @p_f_entrada_fin')
    if p_status != "":
        lst_query.append('(status_sistema.str.contains(@p_status) | '+\
                           'status_usuario.str.contains(@p_status))')
    if p_not_status != "":
        lst_query.append('~(status_sistema.str.contains(@p_not_status) | '+\
                           'status_usuario.str.contains(@p_not_status))')
    if p_not_CACL:
        lst_query.append('~(status_usuario.str.contains("CACL"))')
    if p_not_CTEC:
        lst_query.append('~(status_sistema.str.contains("CTEC"))')
    if p_not_CERR:
        lst_query.append('~(status_sistema.str.contains("CERR"))')
    if p_fallo != "":
        lst_query.append('fallo.str.contains(@p_fallo)')
    if p_problema != "":
        lst_query.append('problema.str.contains(@p_problema)')
    if p_programa != "":
        lst_query.append('ubicacion_tecnica.str.contains(@p_programa)')
        
    texto_query = JOIN_AND.join(lst_query)
    texto_query = texto_query.lstrip(JOIN_AND).rstrip(JOIN_AND)
    
#    print(texto_query)
    df_output=df.query(texto_query, engine='python')
    
    return df_output
#------------------------------------------------------------------------------
def query_tiempo_produccion(df, fecha_ini, fecha_fin, ubicaciontecnica=""):
    """ Query sobre el dataframe de tiempo de producción.
    
    Detallar función.
    """
    JOIN_AND = ' & '
    lst_query =[]
    
    # Comprobación de los parámetros
    if type(fecha_ini) != datetime:
        sys.exit("Función query_tiempo_prod. El parámetro fecha_ini no es "+\
                 "del tipo datetime.")
    if type(fecha_fin) != datetime:
        sys.exit("Función query_tiempo_prod. El parámetro fecha_fin no es "+\
                 "del tipo datetime.")
    if ubicaciontecnica != "" and ~ubicaciontecnica.startswith('P-'):
        sys.exit("Función query_tiempo_prod. El parámetro ubicaciontecnica "+\
                 "no es es correcto.")

    # Condiciones de la query

    if ubicaciontecnica != "":
        lst_query.append('ubicacion_tecnica in @ubicaciontecnica')
    lst_query.append('fecha >= @fecha_ini')
    lst_query.append('fecha <= @fecha_fin')

    texto_query = JOIN_AND.join(lst_query)
    texto_query = texto_query.lstrip(JOIN_AND).rstrip(JOIN_AND)
    
#    print(texto_query)
    df_output=df.query(texto_query, engine='python')
    
    return df_output