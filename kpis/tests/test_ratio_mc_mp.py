# -*- coding: utf-8 -*-
"""
Created on 20/05/2021

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

# Lee los ficheros excel que contienen los historicos de OT's.
df_hot = pd.read_excel(cfg.PATH_KPI_SITES_HOT + 'HISTORICO_OTs.xlsx', 'hot')

# Añadido columna de status, que es el resultado de analizar los status_sistema y status_usuario
df_hot['status'] = df_hot[['status_sistema','status_usuario']].apply(lambda x: get_status(*x), axis=1)


# Copia del dataframe original, filtrado para OT's tipo MP, y con status == CTEC y != CACL y sólo las columnas
# seleccionadas.
df_hot_mp = df_hot.loc[(df_hot['clase_orden'] == 'MP') & (df_hot['status'] == 'CTEC') , ['ubicacion_tecnica',
                                                        'equipo', 'denominacion_objeto', 'fecha_cierre_tecnico',
                                                        'trabajo_real']]

df_hot_mp['ano_mes'] = df_hot_mp['fecha_cierre_tecnico'].dt.strftime('%Y-%m')
df_hot_mp.drop('fecha_cierre_tecnico', axis=1)
df_hot_mp_agrupado = df_hot_mp.groupby(by=['ano_mes', 'ubicacion_tecnica','equipo','denominacion_objeto']).sum()
df_hot_mp_agrupado = df_hot_mp_agrupado.reset_index()
df_hot_mp_agrupado = df_hot_mp_agrupado.rename(columns = {'trabajo_real':'trabajo_real_mp'})

# Copia del dataframe original, filtrado para OT's tipo MC, y con status == CTEC y != CACL y sólo las columnas
# seleccionadas.
df_hot_mc = df_hot.loc[(df_hot['clase_orden'] == 'MC') & (df_hot['status'] == 'CTEC') , ['ubicacion_tecnica',
                                                        'equipo', 'denominacion_objeto', 'fecha_cierre_tecnico',
                                                        'trabajo_real']]

df_hot_mc['ano_mes'] = df_hot_mc['fecha_cierre_tecnico'].dt.strftime('%Y-%m')
df_hot_mc.drop('fecha_cierre_tecnico', axis=1)
df_hot_mc_agrupado = df_hot_mc.groupby(by=['ano_mes', 'ubicacion_tecnica','equipo','denominacion_objeto']).sum()
df_hot_mc_agrupado = df_hot_mc_agrupado.reset_index()
df_hot_mc_agrupado = df_hot_mc_agrupado.rename(columns = {'trabajo_real':'trabajo_real_mc'})

# Combinación de los dos dataframes
df_ratio_mc_mp = pd.merge(df_hot_mc_agrupado,
                          df_hot_mp_agrupado,
                          how='outer',
                          on=['ano_mes','ubicacion_tecnica','equipo','denominacion_objeto'])
df_ratio_mc_mp = df_ratio_mc_mp.fillna(0)
df_ratio_mc_mp['fecha'] = pd.to_datetime(df_ratio_mc_mp['ano_mes'], format='%Y-%m', errors='coerce')

with pd.ExcelWriter(cfg.PATH_RATIO_MP_MC + 'RATIO-MP_MC.xlsx') as output:
    df_ratio_mc_mp.to_excel(output, sheet_name='RATIO MP-MC', index=False)

with pd.ExcelWriter(cfg.PATH_KPI_SITES_RATIO_MP_MC + 'RATIO-MP_MC.xlsx') as output:
    df_ratio_mc_mp.to_excel(output, sheet_name='RATIO MP-MC', index=False)