# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 16:47:27 2021

@author: C48142
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import kpis.informes.eficiencia.queries as queries
import kpis.configuracion.config as cfg
import kpis.informes.eficiencia.preparacion_datos as datos

FECHA_INI = "1/2/2020"
FECHA_FIN = "31/12/2020"

dfh=pd.read_excel(cfg.PATH_EFICIENCIA_HOT+'hot.xlsx',sheetname='hot')
dfp=datos.tiempo_prod2df()

df1=queries.query_hot(dfh,\
                      p_clase_orden='MC',\
                      p_tipo_trabajo='A',\
                      #p_ubicacion_tecnica = '',\
                      p_f_entrada_ini=datetime.strptime(FECHA_INI,'%d/%m/%Y'),\
                      p_f_entrada_fin=datetime.strptime(FECHA_FIN,'%d/%m/%Y'),\
                      #p_not_status = ''\
                      p_status= 'CTEC',\
                      p_not_CACL= True,\
                      #p_not_CTEC= False,\
                      #p_not_CERR= False,\
                      p_programa = 'A350')

df2=queries.query_tiempo_produccion(dfp,\
                            fecha_ini=datetime.strptime(FECHA_INI,'%d/%m/%Y'),\
                            fecha_fin=datetime.strptime(FECHA_FIN,'%d/%m/%Y'),\
                            ubicaciontecnica = '')
""" Grafico con columnas para nº ots y h.parada en el eje izquierdo y grafico
de lineas para el MTTR en el eje drcho"""
tbl=df1.groupby(df1.fecha_entrada.dt.to_period('m'))\
               .agg({'tiempo_parada':['count',sum]})
tbl.columns=["_".join(i) for i in tbl.columns.ravel()]
tbl['mttr']=round(tbl['tiempo_parada_sum']/tbl['tiempo_parada_count'],2)
tbl=tbl.reset_index()


tbl.plot(kind='bar',x='fecha_entrada',y=['tiempo_parada_count','tiempo_parada_sum'])
ax = tbl['mttr'].plot(secondary_y=True, color='k', marker='o')
ax.set_ylabel('mttr')
plt.savefig("figure.pdf")
plt.margins(0.2)
plt.subplots_adjust(left=0.15, bottom=0.15)
plt.show()



