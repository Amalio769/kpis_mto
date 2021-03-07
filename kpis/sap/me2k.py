# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 19:25:16 2020

@author: C48142
"""

#-Begin-----------------------------------------------------------------

#-Includes--------------------------------------------------------------
import sys, win32com.client
import os
from datetime import date
import kpis.configuracion.config as cfg

#-Sub ------------------------------------------------------------------
def me2k(year="", ceco="", pep="", orden="", centro="2013",\
         fecha_entrega_desde="",fecha_entrega_hasta="",\
         fecha_documento_desde="", fecha_documento_hasta=""):
   """ Transacción ME2K para el PEP solicitado
   
   Usa la transacción ME2K, con los datos de year, ceco, pep, orden, centro,
   fecha_entrega_desde, fecha_entrega_hasta, fecha_documento_desde y 
   fecha_documento_hasta para las PO con los parámetros indicados.
   Al menos hay que indicar un Pep/Ceco/Orden, ya que en caso contrario
   habría un error.
   
   Parámetros:
   -----------
   year        : int, año
   ceco        : str, nombre del ceco
   pep         : str, nombre del pep
   orden       : str, nombre de la orden
   centro      : str, por defecto 2013 (Puerto Real)
   fecha_entrega_desde: str, con el formato DD.MM.AAAA
   fecha_entrega_hasta: str, con el formato DD.MM.AAAA
   fecha_docuento_desde : str, con el formato DD.MM.AAAA
   fecha_documento_hasta : str, con el formato DD.MM.AAAA
   """
   
   today = date.today()
   if year=="":
       year=format(today.year)
   if ceco != "":
       pep = ""
       orden = ""
       path = cfg.PATH_COSTES_CECO
   if pep != "":
       ceco = ""
       orden = ""
       path = cfg.PATH_COSTES_PEP
   if orden != "":
       ceco = ""
       pep = ""
       path = cfg.PATH_COSTES_ORDEN
   file_name=str(year) + '-' + \
                (ceco + pep + orden).replace('/','-') + '.txt'
   if fecha_entrega_desde == "":
       fecha_entrega_desde="01.01." + str(year)
   if fecha_entrega_hasta == "":
       fecha_entrega_hasta="31.12." + str(year)
   if fecha_documento_desde == "":
       fecha_documento_desde="01.10." + str(year - 1)
   if fecha_documento_hasta == "":
       fecha_documento_hasta="31.12." + str(year)
       
   if ceco=="" and pep=="" and orden=="":
      sys.exit("Error. Hay que elegir al menos un parámetro entre ceco, pep"+ \
               " y orden")
   
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
      session.findById("wnd[0]/tbar[0]/okcd").text = "ME2K"
      session.findById("wnd[0]").sendVKey(0)
      session.findById("wnd[0]/usr/ctxtEK_KOSTL-LOW").text = ceco
      session.findById("wnd[0]/usr/ctxtEK_PROJN").text = pep
      session.findById("wnd[0]/usr/ctxtEK_AUFNR-LOW").text = orden
      session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = centro
      session.findById("wnd[0]/usr/ctxtS_EINDT-LOW").text = fecha_entrega_desde
      session.findById("wnd[0]/usr/ctxtS_EINDT-HIGH").text = fecha_entrega_hasta
      session.findById("wnd[0]/usr/ctxtS_BEDAT-LOW").text = fecha_documento_desde
      session.findById("wnd[0]/usr/ctxtS_BEDAT-HIGH").text = fecha_documento_hasta
      session.findById("wnd[0]/tbar[1]/btn[8]").press()
      session.findById("wnd[0]/mbar/menu[4]/menu[5]/menu[2]/menu[2]").select()
      session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[1]/usr/ctxtRLGRAP-FILENAME").text= path + file_name
      if os.path.isfile(path + file_name):
          session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[1]/tbar[0]/btn[0]").press()
      session.findById("wnd[0]/tbar[0]/btn[15]").press()      


#   except:
#      print(sys.exc_info()[0])
      
   except BaseException as e: #to catch pywintypes.error
       if e.args[0] == -2147221020:
           print("No hay sesion de SAP abierta")
       elif e.args[0] == -2147352567:
           print("No existen datos para: ",ceco, orden, pep)
           if session.ActiveWindow.Name == "wnd[1]":
               session.findById("wnd[1]/tbar[0]/btn[0]").press()
           session.findById("wnd[0]/tbar[0]/btn[15]").press()

       else:
           print("Error desconocido en funcion me2k(): ", e.args[0] )

   finally:
      session = None
      connection = None
      application = None
      SapGuiAuto = None


#-Sub ------------------------------------------------------------------
def me2k_year(year):
    """ Iteracion de ME2K para la configuracion de costes-year
    
    describe
    """
    import kpis.configuracion.config as cfg
    import pandas as pd

    df_ceco = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='ceco')
    for row in df_ceco.itertuples():
        me2k(year,\
             ceco = str(row.ceco),\
             fecha_entrega_desde = '01.01.' + str(year),\
             fecha_entrega_hasta = '31.12.' + str(year),\
             fecha_documento_desde = '01.10.' + str(year - 1),\
             fecha_documento_hasta = '31.12.' + str(year))

    df_orden = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='orden')
    for row in df_orden.itertuples():
        me2k(year,\
             orden = str(row.orden),\
             fecha_entrega_desde = '01.01.' + str(year),\
             fecha_entrega_hasta = '31.12.' + str(year),\
             fecha_documento_desde = '01.10.' + str(year - 1),\
             fecha_documento_hasta = '31.12.' + str(year))

    df_pep = pd.read_excel(cfg.PATH_COSTES_CONFIGURACION + str(year) + '.xlsx', sheet_name='pep')
    for row in df_pep.itertuples():
        me2k(year,\
             pep = str(row.pep),\
             fecha_entrega_desde = '01.01.' + str(year),\
             fecha_entrega_hasta = '31.12.' + str(year),\
             fecha_documento_desde = '01.10.' + str(year - 1),\
             fecha_documento_hasta = '31.12.' + str(year))
    
# -Sub ------------------------------------------------------------------
def me2k_maxr(year,ceco):
    """ Transacción ME2K para obtener los pedidos MAXR del año solicitado

    Usa la transacción ME2K, con el dato de year, para obtener los pedidos
    MAXR de los CECOS: 301, 602, 455, 475, 485, 495, 497, 510 Y 215, entre
    las fechas del 01.01.year al 31.12.year.

    Parámetros:
    -----------
    year        : int, año
    """

    path = cfg.PATH_REPUESTOS_MAXR
    file_name = str(year) + '-' + ceco + '-MAXR.txt'
    fecha_documento_desde = "01.01." + str(year)
    fecha_documento_hasta = "31.12." + str(year)

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

        # session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "ME2K"
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/usr/ctxtEK_KOSTL-LOW").text = ceco
        session.findById("wnd[0]/usr/ctxtEK_PROJN").text = ""
        session.findById("wnd[0]/usr/ctxtEK_AUFNR-LOW").text = ""
        session.findById("wnd[0]/usr/ctxtS_WERKS-LOW").text = "2013"
        session.findById("wnd[0]/usr/ctxtLISTU").text = "BEST"
        session.findById("wnd[0]/usr/ctxtS_BSART-LOW").text = "MAXR"
        session.findById("wnd[0]/usr/ctxtS_BEDAT-LOW").text = fecha_documento_desde
        session.findById("wnd[0]/usr/ctxtS_BEDAT-HIGH").text = fecha_documento_hasta
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        session.findById("wnd[0]/mbar/menu[4]/menu[5]/menu[2]/menu[2]").select()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[1]/usr/ctxtRLGRAP-FILENAME").text = path + file_name
        if os.path.isfile(path + file_name):
            session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()


    except BaseException as e:  # to catch pywintypes.error
        if e.args[0] == -2147221020:
            print("No hay sesion de SAP abierta")
        elif e.args[0] == -2147352567:
            print("No existen datos para: ", ceco)
            if session.ActiveWindow.Name == "wnd[1]":
                session.findById("wnd[1]/tbar[0]/btn[0]").press()
            session.findById("wnd[0]/tbar[0]/btn[15]").press()

        else:
            print("Error desconocido en funcion me2k(): ", e.args[0])

    finally:
        session = None
        connection = None
        application = None
        SapGuiAuto = None


# -Sub ------------------------------------------------------------------
def me2k_maxr_cecos(year):
    """ Iteracion de ME2K-MAXR para un listado de cecos predetirminados

    y el año indicado.
    """
    import kpis.configuracion.config as cfg
    import pandas as pd

    cecos = ['13301410',
             '13455410',
             '13602410',
             '13475410',
             '13485410',
             '13495410',
             '13497410',
             '13510410',
             '13211410',
             '13215410']

    for _ceco in cecos:
        me2k_maxr(year,_ceco)

