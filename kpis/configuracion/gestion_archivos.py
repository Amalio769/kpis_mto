# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 19:50:59 2021

@author: C48142
"""

import os
import kpis.configuracion.config as cfg

#------------------------------------------------------------------------------
def list_ficheros(path, year, dpto, extension):
    """ Devuelve listado con los archivos del path, year, dpto y extension
    
    pasados en la funcion.
    """
    output = []
    contenido = os.listdir(path)  
    for file_name in contenido:
        if (file_name.find(str(year)) != -1 and \
            file_name.find(dpto + '-') != -1 and \
                          file_name.endswith(extension)):
            output.append(file_name)
    return output
#------------------------------------------------------------------------------
def delete_list_ficheros(path, year, dpto, extension):
    """ Borra los archivos seleccionados por path, year, dpto y extension
    
    pasados en la funcion.
    """
    contenido = os.listdir(path)  
    for file_name in contenido:
        if (file_name.find(str(year)) != -1 and \
            file_name.find(dpto + '-') != -1 and \
                          file_name.endswith(extension)):
            os.remove(path + file_name)
#------------------------------------------------------------------------------      
if __name__ == '__main__':
    path = cfg.PATH_COSTES_PEP
    year = 2020
    dpto = 'ODRM'
    extension = 'txt'
    for linea in list_ficheros(path, year, dpto, extension):
        print(linea)