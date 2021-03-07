# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:02:54 2021

@author: c48142
"""

import kpis.informes.costes.salida_datos
import kpis.sap.me2k
import kpis.sap.zps_capp
import kpis.configuracion.config as cfg
import pandas as pd
from datetime import datetime

now = datetime.now()
year = now.year

if input("Tienes abierto sap de ME2K?. [y/n]").upper() == 'Y':
    for year_idx in range(year - 1, year + 1):
        kpis.sap.me2k.me2k_year(year_idx)
if input("Tienes abierto sap de grafos?. [y/n]").upper() == 'Y':
    for year_idx in range(year - 1, year + 1):
        kpis.sap.zps_capp.zps_capp_year(year_idx)

for year_idx in range(year-1,year+1):
    kpis.informes.costes.salida_datos.coste_po_grafo_year(year_idx)

path_year_1 = cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year-1) + '.xlsx'
path_year = cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year) + '.xlsx'
df_year_1 = pd.read_excel(path_year_1, sheet_name='total')
df_year = pd.read_excel(path_year, sheet_name='total')
df_TOTAL = pd.concat([df_year_1,df_year])

with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT + 'TOTAL-COSTES-ODRM.xlsx') as output:
    df_TOTAL.to_excel(output, sheet_name='ODRM', index= False)

with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT_KPISITES + 'TOTAL-COSTES-ODRM.xlsx') as output:
    df_TOTAL.to_excel(output, sheet_name='ODRM', index= False)
