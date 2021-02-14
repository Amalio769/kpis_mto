# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:08:32 2021

@author: C48142
"""
import kpis.sap.me2k as sap
import kpis.informes.costes.preparacion_datos as datos

year = 2020
dpto = 'ODRM'

sap.me2k_year_dpto(year,dpto)


df=datos.combinar_pep_ceco_orden(year, dpto)
datos.df_pco2excel_app(df,year, dpto)
datos.df_pco2excel_kpisites(df,year, dpto)