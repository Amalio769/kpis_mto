# -*- coding: utf-8 -*-
"""
Created on 27/02/2021

@author: C48142
"""

import kpis.configuracion.config as cfg
import pandas as pd

year=2020
df_pep = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='pep')
df_ceco = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='ceco')
df_ceco_grafo = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='ceco-grafo')
df_orden = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='orden')

for row in df_ceco_grafo.itertuples():
    if row.ceco_grafo == 13301410:
        hr301 = row.hr
    if row.ceco_grafo == 13211410:
        hr211 = row.hr
    if row.ceco_grafo == 13215410:
        hr215 = row.hr