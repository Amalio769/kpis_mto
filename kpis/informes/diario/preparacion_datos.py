# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 18:36:56 2020

@author: C48142
"""

def checkCsv(file_name,separator):
    """ Comprobar coherencia fichero csv de Informe Diario
    
    Comprueba si el fichero 'file' es coherente y todas sus líneas tienen
    el mismo número de separadores. La función devuelve un list con las dife-
    rencias con respecto a la fila de encabezado
    """
    
    result = []
    diferencia = []
    # En  el listado result se almacena del numero de separadores por línea
    with open(file_name,'r') as f:
        for line in f:
            result.append(line.count(separator))
    # En el listado diferencia se almacena la diferencia entre la posición 0,
    # que corresponde a la cabecera y cada una de las líneas.
    for idx in range(len(result)):
        diferencia.append(result[idx]-result[0])
    return diferencia

def modificarCabeceraCsv(file_name):
    """ Elimina del encabeado del fichero de Informe Diario el último ';'
    
    """
    
    # Lectura del fichero original
    lineas=open(file_name, 'r').readlines()
    
    # Modificación del contenido original.
    # Un string es inmutable, con lo que hay que convertirlo a una lista para
    # poder modificarlo y luego volver a unirlo en un string.El último ';' está
    # en la posición [-2], ya que el último carácter es un caracter de nueva
    # linea o retorno de carro.
    cabecera=list(lineas[0])
    if(cabecera[-2])==';':
        del cabecera[-2]
    lineas[0]="".join(cabecera)
        
    # Escritura del fichero modificado
    out = open(file_name, 'w')
    out.writelines(lineas)
    out.close()

def modificarContenidoCsv(file_name):
    """ Modificar contenido fichero csv de Informe Diario
    
    Modifica el contenido del fichero file_name, de tal manera que añade
    un ';' en el lugar apropiado, para simular la falta de la columna PAIR,
    que no siempre viene incluida. Para identificar el error se usa la siguien-
    te condición --> si entre los ';' de las posiciones 48 y 47 hay mas de 
    nueve posiciones es porque es un campo de fecha y por lo tanto hay que
    añadir un ';'. 
    """
    
    lineas=open(file_name, 'r').readlines()
    
    lineas_modificadas=[]
    
    for linea in lineas:
        lst_linea=list(linea)           # convierte el string linea en un list
        posPuntoComa=[]
        for i in range(len(lst_linea)): # bucle para leer posiciones de ';'
            if(lst_linea[i])==';':
                posPuntoComa.append(i)
        if len(posPuntoComa)>50 and (linea[0:5] == "Orden" or linea[0:5] == "00000"):
            if posPuntoComa[48]-posPuntoComa[47]>9 and posPuntoComa[48]-posPuntoComa[47]<25:
                lst_linea.insert(posPuntoComa[47]+1,';')
            lineas_modificadas.append("".join(lst_linea))

    
    # Escritura del fichero modificado
    out = open(file_name, 'w')
    out.writelines(lineas_modificadas)
    out.close() 
    
            