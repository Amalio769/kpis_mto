# -*- coding: utf-8 -*-
"""
Created on 14/05/2021

@author: c48142
"""

import pandas as pd
import numpy as np
import os, datetime
import kpis.configuracion.config as cfg

def get_status(status_sistema, status_usuario):
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
    if clase_orden == 'MP':
        if status == 'CTEC' or status == 'CACL':
            duracion_ot = (fecha_cierre_tecnico - fecha_inicio_extrema).days
        else:
            duracion_ot = (fecha_ref - fecha_inicio_extrema).days
    else:
        duracion_ot = np.nan
    return duracion_ot
def get_kpi_adh(kpi_adh_30_60_90, fecha_ref, clase_orden, fecha_inicio_extrema):
    if clase_orden == 'MP':
        if (fecha_ref - fecha_inicio_extrema).days >= kpi_adh_30_60_90:
            kpi_adh = 1
        else:
            kpi_adh = 0
    else:
        kpi_adh = 0
    return kpi_adh

def get_status_adh_30_60_90(kpi_adh_30_60_90, clase_orden, status, duracion_dias_ot_mp):
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

# Fecha de referencia de calculo para el KPI. Se toma la fecha de creación del fichero historico OTs
fecha_ref_adh_mp = datetime.datetime.fromtimestamp(os.path.getctime(cfg.PATH_EFICIENCIA_HOT + 'hot.xlsx'))

# Lee los ficheros excel que contienen los historicos de OT's y las que se excluyen del cálculo del KPI.
df_hot = pd.read_excel(cfg.PATH_EFICIENCIA_HOT + 'hot.xlsx', 'hot')
df_ot_mp_excluidas_kpi = pd.read_excel(cfg.PATH_ADHERENCIA_MP + "MP-EXCLUIDAS-KPI.xlsx", 'OTs Excluidas')

# Copia del dataframe original, filtrado para OT's tipo MP, y sólo las columnas seleccionadas.
df_hot_mp = df_hot.loc[df_hot['clase_orden'] == 'MP', ['clase_orden', 'tipo_trabajo', 'orden', 'ubicacion_tecnica',
                                                       'denominacion_objeto', 'equipo', 'fecha_entrada',
                                                       'fecha_inicio_extrema', 'fecha_cierre_tecnico', 'status_sistema',
                                                       'status_usuario', 'plan_mto_preventivo','texto_breve']]

# Añadido columna de status, que es el resultado de analizar los status_sistema y status_usuario
df_hot_mp['status'] = df_hot_mp[['status_sistema','status_usuario']].apply(lambda x: get_status(*x), axis=1)
# Exclusión de las OT's autorizadas por Airbus
df_hot_mp = df_hot_mp.loc[~(df_hot_mp.orden.isin(df_ot_mp_excluidas_kpi['ot_excluidas_kpi'])),:]

df_hot_mp['duracion_dias_ot_mp'] = df_hot_mp[['clase_orden','status','fecha_inicio_extrema','fecha_cierre_tecnico']].apply(lambda x: get_duracion_dias_ot_mp(fecha_ref_adh_mp, *x), axis=1)
df_hot_mp['kpi_adh_30'] = df_hot_mp[['clase_orden','fecha_inicio_extrema']].apply(lambda x: get_kpi_adh(30, fecha_ref_adh_mp, *x), axis=1)
df_hot_mp['kpi_adh_60'] = df_hot_mp[['clase_orden','fecha_inicio_extrema']].apply(lambda x: get_kpi_adh(60, fecha_ref_adh_mp, *x), axis=1)
df_hot_mp['kpi_adh_90'] = df_hot_mp[['clase_orden','fecha_inicio_extrema']].apply(lambda x: get_kpi_adh(90, fecha_ref_adh_mp, *x), axis=1)

df_hot_mp['status_adh_30'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(30, *x), axis=1)
df_hot_mp['status_adh_60'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(60, *x), axis=1)
df_hot_mp['status_adh_90'] = df_hot_mp[['clase_orden','status','duracion_dias_ot_mp']].apply(lambda x: get_status_adh_30_60_90(90, *x), axis=1)

with pd.ExcelWriter(cfg.PATH_ADHERENCIA_MP + 'ADHERENCIA-MP.xlsx') as output:
    df_hot_mp.to_excel(output, sheet_name='ADH', index=False)

with pd.ExcelWriter(cfg.PATH_KPI_SITES_ADH_MTO + 'ADHERENCIA-MP.xlsx') as output:
    df_hot_mp.to_excel(output, sheet_name='ADH', index=False)