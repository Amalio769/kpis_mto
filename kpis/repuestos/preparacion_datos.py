# -*- coding: utf-8 -*-
"""
Created on 28/02/2021

@author: C48142
"""


# ------------------------------------------------------------------------------
def me2k_maxr_txt2df_all():
    """ Iteración de la funcion me2ktxt2df para los archivos MAXR

    Detallar funcionalidad
    """
    import pandas as pd
    import kpis.configuracion.config as cfg
    import kpis.informes.costes.preparacion_datos as datos
    import os

    file_list = os.listdir(cfg.PATH_REPUESTOS_MAXR)
    tipo_me2k='ceco'
    path = cfg.PATH_REPUESTOS_MAXR
    datos_df = pd.DataFrame()
    for file_name in file_list:
        temp_df = datos.me2ktxt2df(path + file_name, tipo_me2k, int(file_name[0:4]))
        datos_df = pd.concat([datos_df, temp_df])
    return datos_df

# ------------------------------------------------------------------------------
