# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 366)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget_principal = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_principal.setGeometry(QtCore.QRect(10, 10, 401, 281))
        self.tabWidget_principal.setObjectName("tabWidget_principal")
        self.tab_informediario = QtWidgets.QWidget()
        self.tab_informediario.setObjectName("tab_informediario")
        self.label_fechainicio = QtWidgets.QLabel(self.tab_informediario)
        self.label_fechainicio.setGeometry(QtCore.QRect(20, 20, 71, 21))
        self.label_fechainicio.setObjectName("label_fechainicio")
        self.groupBox_tipoinforme = QtWidgets.QGroupBox(self.tab_informediario)
        self.groupBox_tipoinforme.setGeometry(QtCore.QRect(50, 120, 131, 111))
        self.groupBox_tipoinforme.setObjectName("groupBox_tipoinforme")
        self.radioButton_otsabiertas = QtWidgets.QRadioButton(self.groupBox_tipoinforme)
        self.radioButton_otsabiertas.setGeometry(QtCore.QRect(20, 50, 101, 18))
        self.radioButton_otsabiertas.setObjectName("radioButton_otsabiertas")
        self.radioButton_erroresot = QtWidgets.QRadioButton(self.groupBox_tipoinforme)
        self.radioButton_erroresot.setGeometry(QtCore.QRect(20, 80, 101, 18))
        self.radioButton_erroresot.setObjectName("radioButton_erroresot")
        self.radioButton_informediario = QtWidgets.QRadioButton(self.groupBox_tipoinforme)
        self.radioButton_informediario.setGeometry(QtCore.QRect(20, 20, 101, 18))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_informediario.sizePolicy().hasHeightForWidth())
        self.radioButton_informediario.setSizePolicy(sizePolicy)
        self.radioButton_informediario.setObjectName("radioButton_informediario")
        self.pushButton_generarinforme = QtWidgets.QPushButton(self.tab_informediario)
        self.pushButton_generarinforme.setGeometry(QtCore.QRect(230, 150, 121, 61))
        self.pushButton_generarinforme.setObjectName("pushButton_generarinforme")
        self.dateEdit_fechainicio = QtWidgets.QDateEdit(self.tab_informediario)
        self.dateEdit_fechainicio.setGeometry(QtCore.QRect(100, 20, 121, 21))
        self.dateEdit_fechainicio.setObjectName("dateEdit_fechainicio")
        self.dateEdit_fechafin = QtWidgets.QDateEdit(self.tab_informediario)
        self.dateEdit_fechafin.setGeometry(QtCore.QRect(100, 60, 121, 21))
        self.dateEdit_fechafin.setObjectName("dateEdit_fechafin")
        self.label_fechafin = QtWidgets.QLabel(self.tab_informediario)
        self.label_fechafin.setGeometry(QtCore.QRect(20, 60, 71, 21))
        self.label_fechafin.setObjectName("label_fechafin")
        self.tabWidget_principal.addTab(self.tab_informediario, "")
        self.tab_datoseficiencia = QtWidgets.QWidget()
        self.tab_datoseficiencia.setObjectName("tab_datoseficiencia")
        self.pushButton_saphistoricoot = QtWidgets.QPushButton(self.tab_datoseficiencia)
        self.pushButton_saphistoricoot.setGeometry(QtCore.QRect(20, 30, 361, 31))
        self.pushButton_saphistoricoot.setObjectName("pushButton_saphistoricoot")
        self.pushButton_tiemposproduccion = QtWidgets.QPushButton(self.tab_datoseficiencia)
        self.pushButton_tiemposproduccion.setGeometry(QtCore.QRect(20, 80, 361, 31))
        self.pushButton_tiemposproduccion.setObjectName("pushButton_tiemposproduccion")
        self.tabWidget_principal.addTab(self.tab_datoseficiencia, "")
        self.tab_costes = QtWidgets.QWidget()
        self.tab_costes.setObjectName("tab_costes")
        self.tabWidget_principal.addTab(self.tab_costes, "")
        self.pushButton_salir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_salir.setGeometry(QtCore.QRect(330, 300, 75, 23))
        self.pushButton_salir.setObjectName("pushButton_salir")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_principal.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_fechainicio.setText(_translate("MainWindow", "TextLabel"))
        self.groupBox_tipoinforme.setTitle(_translate("MainWindow", "GroupBox"))
        self.radioButton_otsabiertas.setText(_translate("MainWindow", "RadioButton"))
        self.radioButton_erroresot.setText(_translate("MainWindow", "RadioButton"))
        self.radioButton_informediario.setText(_translate("MainWindow", "RadioButton"))
        self.pushButton_generarinforme.setText(_translate("MainWindow", "PushButton"))
        self.label_fechafin.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget_principal.setTabText(self.tabWidget_principal.indexOf(self.tab_informediario), _translate("MainWindow", "Tab 1"))
        self.pushButton_saphistoricoot.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_tiemposproduccion.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget_principal.setTabText(self.tabWidget_principal.indexOf(self.tab_datoseficiencia), _translate("MainWindow", "Tab 2"))
        self.tabWidget_principal.setTabText(self.tabWidget_principal.indexOf(self.tab_costes), _translate("MainWindow", "Page"))
        self.pushButton_salir.setText(_translate("MainWindow", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

