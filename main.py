# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 13:11:25 2021

@author: C48142
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QGroupBox, QTabWidget, QComboBox
from PyQt5.QtCore import QDate
import datetime
from datetime import timedelta
import sys
import kpis.informes.diario.salida_datos as ids
import kpis.sap.zpm_report_mwo as sap
import kpis.configuracion.config as cfg
import webbrowser as wb

def informe_diario():
    """ Extrae los datos de sap y presenta en Chrome el Informe Diario
    
    Detallar la funcion.
    """
    #Para indicar que el proceso de Informe diario está activo, aparece en pantalla el
    #texto "Working..."
    label_informe_diario_procesando.setText("Working...")
    label_informe_diario_procesando.adjustSize()

    fecha_inicio = fecha_ini.date().toString("dd.MM.yyyy")
    fecha_final = fecha_fin.date().toString("dd.MM.yyyy")
    if radio_id_estandar.isChecked():
        filename_woe = 'INFORME_DIARIO'
    elif radio_id_abierto.isChecked():
        filename_woe = 'INFORME_DIARIO_ABIERTAS'
    else:
        filename_woe = 'INFORME_DIARIO_ERRORES'
        

    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        #Elimina el texto de "Working..."
        label_informe_diario_procesando.setText(" ")
        label_informe_diario_procesando.adjustSize()
        return -1
    #Extrae los datos de SAP
    sap.zpm_report_mwo_id(fecha_inicio,fecha_final,cfg.PATH_INFORME_DIARIO,filename_woe)

    #Los tres tipos de informe diario son :
    #1)Informe diario Estandar
    #2)Informe de OT's abiertas
    #3)Informe de OT's con errores de reporte
    if radio_id_estandar.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ESTANDAR)
    if radio_id_abierto.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ABIERTAS)
    if radio_id_error.isChecked():
        ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                             filename_woe,\
                             fecha_inicio,\
                             fecha_final,\
                             cfg.ID_ERRORES)
    #Presenta el resultado en formato HTML
    wb.open(cfg.PATH_INFORME_DIARIO + filename_woe + '.html')

    #Elimina el texto "Working..." de la interfaz de usuario.
    label_informe_diario_procesando.setText(" ")
    label_informe_diario_procesando.adjustSize()
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
    label_sap_datos_hot_procesando.setText("Working...")
    label_sap_datos_hot_procesando.adjustSize()

    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        #Elimina el texto "Working...", y sale de la función actual.
        label_sap_datos_hot_procesando.setText(" ")
        label_sap_datos_hot_procesando.adjustSize()
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
    label_sap_datos_hot_procesando.setText(" ")
    label_sap_datos_hot_procesando.adjustSize()
#------------------------------------------------------------------------------
def tiempos_produccion():
    """Extrae los tiempos de produccion del fichero manual de CALENDARIOS
    
    y genera un fichero excel con los tiempos de produccion."""
    import kpis.informes.eficiencia.preparacion_datos as datos

    # Muestra en la interfaz de usuario el texto "Working..."
    label_tiempos_produccion_procesando.setText("Working...")
    label_tiempos_produccion_procesando.adjustSize()

    df=datos.tiempo_prod2df()
    datos.df_tiempo_prod2excel(df)

    # Elimina el texto "Working..." de la interfaz de usuario.
    label_tiempos_produccion_procesando.setText(" ")
    label_tiempos_produccion_procesando.adjustSize()
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
    label_actualizar_costes_procesando.setText("Working...")
    label_actualizar_costes_procesando.adjustSize()

    # Fecha actual y año en curso
    now = datetime.now()
    year = now.year

    if (showDialogYN("AVISO", "¿ TIENES SAP-ME2K ABIERTO ?")) == QMessageBox.Yes:
        for year_idx in range(year - 1, year + 1):
            kpis.sap.me2k.me2k_year(year_idx)
    if (showDialogYN("AVISO", "¿ TIENES SAP-GRAFOS ABIERTO ?")) == QMessageBox.Yes:
        for year_idx in range(year - 1, year + 1):
            kpis.sap.zps_capp.zps_capp_year(year_idx)

    for year_idx in range(year - 1, year + 1):
        kpis.informes.costes.salida_datos.coste_po_grafo_year(year_idx)

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
    label_actualizar_costes_procesando.setText(" ")
    label_actualizar_costes_procesando.adjustSize()
#------------------------------------------------------------------------------
def actualizar_repuestos():
    """Extrae de SAP los datos de consumos de repuestos y genera excel con todos

    los archivos que hay en el directorio de la APP."""
    import kpis.sap.me2k
    import kpis.repuestos.salida_datos
    from datetime import datetime

    # Muestra en la interfaz de usuario el texto "Working..."
    label_actualizar_repuestos_procesando.setText("Working...")
    label_actualizar_repuestos_procesando.adjustSize()

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
    label_actualizar_repuestos_procesando.setText(" ")
    label_actualizar_repuestos_procesando.adjustSize()
#------------------------------------------------------------------------------
""" MAIN COMIENZO DEL CODIGO PRINCIPAL DE LA APLICACION"""
app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(400,400,500,300)
win.setWindowTitle("APP-KPI v1.0.0")

tabs = QTabWidget(win)
tabs.move(5,5)
tabs.resize(490,250)

####################### Create first tab ######################################
tab1 = QtWidgets.QWidget()
tabs.addTab(tab1, "Inf.Diario")
 
texto_fecha_ini = QtWidgets.QLabel(tab1)
texto_fecha_ini.setText("Fecha Inicio:")
texto_fecha_ini.adjustSize()
texto_fecha_ini.move(25,25)

