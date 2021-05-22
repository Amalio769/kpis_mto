# -*- coding: utf-8 -*-
"""
Created on 22/05/2021

@author: C48142
"""
import pandas as pd
import numpy as np
import os, datetime
import kpis.configuracion.config as cfg

def get_status(status_sistema, status_usuario):
    """
    Determina el status de una OT como resultado de combiar el status del sistema y usuario.

    La prioridad de los status es: CACL -> CTEC -> CERR -> CPLA -> PMAT -> LIBE -> ABIE -> OTRO
    Hay prioridades en los status ya que varios de ellos pueden darse a la vez.

    :param status_sistema: string con los distintos status de sistema
    :param status_usuario: string con los distintos status de usuario
    :return: string con un único status.
    """
    super_status = status_sistema + ' ' + status_usuario

    if super_status.find('CACL') != -1:
        status = 'CACL'
    elif super_status.find('CTEC') != -1:
        status = 'CTEC'
    elif super_status.find('CERR') != -1:
        status = 'CTEC'
    elif super_status.find('CPLA') != -1:
        status = 'CPLA'
    elif super_status.find('PMAT') != -1:
        status = 'PMAT'
    elif super_status.find('LIBE') != -1:
        status = 'LIBE'
    elif super_status.find('ABIE') != -1:
        status = 'ABIE'
    else:
        status = 'OTRO'
    return status

def get_duracion_dias_ot_mp(fecha_ref, clase_orden, status, fecha_inicio_extrema, fecha_cierre_tecnico):
    """
    Calcula la duración de una OT de PM. Hasta que se cierra (CTEC) o hasta la fecha de referencia (fecha de creación

    del fichero Historico OT's).

    :param fecha_ref: datetime. Fecha creación archivo HOT.xlsx
    :param clase_orden: string. Puede ser MP o MC
    :param status: string. Status sumarizado de la OT (CACL, CTEC, CERR, CPLA, PMAT, ABIE, LIBE, OTRO)
    :param fecha_inicio_extrema: datetime. Fecha planeada para ejecución de la OT de preventivo
    :param fecha_cierre_tecnico: datetime. Fecha en la que la OT pasa al estado CTEC
    :return: int. Número de dias que la OT ha estado abierta (fecha CTEC o fecha actual) - fecha inicio extremo
    """
    if clase_orden == 'MP':
        if status == 'CTEC' or status == 'CACL':
            duracion_ot = (fecha_cierre_tecnico - fecha_inicio_extrema).days
        else:
            duracion_ot = (fecha_ref - fecha_inicio_extrema).days
    else:
        duracion_ot = np.nan
    return duracion_ot

def get_kpi_adh(kpi_adh_30_60_90, clase_orden, equipo, texto_breve):
    """
    Establece flag para indicar si la OT se utiliza para el calculo de la adherencia a 30, 60 o 90 días.

    Para kpi a 30-60 días todas las ot excepto (pu + texto breve empieza por REVISION) y excepto (px)
    Para kpi a 90 días solo (PU + texto breve empieza por REVISION) + (PX)
    :param kpi_adh_30_60_90: int. [30|60|90]. Parámetro para indicar que tipo de KPI se evalúa
    :param fecha_ref: datetime. Fecha de creación del archivo HOT.xlsx
    :param clase_orden: string [MP|MC]
    :param fecha_inicio_extrema: datetime. Fecha planeada para ejecución de la OT de preventivo
    :param equipo: sting. [PMnnnnn|PUnnnnn|PXnnnnn|Null]. Matrícula del equipo
    :param texto_breve: string. Título del mantenimiento preventivo a realizar
    :return: int [0|1]
    """
    if clase_orden == 'MP':
        if kpi_adh_30_60_90 == 30 or kpi_adh_30_60_90 == 60:
            if 'PM' in str(equipo) or ('PU' in str(equipo) and 'REVISION' not in str(texto_breve)) or pd.isna(equipo):
                kpi_adh = 1
            else:
                kpi_adh = 0
        elif kpi_adh_30_60_90 == 90:
            if ('PU' in str(equipo) and 'REVISION' in str(texto_breve)) or 'PX' in str(equipo):
                kpi_adh = 1
            else:
                kpi_adh = 0
        else:
            kpi_adh = 0
    else:
        kpi_adh = 0
    return kpi_adh

def get_status_adh_30_60_90(kpi_adh_30_60_90, clase_orden, status, duracion_dias_ot_mp):
    """
    Calcula el estado de la OT en el periodo de 30-60-90 días, según se indique en uno de los parámetros.

    Este estado de la OT es diferente al estado actual que pueda tener la OT
    :param kpi_adh_30_60_90:
    :param clase_orden:
    :param status:
    :param duracion_dias_ot_mp:
    :return: string [CTEC|ONGN|CACL] Devuelve uno de estos tres estados (a nivel conceptual, ya que ONGN no existe
            como tal en SAP)
    """
    if clase_orden == 'MP':
        if status == 'CACL':
            status_kpi_adh = 'CACL'
        else:
            if duracion_dias_ot_mp <= kpi_adh_30_60_90:
                status_kpi_adh = 'CTEC'
            else:
                status_kpi_adh = 'ONGN'
    else:
        status_kpi_adh = np.nan
    return status_kpi_adh

