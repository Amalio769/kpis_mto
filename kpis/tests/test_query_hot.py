# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:47:27 2021

@author: C48142
"""

import pandas as pd
from datetime import datetime
from kpis.informes.eficiencia.queries import query_hot
import kpis.configuracion.config as cfg

df=pd.read_excel(cfg.PATH_EFICIENCIA_HOT+'hot.xlsx',sheetname='hot')
columnas = ['clase_orden','tipo_trabajo','orden','ubicacion_tecnica',\
            'equipo','fecha_entrada','tiempo_parada']


#df1=select_col_df(df, columnas)
df1=query_hot(df,\
              p_clase_orden='MC',\
              p_tipo_trabajo='A',\
              #p_ubicacion_tecnica = '',\
              p_f_entrada_ini=datetime.strptime("1/1/2020",'%d/%m/%Y'),\
              p_f_entrada_fin=datetime.strptime("31/12/2020",'%d/%m/%Y'),\
              #p_not_status = ''\
              p_status= 'CTEC',\
              p_not_CACL= True,\
              #p_not_CTEC= False,\
              #p_not_CERR= False,\
              p_programa = 'A350')







