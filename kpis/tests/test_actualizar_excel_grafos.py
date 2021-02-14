# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 08:26:52 2021

@author: C48142
"""

import kpis.sap.zps_capp as sap
import kpis.informes.costes.preparacion_datos as datos

year = 2021
dpto = 'ODRM'

sap.zps_capp_year_dpto(year,dpto)


df=datos.procesar_allzpscapp2df(year, dpto)
datos.df_zpscapp2excel_app(df,year, dpto)
datos.df_zpscapp2excel_kpisites(df,year, dpto)