fecha_ini = QtWidgets.QDateEdit(tab1)
fecha_ini.setMinimumDate(QDate(2020, 1, 1))
fecha_ini.setMaximumDate(QDate(2050, 12, 31))
fecha_ini.setDate(datetime.datetime.today()-timedelta(1))
fecha_ini.move(105,15)

texto_fecha_fin = QtWidgets.QLabel(tab1)
texto_fecha_fin.setText("Fecha Final :")
texto_fecha_fin.adjustSize()
texto_fecha_fin.move(25,65)

fecha_fin = QtWidgets.QDateEdit(tab1)
fecha_fin.setMinimumDate(QDate(2020, 1, 1))
fecha_fin.setMaximumDate(QDate(2050, 12, 31))
fecha_fin.setDate(datetime.datetime.today())
fecha_fin.move(105,55)

groupBox1 = QGroupBox(tab1)
groupBox1.setTitle("Tipo Informe")
groupBox1.move(25,105)
groupBox1.resize(100,100)
radio_id_estandar = QtWidgets.QRadioButton("Normal")
radio_id_abierto = QtWidgets.QRadioButton("Ot's abiertas")
radio_id_error = QtWidgets.QRadioButton("Errores Ot's")
radio_id_estandar.setChecked(True)
vbox_groupBox1 = QtWidgets.QVBoxLayout()
vbox_groupBox1.addWidget(radio_id_estandar)
vbox_groupBox1.addWidget(radio_id_abierto)
vbox_groupBox1.addWidget(radio_id_error)
vbox_groupBox1.addStretch(1)
groupBox1.setLayout(vbox_groupBox1)

button_informe_diario = QtWidgets.QPushButton(tab1)
button_informe_diario.clicked.connect(informe_diario)
button_informe_diario.setText("Informe Diario")
button_informe_diario.move(250,105)
button_informe_diario.resize(100,100)

label_informe_diario_procesando = QtWidgets.QLabel(tab1)
label_informe_diario_procesando.setText(" ")
label_informe_diario_procesando.adjustSize()
label_informe_diario_procesando.move(375,150)

####################### Crear segundo tab #####################################
tab2 = QtWidgets.QWidget()
tabs.addTab(tab2, "Dat.Eficiencia")

button_sap_datos_hot = QtWidgets.QPushButton(tab2)
button_sap_datos_hot.clicked.connect(sap_datos_hot)
button_sap_datos_hot.setText("SAP. Datos Historico OT's")
button_sap_datos_hot.setToolTip('Actualiza el fichero excel HISTORICO OTS '+\
                                'con los datos bajados de SAP.')
button_sap_datos_hot.move(25,25)
button_sap_datos_hot.resize(150,30)

label_sap_datos_hot_procesando = QtWidgets.QLabel(tab2)
label_sap_datos_hot_procesando.setText(" ")
label_sap_datos_hot_procesando.adjustSize()
label_sap_datos_hot_procesando.move(200,30)

button_tiempos_produccion = QtWidgets.QPushButton(tab2)
button_tiempos_produccion.clicked.connect(tiempos_produccion)
button_tiempos_produccion.setText("Tiempos de produccion")
button_tiempos_produccion.setToolTip('Actualiza el fichero excel TIEMPOS '+\
                      'PRODUCCION con los datos manuales registrados en el '+\
                      'archivo CALENDARIOS.')
button_tiempos_produccion.move(25,75)
button_tiempos_produccion.resize(150,30)

label_tiempos_produccion_procesando = QtWidgets.QLabel(tab2)
label_tiempos_produccion_procesando.setText(" ")
label_tiempos_produccion_procesando.adjustSize()
label_tiempos_produccion_procesando.move(200,80)

######################## Crear tercer tab #####################################
tab3 = QtWidgets.QWidget()
tabs.addTab(tab3, "Costes")

button_actualizar_costes = QtWidgets.QPushButton(tab3)
button_actualizar_costes.clicked.connect(actualizar_costes)
button_actualizar_costes.setText("Actualizar Costes")
button_actualizar_costes.setToolTip('Extrae de SAP los datos de costes y '+\
                                    'actualiza el fichero de costes. Después '+\
                                    'hay que actualizar manualmente el archivo en Drive')
button_actualizar_costes.move(25,25)
button_actualizar_costes.resize(150,30)

label_actualizar_costes_procesando = QtWidgets.QLabel(tab3)
label_actualizar_costes_procesando.setText(" ")
label_actualizar_costes_procesando.adjustSize()
label_actualizar_costes_procesando.move(200,27)

button_actualizar_repuestos = QtWidgets.QPushButton(tab3)
button_actualizar_repuestos.clicked.connect(actualizar_repuestos)
button_actualizar_repuestos.setText("Actualizar Repuestos")
button_actualizar_repuestos.setToolTip('Extrae de SAP los datos de consumo '+\
                                    'de repuestos y actualiza el fichero. Después '+\
                                    'hay que actualizar manualmente el archivo en Drive')
button_actualizar_repuestos.move(25,75)
button_actualizar_repuestos.resize(150,30)

label_actualizar_repuestos_procesando = QtWidgets.QLabel(tab3)
label_actualizar_repuestos_procesando.setText(" ")
label_actualizar_repuestos_procesando.adjustSize()
label_actualizar_repuestos_procesando.move(200,77)

###############################################################################
button_exit = QtWidgets.QPushButton(win)
button_exit.clicked.connect(win.close)
button_exit.setText("Salir")
button_exit.resize(60,30)
button_exit.move(430,260)
 
win.show()
sys.exit(app.exec_())
#------------------------------------------------------------------------------     
