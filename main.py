# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 13:11:25 2021

@author: C48142
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QGroupBox, QTabWidget, QComboBox
from PyQt5.QtCore import QDate
from main_ui import *
import datetime
from datetime import timedelta
import sys
import kpis.informes.diario.salida_datos as ids
import kpis.sap.zpm_report_mwo as sap
import kpis.configuracion.config as cfg
import webbrowser as wb
import pandas as pd


def informe_diario():
    """ Extrae los datos de sap y presenta en Chrome el Informe Diario
    
    Detallar la funcion.
    """
    #Para indicar que el proceso de Informe diario está activo, aparece en pantalla el
    #texto "Working..."
    #label_informe_diario_procesando.setText("Working...")
    #label_informe_diario_procesando.adjustSize()

    fecha_inicio = window.dateEdit_fechainicio.date().toString("dd.MM.yyyy")
    fecha_final = window.dateEdit_fechafin.date().toString("dd.MM.yyyy")
    if window.radioButton_informediario.isChecked():
        filename_woe = 'INFORME_DIARIO'
    elif window.radioButton_otsabiertas.isChecked():
        filename_woe = 'INFORME_DIARIO_ABIERTAS'
    else:
        filename_woe = 'INFORME_DIARIO_ERRORES'
        

    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        #Elimina el texto de "Working..."
        #label_informe_diario_procesando.setText(" ")
        #label_informe_diario_procesando.adjustSize()
        return -1
    #Extrae los datos de SAP
    sap.zpm_report_mwo_id(fecha_inicio,fecha_final,cfg.PATH_INFORME_DIARIO,filename_woe)

    #Los tres tipos de informe diario son :
    #1)Informe diario Estandar
    #2)Informe de OT's abiertas
    #3)Informe de OT's con errores de reporte
    if window.radioButton_informediario.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ESTANDAR)
    if window.radioButton_otsabiertas.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ABIERTAS)
    if window.radioButton_erroresot.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ERRORES)
    #Presenta el resultado en formato HTML
    wb.open(cfg.PATH_INFORME_DIARIO + filename_woe + '.html')

    #Elimina el texto "Working..." de la interfaz de usuario.
    #label_informe_diario_procesando.setText(" ")
    #label_informe_diario_procesando.adjustSize()
#------------------------------------------------------------------------------
def showDialogYN(texto_titulo,texto_mensaje):
    """ Crear un menu dialogo con opciones de respuesta Y o N
    
    Solo hay que indicar el texto del titulo y el texto del mensaje.
    La función devuelve el boton pulsado."""
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(texto_mensaje)
    msgBox.setWindowTitle(texto_titulo)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    return msgBox.exec()
#------------------------------------------------------------------------------   
def sap_datos_hot():
    """ Extrae de SAP los historicos de Ordenes de Trabajo desde el 2020 hasta
    
    el 2022. Los distintos archivos se almacenan en PATH_EFICIENCIA_HOT."""
    
    import kpis.configuracion.config as cfg
    import kpis.sap.zpm_report_mwo as sap
    import kpis.informes.eficiencia.preparacion_datos as datos
    from datetime import datetime

    #Muestra en la interfaz de usuario el texto "Working..."
    #label_sap_datos_hot_procesando.setText("Working...")
    #label_sap_datos_hot_procesando.adjustSize()

    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        #Elimina el texto "Working...", y sale de la función actual.
        #label_sap_datos_hot_procesando.setText(" ")
        #label_sap_datos_hot_procesando.adjustSize()
        return -1

    #Fecha actual
    now=datetime.now()

    #Iteración para extraer de SAP los historicos de Sap desde el 2020 hasta la fecha
    #de hoy por trimestres.
    for x in range(2020,2022):
        for i in cfg.FECHAS_HOT[x].keys():
            if datetime.strptime(cfg.FECHAS_HOT[x][i]['DESDE'],'%d.%m.%Y') < now:
                sap.zpm_report_mwo_hot(clase_orden='',
                         fecha_entrada_desde = cfg.FECHAS_HOT[x][i]['DESDE'],
                         fecha_entrada_hasta = cfg.FECHAS_HOT[x][i]['HASTA'],
                         variante = 'APP-ODRMP-01',
                         path = cfg.PATH_EFICIENCIA_HOT,
                         file_name_woe = i)

    #Procesa todos los ficheros de historicos de OT's y devuelve un dataframe
    df=datos.procesar_allhto2df()
    #Exporta el dataframe obtenido en un fichero excel en dos ubicaciones distintas,
    #en el directorio de la APP y en el compartido KPI-SITES
    datos.df_hot2excel_app(df)
    datos.df_hot2excel_kpisites(df)

    # Elimina el texto "Working..." de la interfaz de usuario.
    #label_sap_datos_hot_procesando.setText(" ")
    #label_sap_datos_hot_procesando.adjustSize()
