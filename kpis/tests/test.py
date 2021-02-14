# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:39:54 2020

@author: C48142
"""
import kpis.configuracion.config as cfg
import os, sys
import pandas as pd

path_file_name = cfg.PATH_CONFIGURACION_APP + "CONFIGURACION-APP.txt"
col_names = ['year','dpto']
if os.path.isfile(path_file_name):
    df=pd.read_csv(path_file_name, sep=';', header=None, names = col_names,\
                   index_col= None,dtype={'year': 'int64','dpto': 'str'}, encoding = 'latin-1')
else:
    sys.exit("Error. No se puede abrir el fichero " + path_file_name)
