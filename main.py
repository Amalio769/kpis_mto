# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 13:45:34 2021

@author: ng6b71c

Nueva versión con GUI separada de lógica en código. @author original de la lógica c48142
"""

from main_ui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QGroupBox, QTabWidget
from PyQt5.QtCore import QDate
import datetime
from datetime import timedelta
import sys
import kpis.informes.diario.salida_datos as ids
import kpis.sap.zpm_report_mwo as sap
import kpis.configuracion.config as cfg
import webbrowser as wb

def sap_datos_hot():
    """ Extrae de SAP los historicos de Ordenes de Trabajo desde el 2020 hasta
    
    el 2022. Los distintos archivos se almacenan en PATH_EFICIENCIA_HOT."""
    
    import kpis.configuracion.config as cfg
    import kpis.sap.zpm_report_mwo as sap
    import kpis.informes.eficiencia.preparacion_datos as datos
    
    #TODO: Cambiar al QDialog del QtDesigner
    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
            return -1
          
    now=datetime.now()
    
    for x in range(2020,2022):
        for i in cfg.FECHAS_HOT[x].keys():
            if datetime.strptime(cfg.FECHAS_HOT[x][i]['DESDE'],'%d.%m.%Y')<now:
                sap.zpm_report_mwo_hot(clase_orden='',\
                         fecha_entrada_desde = cfg.FECHAS_HOT[x][i]['DESDE'],\
                         fecha_entrada_hasta = cfg.FECHAS_HOT[x][i]['HASTA'],\
                         variante = 'APP-ODRMP-01',\
                         path = cfg.PATH_EFICIENCIA_HOT,\
                         file_name_woe = i)
                
    df=datos.procesar_allhto2df()
    datos.df_hot2excel_app(df)
    datos.df_hot2excel_kpisites(df)
    
def tiempos_produccion():
    """Extra los tiempos de produccion del fichero manual de CALENDARIOS
    
    y genera un fichero excel con los tiempos de produccion."""
    import kpis.informes.eficiencia.preparacion_datos as datos

    df=datos.tiempo_prod2df()
    datos.df_tiempo_prod2excel(df)   

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

""" Extrae los datos de sap y presenta en Chrome el Informe Diario"""
def informe_diario():

    fecha_inicio = window.dateEdit_fechainicio.date().toString("dd.MM.yyyy")
    fecha_final = window.dateEdit_fechafin.date().toString("dd.MM.yyyy")
    if window.radioButton_informediario.isChecked():
        filename_woe = 'INFORME_DIARIO'
    elif window.radioButton_otsabiertas.isChecked():
        filename_woe = 'INFORME_DIARIO_ABIERTAS'
    else:
        filename_woe = 'INFORME_DIARIO_ERRORES'
        
    #TODO: meter el QDialog de Qt Designer
    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        return -1
        
    sap.zpm_report_mwo_id(fecha_inicio,fecha_final,cfg.PATH_INFORME_DIARIO,filename_woe)
        
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
    wb.open(cfg.PATH_INFORME_DIARIO + filename_woe + '.html')


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #Damos nombre a cada objeto en la app
        #Ventana principal
        #Título de la ventana
        self.setWindowTitle("APP-KPI v1.0.0")
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
        self.pushButton_saphistoricoot.clicked.connect(sap_datos_hot)
        #Botón tiempos de producción
        self.pushButton_tiemposproduccion.setText("Tiempos de producción") 
        self.pushButton_tiemposproduccion.clicked.connect(tiempos_produccion)   
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


"""
Created on Sat Jan 23 13:11:25 2021

