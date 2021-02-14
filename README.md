################################ v0.1.1 #######################################

* Correccion para evitar los cambios de cabecera en los informes de historicos
 de ot bajados de sap
* Correccion que detecta el nombre de la unidad compartida de google drive y 
lo aplica a todos los path definidos en la cofiguracion.  

################################ V0.1.2 #######################################

* El informe diario se puede generar bajo tres modalidades
  ID_ESTANDAR : Informe diario tradicional. Se muestras todas las OT's de MC
  ID_ABIERTAS : Se muestran solo las MC Abiertas
  ID_ERRORES  : Se muestran las MC de Averias a las que les falta o el tiempo
                de averia o el problema o la descripcion  de la averia.
* Creacion de función ZPS_CAPP para la extracción de datos de grafos.
* Creación de función zpscapptxt2csv para convertir el fichero extraido de sap 
  en fichero .csv
* Creación de función zpscappcsv2df para convertir el fichero .csv en un data-
  frame
* Creación de función procesar_allzpscapp2df para procesar un dataframe con
  todos los datos de un year y dpto
* Creación de función df_zpscapp2excel_app para crear un archivo excel en el
  directorio de la APP, con los datos totales de un year y dpto
* Creación de función df_zpscapp2excel_kpisites para crear un archivo excel en
  el directorio de KPIS-SITES, con los datos totales de un year y dpto
* Corregido el error de la no aparición del logo de AIRBUS en el reporte de
  Informe Diario
* De la pestaña Informe Diario de la APP se elimina la opcion de sacar el re-
  porte con/sin SAP, ya que puede llevar a confusión. Cada vez que se solicite
  un reporte, forzosamente se conecta a SAP y extrae los datos.
* Corregido error de sombrear en rojo la A en cualesquiera de los informes
  diarios, cuando hay error en la OT.

################################ V0.1.3 #######################################
* Ordenar por fecha ascendente el informe diario abiertas
* Ordenar por fecha ascendente el informe diario errores

  
  
  
  
  
########################### PENDIENTES ########################################


* Creada pestaña costes en APP, con selector dinámico de fecha y dpto según la
  configuración. Botones de extracción de datos de PO y Grafos.
  