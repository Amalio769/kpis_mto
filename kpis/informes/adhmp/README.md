* Utilizar los datos extraidos en historico de Ot's, ya que contienen todas las columnas necesarias para los kpi's de adherencia de mto.
* A los datos anteriores hay que hacerles un filtro para solo obtener las Ot's tipo MP
* De historico Ot's seleccionar exclusivamente las siguientes columnas:
    Orden
    Clase OT
    Tipo Trabajo
    U. Técnica
    Denominación U.Tecnica
    Equipo
    Denominación Equipo
    Texto Breve
    Fecha referencia
    Fecha entrada
    Fecha Inicio Extremo
    Fecha Fin Extremo
    Fecha Liberada
    Fecha Inicio Programado
    Fecha Fin Programado
    Grupo Hoja Ruta
    CGH
    Plan Mantenimiento Preventivo
    Posicion Mto
    Status Sistema
    Status Usuario
* Añadir dos columnas, KPI30 y KPI60, con valor verdadero/falso según si se tiene en cuenta para el calculo de dicho kpi. El valor booleano se obtiene de comparar la fecha de inicio programado + 30/60 con la fecha actual. Si la fecha es menor el resultado es VERDADERO.
* Hay que formatear los datos para que se puedan obtener diferentes gráficos para el KPI ADH-MP > 30 DÍAS y ADH-MP > 60 dias.
* Determinar los graficos a obtener antes de seguir, para definir cómo deben estructurarse los datos.