@author: C48142
"""
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QGroupBox, QTabWidget
from PyQt5.QtCore import QDate
import datetime
from datetime import timedelta
import sys
import kpis.informes.diario.salida_datos as ids
import kpis.sap.zpm_report_mwo as sap
import kpis.configuracion.config as cfg
import webbrowser as wb

def informe_diario():

    
    fecha_inicio = fecha_ini.date().toString("dd.MM.yyyy")
    fecha_final = fecha_fin.date().toString("dd.MM.yyyy")
    if radio_id_estandar.isChecked():
        filename_woe = 'INFORME_DIARIO'
    elif radio_id_abierto.isChecked():
        filename_woe = 'INFORME_DIARIO_ABIERTAS'
    else:
        filename_woe = 'INFORME_DIARIO_ERRORES'
        

    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
        return -1
    sap.zpm_report_mwo_id(fecha_inicio,fecha_final,cfg.PATH_INFORME_DIARIO,filename_woe)
        
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
    wb.open(cfg.PATH_INFORME_DIARIO + filename_woe + '.html')
#------------------------------------------------------------------------------
def showDialogYN(texto_titulo,texto_mensaje):

    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(texto_mensaje)
    msgBox.setWindowTitle(texto_titulo)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    return msgBox.exec()
#------------------------------------------------------------------------------   
def sap_datos_hot():

    
    import kpis.configuracion.config as cfg
    import kpis.sap.zpm_report_mwo as sap
    import kpis.informes.eficiencia.preparacion_datos as datos
    from datetime import datetime
    
    if(showDialogYN("AVISO","¿ TIENES SAP ABIERTO ?")) == QMessageBox.No:
            return -1
          
    now=datetime.now()
    
    for x in range(2020,2022):
        for i in cfg.FECHAS_HOT[x].keys():
            if datetime.strptime(cfg.FECHAS_HOT[x][i]['DESDE'],'%d.%m.%Y')<now:
                sap.zpm_report_mwo_hot(clase_orden='',\
                         fecha_entrada_desde = cfg.FECHAS_HOT[x][i]['DESDE'],\
                         fecha_entrada_hasta = cfg.FECHAS_HOT[x][i]['HASTA'],\
                         variante = 'APP-ODRMP-01',\
                         path = cfg.PATH_EFICIENCIA_HOT,\
                         file_name_woe = i)
                
    df=datos.procesar_allhto2df()
    datos.df_hot2excel_app(df)
    datos.df_hot2excel_kpisites(df)
#------------------------------------------------------------------------------
def tiempos_produccion():

    import kpis.informes.eficiencia.preparacion_datos as datos

    df=datos.tiempo_prod2df()
    datos.df_tiempo_prod2excel(df)   
#------------------------------------------------------------------------------ 

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(400,400,500,300)
win.setWindowTitle("APP-KPI v0.1.3")

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

#groupBox2 = QGroupBox(tab1)
#groupBox2.setTitle("Opciones")
#groupBox2.move(130,105)
#groupBox2.resize(100,100)
#radio_id_sap = QtWidgets.QRadioButton("SAP + Rep.")
#radio_id_reporte = QtWidgets.QRadioButton("Solo Rep.")
#radio_id_sap.setChecked(True)
#vbox_groupBox2 = QtWidgets.QVBoxLayout()
#vbox_groupBox2.addWidget(radio_id_sap)
#vbox_groupBox2.addWidget(radio_id_reporte)
#vbox_groupBox2.addStretch(1)
#groupBox2.setLayout(vbox_groupBox2)

button_informe_diario = QtWidgets.QPushButton(tab1)
button_informe_diario.clicked.connect(informe_diario)
button_informe_diario.setText("Informe Diario")
button_informe_diario.move(250,105)
button_informe_diario.resize(100,100)

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

button_tiempos_produccion = QtWidgets.QPushButton(tab2)
button_tiempos_produccion.clicked.connect(tiempos_produccion)
button_tiempos_produccion.setText("Tiempos de produccion")
button_tiempos_produccion.setToolTip('Actualiza el fichero excel TIEMPOS '+\
                      'PRODUCCION con los datos manuales registrados en el '+\
                      'archivo CALENDARIOS.')
button_tiempos_produccion.move(25,75)
button_tiempos_produccion.resize(150,30)
######################## Crear tercer tab #####################################
tab3 = QtWidgets.QWidget()
tabs.addTab(tab3, "Costes")

###############################################################################
button_exit = QtWidgets.QPushButton(win)
button_exit.clicked.connect(win.close)
button_exit.setText("Salir")
button_exit.resize(60,30)
button_exit.move(430,260)
 
win.show()
sys.exit(app.exec_())
#------------------------------------------------------------------------------     
"""