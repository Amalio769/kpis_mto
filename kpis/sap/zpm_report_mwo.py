# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 18:29:45 2020

@author: C48142
"""

#-Begin------------------------------------------------------------------------

#-Includes---------------------------------------------------------------------
import sys, win32com.client
import os

#-Sub -------------------------------------------------------------------------
def zpm_report_mwo_id(fecha_desde, fecha_hasta, directorio, nombre_fichero_woe):
   """ Extrae de SAP informe con los datos necesarios para INFORME DIARIO
   
   Usa la transacción ZPM_REPORT_MWO, con los datos de fecha inicio y fecha
   final para las OT de MC y del centro emplazamiento 2013.
   Los datos los extrae a través del icono de excel situado en SAP, en la 
   ubicación pasada como parámetro y con el nombre del fichero (sin extensión)
   también pasado como parámetro.
   
   Parámetros:
   -----------
   fecha_desde : str, con el formato DD.MM.AAAA
   
   fecha_hasta : str, con el formato DD.MM.AAAA
   
   directorio  : str, path del directorio de destino del fichero
   
   nombre_fichero_woe : str, nombre del fichero sin extensión.
   """
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

      
      #session.findById("wnd[0]").maximize()
      session.findById("wnd[0]/tbar[0]/okcd").text = "ZPM_REPORT_MWO"
      session.findById("wnd[0]").sendVKey(0)
      # Check box --> Pendiente [True|False]
      session.findById("wnd[0]/usr/chkDY_OFN").selected = True
      # Check box --> En tratam. [True|False]
      session.findById("wnd[0]/usr/chkDY_IAR").selected = True
      # Check box --> Concluido [True|False]
      session.findById("wnd[0]/usr/chkDY_MAB").selected = True
      session.findById("wnd[0]/usr/ctxtAUART-LOW").text = "MC"
      session.findById("wnd[0]/usr/ctxtDATUV").text = fecha_desde
      session.findById("wnd[0]/usr/ctxtDATUB").text = fecha_hasta
      session.findById("wnd[0]/usr/ctxtSWERK-LOW").text = "2013"
      session.findById("wnd[0]/usr/ctxtSWERK-LOW").setFocus()
      session.findById("wnd[0]/usr/ctxtSWERK-LOW").caretPosition = 4
      session.findById("wnd[0]").sendVKey(0)
      session.findById("wnd[0]/tbar[1]/btn[8]").press()         # Ejecutar trans.
      session.findById("wnd[0]/tbar[1]/btn[20]").press()        # Botón fic.excel
      session.findById("wnd[1]/usr/ctxtD_RUTA").text = \
                      (directorio + nombre_fichero_woe)
      session.findById("wnd[1]/usr/ctxtD_RUTA").caretPosition = 7
      if os.path.isfile(directorio + nombre_fichero_woe + ".csv"):
         os.remove(directorio + nombre_fichero_woe + ".csv")
      session.findById("wnd[1]/usr/btnBUTTON_DESCARGA").press()
      session.findById("wnd[0]/tbar[0]/btn[15]").press()
      session.findById("wnd[0]/tbar[0]/btn[15]").press()

   except:
      print(sys.exc_info()[0])

   finally:
      session = None
      connection = None
      application = None
      SapGuiAuto = None

#------------------------------------------------------------------------------
def zpm_report_mwo_hot(clase_orden,\
                       fecha_entrada_desde,\
                       fecha_entrada_hasta,\
                       variante,\
                       path,\
                       file_name_woe):
    """Extrae de SAP los datos de Historico de Ot's para cálculos de eficiencia
    
    Detallar la información.
    """
    
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

        #session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "ZPM_REPORT_MWO"
        session.findById("wnd[0]").sendVKey(0)
        # Check box --> Pendiente [True|False]
        session.findById("wnd[0]/usr/chkDY_OFN").selected = True
        # Check box --> En tratam. [True|False]
        session.findById("wnd[0]/usr/chkDY_IAR").selected = True
        # Check box --> Concluido [True|False]
        session.findById("wnd[0]/usr/chkDY_MAB").selected = True
        # Clase Orden
        session.findById("wnd[0]/usr/ctxtAUART-LOW").text = clase_orden
        # Fecha periodo desde en blanco
        session.findById("wnd[0]/usr/ctxtDATUV").text = ""
        # Fecha periodo hasta en blanco
        session.findById("wnd[0]/usr/ctxtDATUB").text = ""
        # Fecha entrada Ot desde
        session.findById("wnd[0]/usr/ctxtERDAT-LOW").text = fecha_entrada_desde
        # Fecha entrada Ot hasta
        session.findById("wnd[0]/usr/ctxtERDAT-HIGH").text = fecha_entrada_hasta
        # Centro Emplazamiento
        session.findById("wnd[0]/usr/ctxtSWERK-LOW").text = "2013"
        # Selección Variante
        session.findById("wnd[0]/usr/ctxtVARIANT").text = variante
        session.findById("wnd[0]/usr/ctxtVARIANT").setFocus()
        session.findById("wnd[0]/usr/ctxtVARIANT").caretPosition = 12
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        session.findById("wnd[0]/mbar/menu[0]/menu[11]/menu[2]").select()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[1]/usr/ctxtRLGRAP-FILENAME").text = path + file_name_woe + '.txt'
        session.findById("wnd[1]/usr/ctxtRLGRAP-FILENAME").caretPosition = 49
        if os.path.isfile(path + file_name_woe + '.txt'):
            session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
      

    except:
        print(sys.exc_info()[0])

    finally:
        session = None
        connection = None
        application = None
        SapGuiAuto = None

#-End--------------------------------------------------------------------------