# -*- coding: utf-8 -*-
"""
Procesa el archivo file_name_woe (without extension) : corrige los
errores del fichero csv y genera un fichero html con el mismo nombre
(file_name_woe)
@param: file_name_woe -> nombre archivo sin extensión
Created on Thu Dec 24 07:29:35 2020

@author: C48142
"""
import kpis.configuracion.config as cfg

def procesar_informe(file_path,file_name_woe,fecha_ini,fecha_fin,\
                     tipo_reporte=cfg.ID_ESTANDAR):
   """ Procesa el archivo file_name_woe (without extension)
   
   Corrige los errores del fichero csv y genera un fichero html con el mismo
   nombre (file_name_woe)
   
   Parámetros:
   ----------
   * file_path     : (string) directorio en formato G://name/name1..../
   
   * file_name_woe : (string) nombre archivo sin extensión
   
   * fecha_ini     : (string) fecha de inicio del reporte
   
   * fecha_fin     : (string) fecha final del reporte
   
   * tipo_reporte  : (int) Tipo de informe. Hay tres tipos de informes:
                     ID_ESTANDAR -> reporte estandar
                     ID_ABIERTAS -> reporte con Ot's abiertas
                     ID_ERRORES  -> reporte con Ot's con errores
   """
   import kpis.informes.diario.preparacion_datos as datos
   import pandas as pd
   import numpy as np
   import kpis.configuracion.config as cfg
   
   # Las siguientes instrucciones corrigen el fichero csv, que tiene un ; de
   # más en la cabecera y le falta un ; por el campo Sum_PAIR.
   datos.modificarCabeceraCsv(file_path + file_name_woe + '.csv')
   datos.modificarContenidoCsv(file_path + file_name_woe + '.csv')
   
   # Crea un dataframe leyendo el archivo file_name
   df_archivoCsv=pd.read_csv(file_path + file_name_woe + '.csv',\
                             sep=';', header=0, na_values="",\
                             encoding='latin_1',engine='python')
   # Elimina los espacios en blanco de los nombres de columna
   df_archivoCsv.columns = df_archivoCsv.columns.str.replace(' ','_')
   # Crea una vista del df original, con los campos necesarios para la 
   # creación del informe
   vistaID=df_archivoCsv[['Orden',\
                          'Status_de_sistema',\
                          'Status_de_usuario',\
                          'Ubicación_técnica',\
                          'Tipo_de_trabajo',\
                          'Equipo',\
                          'Denominación_objeto',\
                          'Problema',\
                          'Fecha_entrada',\
                          'Hr._creacion',\
                          'Fecha_inicio',\
                          'Hora_inicio',\
                          'F._Cierre_Tecnico',\
                          'Hora_Cierre_Técnico',\
                          'H._pers',\
                          'Coste_M.',\
                          'H._parada',\
                          'Sumatorio_Horas_status_CPLA',\
                          'Sumatorio_Horas_status_PSUP',\
                          'Sumatorio_Horas_status_PMAT',\
                          'Sumatorio_horas_status_TMPO',\
                          'Tiempo_Respuest',\
                          'Tiempo_Total',\
                          'Sumatorio_Horas_status_PAIR',\
                          'Texto_largo',\
                          'Resolución_avería']]
      
   # Ordenar los datos por Ubi.Técnica, Equipo y Tipo Trabajo
   vistaID = vistaID.sort_values(by=['Ubicación_técnica','Equipo',\
                                     'Tipo_de_trabajo'])
   texto_tipo_reporte = "ESTANDAR"
   # Filtro para obtener dataframe con las ot's abiertas
   if tipo_reporte == cfg.ID_ABIERTAS:
       texto_tipo_reporte = "OT's ABIERTAS"
       vistaID = vistaID[~vistaID['Status_de_usuario'].str.contains('CACL') 
                        & ~vistaID['Status_de_sistema'].str.contains('CTEC','CERR')]
       # Ordenar los datos por Orden, Ubi.Técnica y Equipo
       vistaID = vistaID.sort_values(by=['Orden','Ubicación_técnica',\
                                         'Equipo'])
       
   # Filtro para obtener dataframe con ot's de averias cerradas y con errores
   if tipo_reporte == cfg.ID_ERRORES:
       texto_tipo_reporte = "OT's MC(A) CON ERRORES"
       vistaID = vistaID[~vistaID['Status_de_usuario'].str.contains('CACL') 
                        & vistaID['Status_de_sistema'].str.contains('CTEC','CERR')
                        & vistaID['Tipo_de_trabajo'].str.contains('A')
                        & ((vistaID['Resolución_avería'].isnull())
                           | (vistaID['Problema'].isnull())
                           | (vistaID['H._parada'] == 0))]
       # Ordenar los datos por Orden, Ubi.Técnica y Equipo
       vistaID = vistaID.sort_values(by=['Orden','Ubicación_técnica',\
                                         'Equipo'])                 

   # Utilizando una plantilla de HTML crea una página web con una tabla que 
   # contiene toda la información del reporte. A continuación se itera el df y
   # se sustituyen los códigos de cada celda por el valor correspondiente del
   # informe.
   texto_html=[]
   texto_html.append(cfg.HTML_ID["CABECERA"].\
                     replace("{FECHA_INI}",fecha_ini).\
                     replace("{FECHA_FIN}",fecha_fin).\
                     replace("{PATH_LOGO}",cfg.PATH_INFORME_DIARIO).\
                     replace("{TIPO_REPORTE}", texto_tipo_reporte))

   for index, row in vistaID.iterrows():
       t_html=cfg.HTML_ID["TABLA"]
       t_html=t_html.replace("{01}", str(row["Orden"]))
       t_html=t_html.replace("{02}", str(row["Ubicación_técnica"]))
       t_html=t_html.replace("{03}", str(row["Equipo"])+'-'+ str(row["Denominación_objeto"]))
       t_html=t_html.replace("{04}", str(row["Status_de_sistema"]))
       t_html=t_html.replace("{05}", "Fecha Ent/Ini/Fin")
       t_html=t_html.replace("{07}", "H.Par.")
       t_html=t_html.replace("{08}", "T.Resp")
       t_html=t_html.replace("{09}", "T.Resol")
       t_html=t_html.replace("{010}", "T.Aver")
       t_html=t_html.replace("{011}", "T.Tot")
       t_html=t_html.replace("{11}", row["Tipo_de_trabajo"])
       t_html=t_html.replace("{12}", str(row["Texto_largo"]))
       t_html=t_html.replace("{13}", str(row["Resolución_avería"]))
       t_html=t_html.replace("{15}", row["Fecha_entrada"])
       t_html=t_html.replace("{16}", row["Hr._creacion"])
       t_html=t_html.replace("{17}", str(round(row["H._parada"],2)))
       t_html=t_html.replace("{18}", str(round(row["Tiempo_Respuest"],2)))
       t_html=t_html.replace("{19}", str(round(row["Sumatorio_horas_status_TMPO"]-row["Tiempo_Respuest"],2)))
       t_html=t_html.replace("{110}", str(round(row["Sumatorio_horas_status_TMPO"],2)))
       t_html=t_html.replace("{111}", str(round(row["Tiempo_Total"],2)))
       t_html=t_html.replace("{25}", row["Fecha_inicio"])
       t_html=t_html.replace("{26}", row["Hora_inicio"])
       t_html=t_html.replace("{28}", "T.CPLA")
       t_html=t_html.replace("{29}", "T.PMAT")
       t_html=t_html.replace("{210}", "T.PSUP")
       t_html=t_html.replace("{211}", "C.Mat")
       t_html=t_html.replace("{31}", str(row["Problema"]))
       t_html=t_html.replace("{34}", row["Status_de_usuario"])
       t_html=t_html.replace("{35}", row["F._Cierre_Tecnico"])
       t_html=t_html.replace("{36}", row["Hora_Cierre_Técnico"])
       t_html=t_html.replace("{38}", str(round(row["Sumatorio_Horas_status_CPLA"],2)))
       t_html=t_html.replace("{39}", str(round(row["Sumatorio_Horas_status_PMAT"],2)))
       t_html=t_html.replace("{310}", str(round(row["Sumatorio_Horas_status_PSUP"],2)))

       # Por motivos que desconozco cuando en la descarga del fichero de SAP hay algún dato erróneo en la columna
       # de Coste_M. la considera como string, en caso de que los datos sean correctos se bajan como float.
       # Por ese motivo en el código que sigue a continuación se analiza si dicho campo es str o float.
       if type(row["Coste_M."]) == str:
           t_html = t_html.replace("{311}", row["Coste_M."])
       if type(row["Coste_M."]) == float:
           t_html = t_html.replace("{311}", str(round(row["Coste_M."],2)))

       # Si la OT ha sido cancelada toda la linea se pone en gris
       if row["Status_de_usuario"].find('CACL') != -1:
           t_html=t_html.replace("{COLOR_TIPO_TRABAJO}","lightgray")
           t_html=t_html.replace("{COLOR_HORA_PARADA}","lightgray")
           t_html=t_html.replace("{COLOR_PROBLEMA}","lightgray")
           t_html=t_html.replace("{COLOR_GENERAL}","lightgray")
       # Si la OT de Avería está activa toda la línea se coloca en rojo
       if row["Status_de_usuario"].find('CACL') == -1 and \
             row["Status_de_sistema"].find('CTEC')== -1 and \
             row["Tipo_de_trabajo"]=='A':
           t_html=t_html.replace("{COLOR_TIPO_TRABAJO}","red")
           t_html=t_html.replace("{COLOR_HORA_PARADA}","red")
           t_html=t_html.replace("{COLOR_PROBLEMA}","red")
           t_html=t_html.replace("{COLOR_GENERAL}","red")
       # Coloca la A en Rojo si no se han completado los datos de tiempo de
       # parada, resolución de averia o problema. La OT tiene que tener el CTEC
       if row["Tipo_de_trabajo"]=='A' and (row["H._parada"] == 0 or \
                                           str(row["Resolución_avería"]) == "nan" or\
                                           str(row["Problema"]) == "nan")\
                                      and row["Status_de_sistema"].find('CTEC')!= -1:
           t_html=t_html.replace("{COLOR_TIPO_TRABAJO}","red")
       else:
           t_html=t_html.replace("{COLOR_TIPO_TRABAJO}","black")
       # Coloca el tiempo de parada en rojo si supera > 1hora y es Averia
       if row["Tipo_de_trabajo"]=='A' and row["H._parada"] > 1.0:
           t_html=t_html.replace("{COLOR_HORA_PARADA}","red")
       else:
           t_html=t_html.replace("{COLOR_HORA_PARADA}","blue")
       # Una vez chequeadas las condiciones el resto de etiquetas de color se
       # ponen al color de defecto
       t_html=t_html.replace("{COLOR_TIPO_TRABAJO}","black")
       t_html=t_html.replace("{COLOR_HORA_PARADA}","black")
       t_html=t_html.replace("{COLOR_PROBLEMA}","blue")
       t_html=t_html.replace("{COLOR_GENERAL}","black")

       texto_html.append(t_html)
   texto_html.append(cfg.HTML_ID["PIE"])
   

   # Creación del archivo html a partir de los datos procesasos anteriormente.
   f=open(file_path + file_name_woe + '.html',"w")
   f.write("".join(texto_html))
   f.close()