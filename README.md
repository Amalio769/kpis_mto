# *__APP KPIs MANTENIMIENTO__*

Creado por: Maria José Tocino & Amalio Rete Campos

Última versión: V1.1.4

## *REQUISITOS DE INSTALACIÓN*

#### Debes tener instalado:
* Anaconda 3
* Git

#### Hay que configurar Anaconda
* Abre el siguiente enlace [https://github.airbus.corp/Airbus/anaconda-configurator-script]()
* Click sobre **anaconda_condigurator.ps1**
* Click sobre **RAW** y se abrirá una ventana
* Guarda el contenido de la ventana pulsando **CTL+S**
    * En _File Type_ selecciona **All files(\*.\*)**
    * En _File Name_ escribe **anaconda_configurator.ps1**
    * Selecciona tu carpeta preferida. Recomendado usar C:\Users\C48XXX\
    * Abre **powershell* y navega hasta la carpeta donde has guardado el archivo
    > cd c:\users\cXXXXX
    * Ejecuta el script
    > .\anaconda_configurator.ps1
    * Si todo va bien tendrás que aceptar varias preguntas (escribe "y" y pulsa enter), en caso contrario se mostrara en pantalla un mensaje con texto de color rojo.
    
##*INSTALACIÓN*

Primero creamos el environment **appkpimto** de la siguiente forma:

1.- Abrir el Shell de Conda

2.- Ejecuta el siguiente comando para crear el environment con python 3.6.
> conda create --name appkpimto python=3.6

3.- Activa el entorno creado
> conda activate appkpimto

4.- Instala los paquetes necesarios para la aplicación
> conda install -c conda-forge numpy==1.19.5 pyqt==5.12.3 pywin32==300 pandas==1.0.5 openpyxl==3.0.0 xlrd==1.2.0


  

