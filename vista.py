"""
VISTA (V del patrón MVC)
Responsable de TODO lo que ve el usuario:
- Mostrar registros, menus y mensajes
- Capturar lo que el usuario escribe
No accede a la base de datos ni a la API.
"""


class Vista:
    def mostrar_registros(self, datos):
        print("\n--- REGISTROS ACTUALES EN LA BASE DE DATOS ---")
        if not datos:
            print("La tabla esta vacia.")
        for d in datos:
            print(f"ID: {d[0]} | Ciudad: {d[1]} | Departamento: {d[2]} | Edad: {d[3]}")
        print("-----------------------------------------------")

    def mostrar_analisis(self, filas):
        print("\n--- ANALISIS POR DEPARTAMENTO ---")
        for dep, total, promedio in filas:
            print(f"{dep}: {total} registros | edad promedio: {round(float(promedio),1)}")
        print("---------------------------------")

    def mostrar_menu(self):
        print("\n¿Que accion desea realizar?")
        print("1. Crear un registro (CREATE)")
        print("2. Actualizar un registro (UPDATE)")
        print("3. Eliminar un registro (DELETE)")
        print("4. Ver datos actuales (READ)")
        print("5. Ver analisis y grafica")
        print("6. Cerrar conexion y salir")
        return input("Seleccione una opcion (1-6): ").strip()

    def pedir(self, mensaje):
        return input(mensaje).strip()

    def mensaje(self, texto):
        print(texto)