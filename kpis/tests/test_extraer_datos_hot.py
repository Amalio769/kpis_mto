
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 19:02:43 2020

@author: C48142
"""

import kpis.configuracion.config as cfg
import kpis.sap.zpm_report_mwo as sap
from datetime import datetime

now=datetime.now()

for x in range(2020,2022):
    for i in cfg.FECHAS_HOT[x].keys():
        if datetime.strptime(cfg.FECHAS_HOT[x][i]['DESDE'],'%d.%m.%Y') < now:
            sap.zpm_report_mwo_hot(clase_orden='',\
                                   fecha_entrada_desde = cfg.FECHAS_HOT[x][i]['DESDE'],\
                                   fecha_entrada_hasta = cfg.FECHAS_HOT[x][i]['HASTA'],\
                                   variante = 'APP-ODRMP-01',\
                                   path = cfg.PATH_EFICIENCIA_HOT,\
                                   file_name_woe = i)