#------------------------------------------------------------------------------
def tiempos_produccion():
    """Extrae los tiempos de produccion del fichero manual de CALENDARIOS
    
    y genera un fichero excel con los tiempos de produccion."""
    import kpis.informes.eficiencia.preparacion_datos as datos

    # Muestra en la interfaz de usuario el texto "Working..."
    #label_tiempos_produccion_procesando.setText("Working...")
    #label_tiempos_produccion_procesando.adjustSize()

    df=datos.tiempo_prod2df()
    datos.df_tiempo_prod2excel(df)

    # Elimina el texto "Working..." de la interfaz de usuario.
    #label_tiempos_produccion_procesando.setText(" ")
    #label_tiempos_produccion_procesando.adjustSize()
#------------------------------------------------------------------------------
def actualizar_adherencia_mp():
    """
    Actualiza el KPI de Adherencia de Mantenimiento Preventivo
    """
    import kpis.informes.mp.salida_datos as mp

    mp.kpi_adh_mto()
#------------------------------------------------------------------------------
def actualizar_ratio_mp_mc():
    """
    Actualiza el KPI de Ratio MP/MC
    """
    import kpis.informes.mp.salida_datos as mp

    mp.kpi_ratio_mp_mc()
#------------------------------------------------------------------------------
def actualizar_costes():
    """Extrae de SAP los datos de costes y actualiza el archivo excel

    tanto en el directorio de la APP y en KPI-SITES."""
    import kpis.informes.costes.salida_datos
    import kpis.sap.me2k
    import kpis.sap.zps_capp
    import kpis.configuracion.config as cfg
    import pandas as pd
    from datetime import datetime

    # Muestra en la interfaz de usuario el texto "Working..."
    #label_actualizar_costes_procesando.setText("Working...")
    #label_actualizar_costes_procesando.adjustSize()

    # Fecha actual y año en curso
    now = datetime.now()
    year = now.year

    # Ventana Dialogo preguntando que tienes SAP abierto
    if (showDialogYN("AVISO", "¿ TIENES SAP-ME2K ABIERTO ?")) == QMessageBox.No:
        # Elimina el texto "Working..." de la interfaz de usuario.
        #label_actualizar_costes_procesando.setText(" ")
        #label_actualizar_costes_procesando.adjustSize()
        return -1

    # Extrae de SAP los datos de costes del año en curso y del anterior
    for year_idx in range(year - 1, year + 1):
        kpis.sap.me2k.me2k_year(year_idx)

    # Ventana Dialogo preguntando que tienes SAP abierto
    if (showDialogYN("AVISO", "¿ TIENES SAP-GRAFOS ABIERTO ?")) == QMessageBox.No:
        # Elimina el texto "Working..." de la interfaz de usuario.
        #label_actualizar_costes_procesando.setText(" ")
        #label_actualizar_costes_procesando.adjustSize()
        return -1

    # Extrae de SAP los datos de grafos del año en curso y del anterior
    for year_idx in range(year - 1, year + 1):
        kpis.sap.zps_capp.zps_capp_year(year_idx)

    # Para cada año en la iteración crea un archivo excel con el total de costes de PO
    # y grafos.
    for year_idx in range(year - 1, year + 1):
        kpis.informes.costes.salida_datos.coste_po_grafo_year(year_idx)

    # Con los archivos excel del año en curso y anterior, creados en el paso anterior,
    # crea un archivo excel con la suma de los dos, y lo almacena en dos ubicaciones
    # distintas.
    path_year_1 = cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year - 1) + '.xlsx'
    path_year = cfg.PATH_COSTES_OUTPUT + 'Datos-PO-' + str(year) + '.xlsx'
    df_year_1 = pd.read_excel(path_year_1, sheet_name='total')
    df_year = pd.read_excel(path_year, sheet_name='total')
    df_TOTAL = pd.concat([df_year_1, df_year])

    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT + 'TOTAL-COSTES-ODRM.xlsx') as output:
        df_TOTAL.to_excel(output, sheet_name='ODRM', index=False)

    with pd.ExcelWriter(cfg.PATH_COSTES_OUTPUT_KPISITES + 'TOTAL-COSTES-ODRM.xlsx') as output:
        df_TOTAL.to_excel(output, sheet_name='ODRM', index=False)

    # Elimina el texto "Working..." de la interfaz de usuario.
    #label_actualizar_costes_procesando.setText(" ")
    #label_actualizar_costes_procesando.adjustSize()
#------------------------------------------------------------------------------
def actualizar_repuestos():
    """Extrae de SAP los datos de consumos de repuestos y genera excel con todos

    los archivos que hay en el directorio de la APP."""
    import kpis.sap.me2k
    import kpis.repuestos.salida_datos
    from datetime import datetime

    # Muestra en la interfaz de usuario el texto "Working..."
    #label_actualizar_repuestos_procesando.setText("Working...")
    #label_actualizar_repuestos_procesando.adjustSize()

    # Fecha y año actual
    now = datetime.now()
    year = now.year

    # Ventana de dialogo para chequear que SAP está abierto
    if (showDialogYN("AVISO", "¿ TIENES SAP-ME2K ABIERTO ?")) == QMessageBox.Yes:
        # Extrae datos de SAP
        kpis.sap.me2k.me2k_maxr_cecos(year)
    # Procesa los archivos de repuestos, crea dataframe y exporta a excel
    kpis.repuestos.salida_datos.maxr_df2excel()

    # Elimina el texto "Working..." de la interfaz de usuario.
    #label_actualizar_repuestos_procesando.setText(" ")
    #label_actualizar_repuestos_procesando.adjustSize()
