# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 18:12:09 2021

@author: C48142
"""

import kpis.informes.eficiencia.preparacion_datos as datos

df=datos.tiempo_prod2df()
datos.df_tiempo_prod2excel(df)