def get_ctec_30_60_90(kpi_adh, status):
    """
    Asigna valor 1 a aquellas OT's que se han cerrado dentro de la ventana correcta de tiempo (30-60-90).

    Este valor se utilizar para facilitar el cálculo sumarizado del total de OT's cerradas.
    :param kpi_adh: int [0|1]. 0-> esta OT no se tiene en cuenta para el calculo del KPI
                                1-> esta OT si se tiene en cuenta para el calculo del KPI
    :param status: string [CTEC|CACL|ONGN]. Indica el estado de la OT en la ventana de verificación (30-60-90)
    :return: [0|1]
    """
    if kpi_adh == 1:
        if status == 'CTEC':
            status_ctec = 1
        else:
            status_ctec = 0
    else:
        status_ctec = np.nan
    return status_ctec

def kpi_adh_mto():
    """
    Calcula el KPI de ADHERENCIA del MP.

    En esta primera fase usa el archivo HISTORICO_OTs.xlsx como fuente de datos y el archivo MP-EXCLUIDAS-KPI.xlsx con
    las OT's validadas por Airbus como excluidas.
    :return: None
    """
    # Fecha de referencia de calculo para el KPI. Se toma la fecha de creación del fichero historico OTs
    fecha_ref_adh_mp = datetime.datetime.fromtimestamp(os.path.getctime(cfg.PATH_EFICIENCIA_HOT + 'hot.xlsx'))

    # Lee los ficheros excel que contienen los historicos de OT's y las que se excluyen del cálculo del KPI.
    df_hot = pd.read_excel(cfg.PATH_KPI_SITES_HOT + 'HISTORICO_OTs.xlsx', 'hot')
    df_ot_mp_excluidas_kpi = pd.read_excel(cfg.PATH_KPI_SITES_ADH_MTO + "MP-EXCLUIDAS-KPI.xlsx", 'OTs Excluidas')

    # Copia del dataframe original, filtrado para OT's tipo MP, y sólo las columnas seleccionadas.
    df_hot_mp = df_hot.loc[df_hot['clase_orden'] == 'MP', ['clase_orden', 'tipo_trabajo', 'orden', 'ubicacion_tecnica',
                                                           'denominacion_objeto', 'equipo', 'fecha_entrada',
                                                           'fecha_inicio_extrema', 'fecha_cierre_tecnico', 'status_sistema',
                                                           'status_usuario', 'plan_mto_preventivo','texto_breve']]

    # Añadido columna de status, que es el resultado de analizar los status_sistema y status_usuario
    df_hot_mp['status'] = df_hot_mp[['status_sistema','status_usuario']].apply(lambda x: get_status(*x), axis=1)
    # Exclusión de las OT's autorizadas por Airbus
    df_hot_mp = df_hot_mp.loc[~(df_hot_mp.orden.isin(df_ot_mp_excluidas_kpi['ot_excluidas_kpi'])),:]

    # Calcula la duración de la OT, desde la fecha planificada hasta la fecha de cierre o fecha actual (lo que antes
    # ocurra.
    df_hot_mp['duracion_dias_ot_mp'] = df_hot_mp[['clase_orden','status','fecha_inicio_extrema','fecha_cierre_tecnico']].apply(lambda x: get_duracion_dias_ot_mp(fecha_ref_adh_mp, *x), axis=1)

    # Determina para cada OT si debe ser considerada para el KPI de 30, 60 y/o 90 días
    df_hot_mp['kpi_adh_30'] = df_hot_mp[['clase_orden','equipo','texto_breve']].apply(lambda x: get_kpi_adh(30, *x), axis=1)
    df_hot_mp['kpi_adh_60'] = df_hot_mp[['clase_orden','equipo','texto_breve']].apply(lambda x: get_kpi_adh(60, *x), axis=1)
    df_hot_mp['kpi_adh_90'] = df_hot_mp[['clase_orden','equipo','texto_breve']].apply(lambda x: get_kpi_adh(90, *x), axis=1)

    # Determina el status de la OT dentro de la ventana de evaluación (30, 60 , 90 días)
    df_hot_mp['status_adh_30'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(30, *x), axis=1)
    df_hot_mp['status_adh_60'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(60, *x), axis=1)
    df_hot_mp['status_adh_90'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(90, *x), axis=1)

    # Asigna un 1 a aquellas OT cerradas dentro de la ventana de evaluación (30,60,90 dias). Esto se hace para facilitar
    # el cálculo del KPI en Google Data Studio.
    df_hot_mp['ctec30'] = df_hot_mp[['kpi_adh_30','status_adh_30']].apply(lambda x: get_ctec_30_60_90(*x), axis=1)
    df_hot_mp['ctec60'] = df_hot_mp[['kpi_adh_60','status_adh_60']].apply(lambda x: get_ctec_30_60_90(*x), axis=1)
    df_hot_mp['ctec90'] = df_hot_mp[['kpi_adh_90','status_adh_90']].apply(lambda x: get_ctec_30_60_90(*x), axis=1)

    # Crea un fichero excel con el contenido del Dataframe en el compartido APP-KPI
    with pd.ExcelWriter(cfg.PATH_ADHERENCIA_MP + 'ADHERENCIA-MP.xlsx') as output:
        df_hot_mp.to_excel(output, sheet_name='ADH', index=False)

    # Crea un fichero excel con el contenido del Dataframe en el compartido de KPI-SITES
    with pd.ExcelWriter(cfg.PATH_KPI_SITES_ADH_MTO + 'ADHERENCIA-MP.xlsx') as output:
        df_hot_mp.to_excel(output, sheet_name='ADH', index=False)