#------------------------------------------------------------------------------
""" MAIN COMIENZO DEL CODIGO PRINCIPAL DE LA APLICACION"""

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #Damos nombre a cada objeto en la app
        #Ventana principal
        #Título de la ventana
        self.setWindowTitle("APP-KPI v1.1.4")
        #Botón para salir de la app
        self.pushButton_salir.setText("Salir")
        self.pushButton_salir.clicked.connect(self.close)
        
        #Primera pestaña (Inf.Diario)
        #Título de la pestaña
        self.tabWidget_principal.setTabText(0, "Inf.Diario")
        #Etiqueta de fecha inicio
        self.label_fechainicio.setText("Fecha inicio:")
        self.dateEdit_fechainicio.setMinimumDate(QDate(2020, 1, 1))
        self.dateEdit_fechainicio.setMaximumDate(QDate(2050, 12, 31))
        self.dateEdit_fechainicio.setDate(datetime.datetime.today()-timedelta(1))
        #Etiqueta de fecha fin
        self.label_fechafin.setText("Fecha final:")
        self.dateEdit_fechafin.setMinimumDate(QDate(2020, 1, 1))
        self.dateEdit_fechafin.setMaximumDate(QDate(2050, 12, 31))
        self.dateEdit_fechafin.setDate(datetime.datetime.today())
        #Título y opciones del groupbox
        self.groupBox_tipoinforme.setTitle("Tipo informe")
        self.radioButton_informediario.setText("Informe diario")
        self.radioButton_otsabiertas.setText("OT's abiertas")
        self.radioButton_erroresot.setText("Errores OT's")
        #Botón para generar informe
        self.pushButton_generarinforme.setText("Generar informe")
        self.pushButton_generarinforme.clicked.connect(informe_diario)
        
        #Segunda pestaña (Dat.Eficiencia)
        #Título de la pestaña
        self.tabWidget_principal.setTabText(1, "Dat.Eficiencia")
        #Botón histórico OT's
        self.pushButton_saphistoricoot.setText("SAP. Datos Histórico OT's")
        self.pushButton_saphistoricoot.setToolTip('Actualiza el fichero excel HISTORICO OTS '+\
                                'con los datos bajados de SAP.')
        self.pushButton_saphistoricoot.clicked.connect(sap_datos_hot)
        #Botón tiempos de producción
        self.pushButton_tiemposproduccion.setText("Tiempos de producción") 
        self.pushButton_tiemposproduccion.setToolTip('Actualiza el fichero excel TIEMPOS '+\
                      'PRODUCCION con los datos manuales registrados en el '+\
                      'archivo CALENDARIOS.')
        self.pushButton_tiemposproduccion.clicked.connect(tiempos_produccion)

        # Tercera pestaña (Mantenimiento)
        # Título de la pestaña
        self.tabWidget_principal.setTabText(2, "MP")
        # Botón KPI adherencia MP
        self.pushButton_adherencia_mp.setText("KPI ADH MP")
        self.pushButton_adherencia_mp.setToolTip('Con los datos del fichero Historico OTs calcula el KPI de ' + \
                                                    'Adherencia de Mantenimiento Preventivo. Después ' + \
                                                    'hay que actualizar manualmente el archivo en Drive')
        self.pushButton_adherencia_mp.clicked.connect(actualizar_adherencia_mp)
        # Botón KPI Ratio MP/MC
        self.pushButton_ratio_mp_mc.setText("KPI RATIO MP/MC")
        self.pushButton_ratio_mp_mc.setToolTip('Con los datos del fichero Historico OTs calcula el KPI de ' + \
                                                 'Ratio MP/MC. Después ' + \
                                                 'hay que actualizar manualmente el archivo en Drive')
        self.pushButton_ratio_mp_mc.clicked.connect(actualizar_ratio_mp_mc)

        # Cuarta pestaña (Costes)
        # Título de la pestaña
        self.tabWidget_principal.setTabText(3, "Costes")
        # Botón actualizar costes
        self.pushButton_actualizarcostes.setText("Actualizar costes")
        self.pushButton_actualizarcostes.setToolTip('Extrae de SAP los datos de costes y '+\
                                     'actualiza el fichero de costes. Después '+\
                                     'hay que actualizar manualmente el archivo en Drive')
        self.pushButton_actualizarcostes.clicked.connect(actualizar_costes)
        # Botón actualizar repuestos
        self.pushButton_actualizarrepuestos.setText("Actualizar repuestos")
        self.pushButton_actualizarrepuestos.setToolTip('Extrae de SAP los datos de consumo '+\
                                     'de repuestos y actualiza el fichero. Después '+\
                                     'hay que actualizar manualmente el archivo en Drive')
        self.pushButton_actualizarrepuestos.clicked.connect(actualizar_repuestos)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
