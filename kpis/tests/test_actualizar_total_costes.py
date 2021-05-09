# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:02:54 2021

@author: c48142
"""
def test_actualizar_total_costes():
    """Extrae de SAP los datos de costes y actualiza el archivo excel

    tanto en el directorio de la APP y en KPI-SITES."""
    import kpis.informes.costes.salida_datos
    import kpis.sap.zps_capp
    import kpis.configuracion.config as cfg
    import pandas as pd
    from datetime import datetime

    # Fecha actual y año en curso
    now = datetime.now()
    year = now.year


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


if __name__ == '__main__':
    test_actualizar_total_costes()