# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 07:44:50 2020

@author: C48142
"""

def main():
    import kpis.informes.diario.salida_datos as ids
    import kpis.sap.zpm_report_mwo as sap
    import kpis.configuracion.config as cfg
    import webbrowser as wb
    
    FECHA_INI = "01.1.2021"
    FECHA_FIN = "26.1.2021"
    #sap.zpm_report_mwo_id(FECHA_INI,FECHA_FIN,cfg.PATH_INFORME_DIARIO,"INFORME_DIARIO")
    filename_woe = "INFORME_DIARIO_ERRORES"
    ids.procesar_informe(cfg.PATH_INFORME_DIARIO,\
                         filename_woe,\
                         FECHA_INI,\
                         FECHA_FIN,\
                         cfg.ID_ERRORES)
    wb.open(cfg.PATH_INFORME_DIARIO + filename_woe + '.html')
    
if __name__ == '__main__':
    main()
else:
    print("Ha ocurrido un error.")