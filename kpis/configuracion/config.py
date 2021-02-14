# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 06:56:38 2020

@author: C48142
"""
import os

contenido=os.listdir("G://")
for i in contenido:
  if i.startswith('Unidades'):
      path_g = i


PATH_APP = "G://" + path_g
PATH_CONFIGURACION_APP = PATH_APP + "/APP-KPIs/CONFIGURACION/"
PATH_INFORME_DIARIO = PATH_APP + "/APP-KPIs/INFORME-DIARIO/"
PATH_COSTES_CECO = PATH_APP + "/APP-KPIs/COSTES/CECO/"
PATH_COSTES_CONFIGURACION = PATH_APP + "/APP-KPIs/COSTES/CONFIGURACION/"
PATH_COSTES_ORDEN = PATH_APP + "/APP-KPIs/COSTES/ORDEN/"
PATH_COSTES_OUTPUT = PATH_APP + "/APP-KPIs/COSTES/OUTPUT/"
PATH_COSTES_OUTPUT_KPISITES = PATH_APP + "/ODRMP - MANTENIMIENTO PRODUCTIVO/11 - KPI-SITES/COSTES/"
PATH_COSTES_PEP = PATH_APP + "/APP-KPIs/COSTES/PEP/"
PATH_COSTES_GRAFOS = PATH_APP + "/APP-KPIs/COSTES/GRAFOS/"
PATH_EFICIENCIA_HOT = PATH_APP + "/APP-KPIs/EFICIENCIA-HISTORICO-OT/"
PATH_TIEMPO_PRODUCCION = PATH_APP + "/APP-KPIs/TIEMPO-PRODUCCION/"
PATH_KPI_SITES_HOT = PATH_APP + "/ODRMP - MANTENIMIENTO PRODUCTIVO/11 - KPI-SITES/HISTORICO OTs/"
PATH_KPI_SITES_TPO_PRODUCCION = PATH_APP + "/ODRMP - MANTENIMIENTO PRODUCTIVO/11 - KPI-SITES/TIEMPOS PRODUCCION/"

CABECERA_TXT_HOT = "|  Cl.|T.Trabajo|Orden  |Ubicación técnica           |Denominación objeto                     |Equipo |Fe.entrada|Inic.extr.|Fin extr. |F.Cierre T|Texto breve                             |Status sistema                    |Status usuario     |Pl.MantPrv  |  Sum CPLA|Sum PSUP|  Sum PMAT| Suma PAIR|   Sum ...|Tiempo Res|H. parada| Tiem Tota|Trbjo real|Fallo   |Problema                                |Cód. cat.|Ce.coste|Denom.ubic.técnica                      |Fecha ref.|F.Cier Com|Inicio    |Inic.real |Fin real  |Liber.    |Fin progr.|Fin real|CGH|GrpHRuta|Hist. dsd |H.Cier Com|HoraCierrT|HoraFinExt|Fin (hora)|Hora inic.|HoraRef |H. inicio|Hora inic.|In.real |Hr. crea|Inic.prog.|Pos.PM|"
CABECERA_TXT_GRAFOS ="|ceco|num_empleado|nombre_empleado|fecha|denominacion_operacion|denominacion_grafo|denominacion_pep|horas|grafo|pep|"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
# Parametro para seleccionar tipo de reporte Informe Diario
ID_ESTANDAR = 1
ID_ABIERTAS = 2
ID_ERRORES  = 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
PROGRAMAS = ['A320','A330','A350','A380','PINT','SAUX','EXPE']
STATUS_OT = ['CPLA','PMAT','PSUP','...','PAIR','CACL','CERR','SUPE','CTEC',\
             'KKMP','NLIQ','NOTP','LIBE','IMPR','DMNV','MOVM','RECH','NEJE']

FECHAS_HOT = {
              2019 :{
                     '2019-Q1':{
                                'DESDE':'01.01.2019',
                                'HASTA':'31.03.2019'},
                     '2019-Q2':{
                                'DESDE':'01.04.2019',
                                'HASTA':'30.06.2019'},
                     '2019-Q3':{
                                'DESDE':'01.07.2019',
                                'HASTA':'30.09.2019'},
                     '2019-Q4':{
                                'DESDE':'01.10.2019',
                                'HASTA':'31.12.2019'}},
              2020 :{
                     '2020-Q1':{
                                'DESDE':'01.01.2020',
                                'HASTA':'31.03.2020'},
                     '2020-Q2':{
                                'DESDE':'01.04.2020',
                                'HASTA':'30.06.2020'},
                     '2020-Q3':{
                                'DESDE':'01.07.2020',
                                'HASTA':'30.09.2020'},
                     '2020-Q4':{
                                'DESDE':'01.10.2020',
                                'HASTA':'31.12.2020'}},
              2021 :{
                     '2021-Q1':{
                                'DESDE':'01.01.2021',
                                'HASTA':'31.03.2021'},
                     '2021-Q2':{
                                'DESDE':'01.04.2021',
                                'HASTA':'30.06.2021'},
                     '2021-Q3':{
                                'DESDE':'01.07.2021',
                                'HASTA':'30.09.2021'},
                     '2021-Q4':{
                                'DESDE':'01.10.2021',
                                'HASTA':'31.12.2021'}},
              2022 :{
                     '2022-Q1':{
                                'DESDE':'01.01.2022',
                                'HASTA':'31.03.2022'},
                     '2022-Q2':{
                                'DESDE':'01.04.2022',
                                'HASTA':'30.06.2022'},
                     '2022-Q3':{
                                'DESDE':'01.07.2022',
                                'HASTA':'30.09.2022'},
                     '2022-Q4':{
                                'DESDE':'01.10.2022',
                                'HASTA':'31.12.2022'}}                         
              }
NOMBRE_COLUMNAS_ZPM_HTO = {
                            'Cl.':'clase_orden',
                            'T.Trabajo':'tipo_trabajo',
                            'Orden':'orden',
                            'Ubicación técnica':'ubicacion_tecnica',
                            'Denominación objeto':'denominacion_objeto',
                            'Equipo':'equipo',
                            'Fe.entrada':'fecha_entrada',
                            'Inic.extr.':'fecha_inicio_extrema',
                            'Fin extr.':'fecha_fin_extrema',
                            'F.Cierre T':'fecha_cierre_tecnico',
                            'Texto breve':'texto_breve',
                            'Status sistema':'status_sistema',
                            'Status usuario':'status_usuario',
                            'Pl.MantPrv':'plan_mto_preventivo',
                            'Sum CPLA':'sum_cpla',
                            'Sum PSUP':'sum_psup',
                            'Sum PMAT':'sum_pmat',
                            'Suma PAIR':'sum_pair',
                            'Sum ...':'tiempo_resolucion',
                            'Tiempo Res':'tiempo_respuesta',
                            'H. parada':'tiempo_parada',
                            'Tiem Tota':'tiempo_total',
                            'Trbjo real':'trabajo_real',
                            'Fallo':'fallo',
                            'Problema':'problema',
                            'Cód. cat.':'cod_cat_fallo',
                            'Ce.coste':'ceco',
                            'Denom.ubic.técnica':'denominacion_ubicacion_tecnica',
                            'Fecha ref.':'fecha_referencia',
                            'F.Cier Com':'fecha_cierre_comercial',
                            'Inicio':'fecha_inicio',
                            'Inic.real':'fecha_inicio_real',
                            'Fin real':'fecha_fin_real',
                            'Liber.':'fecha_liberacion',
                            'Fin progr.':'fecha_fin_programado',
                            'Fin real.1':'hora_fin_real',
                            'CGH':'contador_grupo_hruta',
                            'GrpHRuta':'grphruta',
                            'Hist. dsd':'fecha_historico_desde',
                            'H.Cier Com':'hora_cierre_comercial',
                            'HoraCierrT':'hora_cierre_tecnico',
                            'HoraFinExt':'hora_fin_extrema',
                            'Fin (hora)':'hora_fin_programacion',
                            'Hora inic.':'hora_inicio_programacion',
                            'HoraRef':'hora_referencia',
                            'H. inicio':'hora_inicio',
                            'Hora inic..1':'hora_inicio_extrema',
                            'In.real':'hora_inicio_real',
                            'Hr. crea':'hora_creacion',
                            'Inic.prog.':'fecha_inicio_programado',
                            'Pos.PM':'posicion_mantenimiento'}

# Plantilla HTML para INFORME DIARIO
HTML_ID={'CABECERA': """<!DOCTYPE html>
                    <html>
                    <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    th, td {
                      padding: 5px;
                      text-align: center;
                    }
                    h2, img {
                      font-size: 30px;
                      text-align: center;
                      display: inline-block;
                    }
                    @media print {
                       @page {
                          size:landscape;
                          margin: 1;
                        }
                    }
                    </style>
                    </head>
                    <body>
                    <h2><img style="width: 10%"; src="{PATH_LOGO}AIRBUS_Blue.png"></img>ZPM_REPORT_MWO PUERTO REAL</h2>
                    <h3>Informe {TIPO_REPORTE} Desde: {FECHA_INI}  Hasta: {FECHA_FIN}</h3>
                    <table style="width:100%">""",
        'TABLA'   : """
                      <tr>
                        <td style="color:{COLOR_GENERAL}">{01}</td>
                        <td style="color:{COLOR_GENERAL}">{02}</td>
                        <td style="color:{COLOR_GENERAL}">{03}</td>
                        <td rowspan="3", style="color:{COLOR_GENERAL}">{04}</td>
                        <td colspan="2", style="color:{COLOR_GENERAL}">{05}</td>
                        <td style="color:{COLOR_GENERAL}">{07}</td>
                        <td style="color:{COLOR_GENERAL}">{08}</td>
                        <td style="color:{COLOR_GENERAL}">{09}</td>
                        <td style="color:{COLOR_GENERAL}">{010}</td>
                        <td style="color:{COLOR_GENERAL}">{011}</td>
                      </tr>
                      <tr>
                        <td rowspan="2", style="font-size: 30px; color:{COLOR_TIPO_TRABAJO}">{11}</td>
                        <td rowspan="2", style="color:{COLOR_GENERAL}">{12}</td>
                        <td rowspan="3", style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{13}</td>
                        <td style="color:{COLOR_GENERAL}">{15}</td>
                        <td style="color:{COLOR_GENERAL}">{16}</td>
                        <td rowspan="3", style="font-size: 30px; color:{COLOR_HORA_PARADA}; border-bottom: 4px solid #000">{17}</td>
                        <td style="color:{COLOR_GENERAL}">{18}</td>
                        <td style="color:{COLOR_GENERAL}">{19}</td>
                        <td style="color:{COLOR_GENERAL}">{110}</td>
                        <td style="color:{COLOR_GENERAL}">{111}</td>
                      </tr>
                      <tr>
                        <td style="color:{COLOR_GENERAL}">{25}</td>
                        <td style="color:{COLOR_GENERAL}">{26}</td>
                        <td style="color:{COLOR_GENERAL}">{28}</td>
                        <td style="color:{COLOR_GENERAL}">{29}</td>
                        <td style="color:{COLOR_GENERAL}">{210}</td>
                        <td style="color:{COLOR_GENERAL}">{211}</td>
                      </tr>
                      <tr>
                        <td colspan="2", style="color:{COLOR_PROBLEMA}; border-bottom: 4px solid #000">{31}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{34}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{35}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{36}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{38}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{39}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{310}</td>
                        <td style="border-bottom: 4px solid #000; color:{COLOR_GENERAL}">{311}</td>
                      </tr>""",
         'PIE'     : """
                    </table>           
                    </body>
                    </html>"""}