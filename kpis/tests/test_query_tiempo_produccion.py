# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 17:33:00 2021

@author: C48142
"""

from datetime import datetime
from kpis.informes.eficiencia.queries import query_tiempo_produccion
import kpis.informes.eficiencia.preparacion_datos as datos


df=datos.tiempo_prod2df()

df1=query_tiempo_produccion(df,\
                  fecha_ini=datetime.strptime("1/1/2020",'%d/%m/%Y'),\
                  fecha_fin=datetime.strptime("31/12/2020",'%d/%m/%Y'),\
                  ubicaciontecnica = '')
