import requests
import json
import mysql.connector

"""
PUNTO DE ENTRADA del programa.
Solo crea el Controlador y lo ejecuta (MVC).
Ejecutar con:  python main.py
"""

from controlador import Controlador

if __name__ == "__main__":
    app = Controlador()
    app.iniciar()
    


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="datoscolombia"
)

cursor = conexion.cursor()
print("Conexion exitosa a MySQL")


def mostrar_datos():
    cursor.execute("SELECT * FROM registros")
    datos_sql = cursor.fetchall()
    
    print("\n--- REGISTROS ACTUALES EN LA BASE DE DATOS ---")
    if not datos_sql:
        print("La tabla está vacía.")
    for dato in datos_sql:
        print(f"ID: {dato[0]} | Ciudad: {dato[1]} | Departamento: {dato[2]} | Edad: {dato[3]}")
    print("-----------------------------------------------\n")



url = "https://www.datos.gov.co/resource/gt2j-8ykr.json"
respuesta = requests.get(url)
datos = respuesta.json()

print(f"Registros obtenidos de la API: {len(datos)}")

cursor.execute("TRUNCATE TABLE registros") 

for fila in datos[:10]:
    ciudad = fila.get('municipio_nom', fila.get('ciudad', fila.get('municipio', fila.get('nombre_municipio', 'No especificado'))))
    departamento = fila.get('departamento_nom', fila.get('departamento', fila.get('nombre_depa', 'No especificado')))
    
    try:
        edad = int(fila.get('edad', fila.get('edad_anos', 0)))
    except:
        edad = 0
    
    cursor.execute("""
        INSERT INTO registros (ciudad, departamento, edad)
        VALUES (%s, %s, %s)
    """, (ciudad, departamento, edad))

conexion.commit()
print("Datos de la API cargados e insertados con éxito.")


ejecutando = True

while ejecutando:
    
    mostrar_datos()
    
    print("¿Qué acción desea realizar?")
    print("1. Actualizar un registro (UPDATE)")
    print("2. Eliminar un registro (DELETE)")
    print("3. Solo ver los datos actuales (READ)")
    print("4. Cerrar conexión y salir")
    
    opcion = input("Seleccione una opción (1-4): ").strip()
    
    if opcion == '1':
       
        try:
            id_actualizar = int(input("\nIngrese ID del registro a actualizar: "))
            nueva_ciudad = input("Ingrese nueva ciudad: ")

            cursor.execute("""
                UPDATE registros
                SET ciudad = %s
                WHERE id = %s
            """, (nueva_ciudad, id_actualizar))
            conexion.commit()
            print("\n>>> ¡Registro actualizado con éxito! <<<")
        except Exception as e:
            print(f"\nError al actualizar: {e}")
            
    elif opcion == '2':
       
        try:
            id_eliminar = int(input("\nIngrese ID del registro a eliminar: "))
            cursor.execute("""
                DELETE FROM registros
                WHERE id = %s
            """, (id_eliminar,))
            conexion.commit()
            print("\n>>> ¡Registro eliminado con éxito! <<<")
        except Exception as e:
            print(f"\nError al eliminar: {e}")
            
    elif opcion == '3':
    
        print("\nRefrescando vista de datos...")
        
    elif opcion == '4':
        
        print("\nPreparando para salir...")
        confirmacion = input("¿Está seguro de que desea cerrar la conexión? (s/n): ").strip().lower()
        if confirmacion == 's':
            ejecutando = False 
        else:
            print("\nOperación cancelada. Volviendo al menú.")
            
    else:
        print("\n[Opción inválida] Por favor, digite un número entre 1 y 4.")
    
    if ejecutando:
        input("\nPresione ENTER para continuar en el sistema...")


conexion.close()
print("\nConexion cerrada correctamente. ¡Programa finalizado!")