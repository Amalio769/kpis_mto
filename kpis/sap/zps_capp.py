# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:25:29 2021

@author: C48142
"""

#-Includes--------------------------------------------------------------
import sys, win32com.client
import os
import kpis.configuracion.config as cfg


#-Sub ------------------------------------------------------------------
def zps_capp(year, ceco="", grafo="", centro="2013",num_personal="",\
         fecha_desde="",fecha_hasta="",):
   """ Transacción ZPS_CAPP para las imputaciones de horas aprobadas
   
   Detallar la función
   """
   

   path = cfg.PATH_COSTES_GRAFOS
   file_name=str(year) + '-' + ceco + '.txt'
   if fecha_desde == "":
       fecha_desde="01.01." + str(year)
   if fecha_hasta == "":
       fecha_hasta="31.12." + str(year)

       
#   if ceco=="" and pep=="" and orden=="":
#      sys.exit("Error. Hay que elegir al menos un parámetro entre ceco, pep"+ \
#               " y orden")
   
   try:

      SapGuiAuto = win32com.client.GetObject("SAPGUI")
      if not type(SapGuiAuto) == win32com.client.CDispatch:
         return

      application = SapGuiAuto.GetScriptingEngine
      if not type(application) == win32com.client.CDispatch:
         SapGuiAuto = None
         return

      connection = application.Children(0)
      if not type(connection) == win32com.client.CDispatch:
         application = None
         SapGuiAuto = None
         return

      session = connection.Children(0)
      if not type(session) == win32com.client.CDispatch:
         connection = None
         application = None
         SapGuiAuto = None
         return



#      session.findById("wnd[0]").maximize()
      session.findById("wnd[0]/tbar[0]/okcd").text = "ZPS_CAPP"
      session.findById("wnd[0]").sendVKey(0)
      session.findById("wnd[0]/usr/ctxtSO_PERS-LOW").text = "12345678"
      session.findById("wnd[0]/usr/ctxtSO_PERS-LOW").text = ""
      session.findById("wnd[0]/usr/ctxtSO_PERS-LOW").text = num_personal
      # Pulsa el boton todos los parametros
      session.findById("wnd[0]/tbar[1]/btn[27]").press()
      session.findById("wnd[0]/usr/radANDZEIT").select()
      session.findById("wnd[0]/usr/ctxtSO_STATU-LOW").text = "30"
      session.findById("wnd[0]/usr/ctxtSO_PERS-LOW").setfocus()

      session.findById("wnd[0]/usr/ctxtSO_DATUM-LOW").text = fecha_desde
      session.findById("wnd[0]/usr/ctxtSO_DATUM-HIGH").text = fecha_hasta
      session.findById("wnd[0]/usr/ctxtSO_SKOSL-LOW").text = ceco
      session.findById("wnd[0]/usr/ctxtSO_WERKS-LOW").text = "2013"
      session.findById("wnd[0]/usr/ctxtVARIANT").text = "GRF-APP-KPI"
#      session.findById("wnd[0]/usr/ctxtVARIANT").setFocus
#      session.findById("wnd[0]/usr/ctxtVARIANT").caretPosition = 11
      session.findById("wnd[0]/tbar[1]/btn[8]").press()
      session.findById("wnd[0]/mbar/menu[0]/menu[1]/menu[2]").select()
      session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[1]/usr/ctxtRLGRAP-FILENAME").text= path + file_name
      if os.path.isfile(path + file_name):
          session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[0]/tbar[0]/btn[15]").press()
      session.findById("wnd[0]/tbar[0]/btn[15]").press()

#   except:
#      print(sys.exc_info()[0])
#      print("Esta fallando aqui")
   except BaseException as e: #to catch pywintypes.error
       if e.args[0] == -2147221020:
           print("No hay sesion de SAP abierta")
       elif e.args[0] == -2147352567:
           print("No existen datos")
           if session.ActiveWindow.Name == "wnd[1]":
               session.findById("wnd[1]/tbar[0]/btn[0]").press()
           session.findById("wnd[0]/tbar[0]/btn[15]").press()
       else:
           print("Error desconocido en funcion zps_capp(): ", e.args[0] )

   finally:
      session = None
      connection = None
      application = None
      SapGuiAuto = None
#-Sub ------------------------------------------------------------------
def zps_capp_year(year):
    """ Iteracion de ZPS_CAPP para la configuracion de costes-year
    
    describe
    """
    import kpis.configuracion.config as cfg
    
  
    with open(cfg.PATH_COSTES_CONFIGURACION + str(year) + '-CECO-GRAFO.txt') as f:
        for linea in f:
            zps_capp(year, ceco = linea.rstrip())
    
#-Main------------------------------------------------------------------

#-End-------------------------------------------------------------------