def kpi_ratio_mp_mc():
    """
    Calcula el KPI de RATIO MP/MC.

    En esta primera fase usa el archivo HISTORICO_OTs.xlsx como fuente de datos para el cálculo del KPI.
    :return: None
    """
    # Lee los ficheros excel que contienen los historicos de OT's.
    df_hot = pd.read_excel(cfg.PATH_KPI_SITES_HOT + 'HISTORICO_OTs.xlsx', 'hot')

    # Añadido columna de status, que es el resultado de analizar los status_sistema y status_usuario
    df_hot['status'] = df_hot[['status_sistema', 'status_usuario']].apply(lambda x: get_status(*x), axis=1)

    # Copia del dataframe original, filtrado para OT's tipo MP, y con status == CTEC y != CACL y sólo las columnas
    # seleccionadas.
    df_hot_mp = df_hot.loc[(df_hot['clase_orden'] == 'MP') & (df_hot['status'] == 'CTEC'), ['ubicacion_tecnica',
                                                                                            'equipo',
                                                                                            'denominacion_objeto',
                                                                                            'fecha_cierre_tecnico',
                                                                                            'trabajo_real']]

    df_hot_mp['ano_mes'] = df_hot_mp['fecha_cierre_tecnico'].dt.strftime('%Y-%m')
    df_hot_mp.drop('fecha_cierre_tecnico', axis=1)
    df_hot_mp_agrupado = df_hot_mp.groupby(by=['ano_mes', 'ubicacion_tecnica', 'equipo', 'denominacion_objeto']).sum()
    df_hot_mp_agrupado = df_hot_mp_agrupado.reset_index()
    df_hot_mp_agrupado = df_hot_mp_agrupado.rename(columns={'trabajo_real': 'trabajo_real_mp'})

    # Copia del dataframe original, filtrado para OT's tipo MC, y con status == CTEC y != CACL y sólo las columnas
    # seleccionadas.
    df_hot_mc = df_hot.loc[(df_hot['clase_orden'] == 'MC') & (df_hot['status'] == 'CTEC'), ['ubicacion_tecnica',
                                                                                            'equipo',
                                                                                            'denominacion_objeto',
                                                                                            'fecha_cierre_tecnico',
                                                                                            'trabajo_real']]

    df_hot_mc['ano_mes'] = df_hot_mc['fecha_cierre_tecnico'].dt.strftime('%Y-%m')
    df_hot_mc.drop('fecha_cierre_tecnico', axis=1)
    df_hot_mc_agrupado = df_hot_mc.groupby(by=['ano_mes', 'ubicacion_tecnica', 'equipo', 'denominacion_objeto']).sum()
    df_hot_mc_agrupado = df_hot_mc_agrupado.reset_index()
    df_hot_mc_agrupado = df_hot_mc_agrupado.rename(columns={'trabajo_real': 'trabajo_real_mc'})

    # Combinación de los dos dataframes
    df_ratio_mc_mp = pd.merge(df_hot_mc_agrupado,
                              df_hot_mp_agrupado,
                              how='outer',
                              on=['ano_mes', 'ubicacion_tecnica', 'equipo', 'denominacion_objeto'])
    df_ratio_mc_mp = df_ratio_mc_mp.fillna(0)
    df_ratio_mc_mp['fecha'] = pd.to_datetime(df_ratio_mc_mp['ano_mes'], format='%Y-%m', errors='coerce')

    with pd.ExcelWriter(cfg.PATH_RATIO_MP_MC + 'RATIO-MP_MC.xlsx') as output:
        df_ratio_mc_mp.to_excel(output, sheet_name='RATIO MP-MC', index=False)

    with pd.ExcelWriter(cfg.PATH_KPI_SITES_RATIO_MP_MC + 'RATIO-MP_MC.xlsx') as output:
        df_ratio_mc_mp.to_excel(output, sheet_name='RATIO MP-MC', index=False)