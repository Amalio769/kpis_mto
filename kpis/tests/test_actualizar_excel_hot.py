# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 21:05:35 2021

@author: C48142
"""

import kpis.informes.eficiencia.preparacion_datos as datos

df=datos.procesar_allhto2df()
datos.df_hot2excel_app(df)
datos.df_hot2excel_kpisites(df)