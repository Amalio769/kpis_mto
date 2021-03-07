# -*- coding: utf-8 -*-
"""
Created on 28/02/2021

@author: C48142
"""

def maxr_df2excel():
    """ Procesa todos los archivos MAXR

    :return:
    """
    import kpis.repuestos.preparacion_datos as datos
    import kpis.configuracion.config as cfg
    import pandas as pd

    df = datos.me2k_maxr_txt2df_all()
    with pd.ExcelWriter(cfg.PATH_REPUESTOS_OUTPUT + 'TOTAL-MAXR.xlsx') as output:
        df.to_excel(output, sheet_name='REPUESTOS', index=False)
    with pd.ExcelWriter(cfg.PATH_REPUESTOS_OUTPUT_KPISITES + 'TOTAL-MAXR.xlsx') as output:
        df.to_excel(output, sheet_name='REPUESTOS', index=False)
