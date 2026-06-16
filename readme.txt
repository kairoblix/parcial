======================================================================
GUÍA DE EJECUCIÓN - PROYECTO INTEGRADOR: DATOS ABIERTOS COLOMBIA
======================================================================
Estimada profesora, para ejecutar correctamente este sistema en su 
computador, por favor siga los siguientes pasos:
1. REQUISITOS PREVIOS (LIBRERÍAS):
   Abra la terminal en su editor de código (o CMD) e instale la librería
   necesaria para la conexión con MySQL ejecutando el siguiente comando:
   
   pip install mysql-connector-python requests
2. CONFIGURACIÓN DE LA BASE DE DATOS (XAMPP / phpMyAdmin):
   - Inicie los servicios de Apache y MySQL desde el Panel de XAMPP.
   - Ingrese a http://localhost/phpmyadmin/
   - Cree una nueva base de datos llamada exactamente: datoscolombia
   - Seleccione la base de datos creada, vaya a la pestaña "Importar", 
     seleccione el archivo "respaldo_base_datos.sql" incluido en esta 
     carpeta y haga clic en "Importar" (al final de la página).
3. EJECUCIÓN DEL PROGRAMA:
   - Abra la carpeta en Visual Studio Code.
   - Ejecute el archivo principal con el comando:
     python main.py
4. FUNCIONALIDADES INCLUIDAS EN EL MENÚ:
   El programa consume automáticamente los primeros 10 registros de la 
   API de datos.gov.co, limpia la tabla antigua (Truncate) e inserta 
   los datos frescos. Posteriormente, despliega un menú interactivo en 
   bucle continuo (while) que le permitirá:
   - Actualizar un registro (UPDATE) y ver el cambio en tiempo real.
   - Eliminar un registro (DELETE) y verificar la actualización.
   - Consultar la tabla completa (READ).
   - Decidir cuándo cerrar la conexión de forma segura.
======================================================================
