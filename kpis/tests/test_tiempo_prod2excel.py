# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 16:42:08 2021

@author: C48142
"""

import kpis.informes.eficiencia.preparacion_datos as datos

df=datos.tiempo_prod2df()
datos.df_tiempo_prod2excel(df)