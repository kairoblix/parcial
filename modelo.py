"""
MODELO (M del patrón MVC)
Responsable de TODO lo relacionado con datos:
- Consumir la API de datos.gov.co
- Conexión a MySQL (XAMPP)
- Operaciones CRUD sobre la tabla 'registros'
- Consultas de análisis
No imprime nada en pantalla: solo devuelve datos.
"""

import requests
import mysql.connector

URL_API = "https://www.datos.gov.co/resource/gt2j-8ykr.json"


class Modelo:
    def __init__(self):
        
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="datoscolombia"
        )
        self.cursor = self.conexion.cursor()

    
    def cargar_desde_api(self, limite=10):
        """Descarga los datos de la API y los inserta frescos en la BD."""
        try:
            respuesta = requests.get(URL_API, timeout=10)
            respuesta.raise_for_status()          # valida codigo HTTP (errores 4xx/5xx)
            datos = respuesta.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] No se pudo consultar la API: {e}")
            return 0

        self.cursor.execute("TRUNCATE TABLE registros")
        for fila in datos[:limite]:
            ciudad = fila.get('ciudad_municipio_nom',
                      fila.get('municipio_nom',
                      fila.get('ciudad', 'No especificado')))
            departamento = fila.get('departamento_nom',
                            fila.get('departamento', 'No especificado'))
            try:
                edad = int(fila.get('edad', 0))
            except (ValueError, TypeError):
                edad = 0
            self.crear(ciudad, departamento, edad)
        self.conexion.commit()
        return len(datos[:limite])

   
    def crear(self, ciudad, departamento, edad):
        self.cursor.execute(
            "INSERT INTO registros (ciudad, departamento, edad) VALUES (%s,%s,%s)",
            (ciudad, departamento, edad)
        )
        self.conexion.commit()

    def leer(self):
        self.cursor.execute("SELECT * FROM registros")
        return self.cursor.fetchall()

    def actualizar(self, id_registro, nueva_ciudad):
        self.cursor.execute(
            "UPDATE registros SET ciudad=%s WHERE id=%s",
            (nueva_ciudad, id_registro)
        )
        self.conexion.commit()
        return self.cursor.rowcount      

    def eliminar(self, id_registro):
        self.cursor.execute("DELETE FROM registros WHERE id=%s", (id_registro,))
        self.conexion.commit()
        return self.cursor.rowcount

    
    def analisis(self):
        """Devuelve estadisticas simples calculadas sobre los datos."""
        self.cursor.execute(
            "SELECT departamento, COUNT(*), AVG(edad) "
            "FROM registros GROUP BY departamento"
        )
        return self.cursor.fetchall()   

    def cerrar(self):
        self.conexion.close()