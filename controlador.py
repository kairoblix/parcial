"""
CONTROLADOR (C del patrón MVC)
Conecta el Modelo (datos) con la Vista (interfaz).
Contiene la logica del programa: decide que hacer segun la opcion del usuario.
"""

import matplotlib.pyplot as plt
from modelo import Modelo
from vista import Vista


class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = Vista()

    def iniciar(self):
        self.vista.mensaje("Conexion exitosa a MySQL")
        cantidad = self.modelo.cargar_desde_api(10)
        self.vista.mensaje(f"Registros cargados desde la API: {cantidad}")

        ejecutando = True
        while ejecutando:
            self.vista.mostrar_registros(self.modelo.leer())
            opcion = self.vista.mostrar_menu()

            if opcion == '1':                       # CREATE
                ciudad = self.vista.pedir("Ciudad: ")
                depto = self.vista.pedir("Departamento: ")
                try:
                    edad = int(self.vista.pedir("Edad: "))
                except ValueError:
                    edad = 0
                self.modelo.crear(ciudad, depto, edad)
                self.vista.mensaje(">>> Registro creado con exito <<<")

            elif opcion == '2':                     # UPDATE
                try:
                    idr = int(self.vista.pedir("ID a actualizar: "))
                    nueva = self.vista.pedir("Nueva ciudad: ")
                    if self.modelo.actualizar(idr, nueva):
                        self.vista.mensaje(">>> Registro actualizado <<<")
                    else:
                        self.vista.mensaje("No existe ese ID.")
                except ValueError:
                    self.vista.mensaje("ID invalido.")

            elif opcion == '3':                     # DELETE
                try:
                    idr = int(self.vista.pedir("ID a eliminar: "))
                    if self.modelo.eliminar(idr):
                        self.vista.mensaje(">>> Registro eliminado <<<")
                    else:
                        self.vista.mensaje("No existe ese ID.")
                except ValueError:
                    self.vista.mensaje("ID invalido.")

            elif opcion == '4':                     # READ
                self.vista.mensaje("Refrescando vista de datos...")

            elif opcion == '5':                     # ANALISIS + GRAFICA
                filas = self.modelo.analisis()
                self.vista.mostrar_analisis(filas)
                self.generar_grafica(filas)

            elif opcion == '6':                     # SALIR
                if self.vista.pedir("¿Seguro que desea salir? (s/n): ").lower() == 's':
                    ejecutando = False
                else:
                    self.vista.mensaje("Operacion cancelada.")
            else:
                self.vista.mensaje("[Opcion invalida] Digite un numero entre 1 y 6.")

            if ejecutando:
                self.vista.pedir("\nPresione ENTER para continuar...")

        self.modelo.cerrar()
        self.vista.mensaje("\nConexion cerrada correctamente. Programa finalizado!")

    def generar_grafica(self, filas):
        """Grafica de barras: cantidad de registros por departamento."""
        if not filas:
            self.vista.mensaje("No hay datos para graficar.")
            return
        departamentos = [f[0] for f in filas]
        totales = [f[1] for f in filas]
        plt.bar(departamentos, totales, color="#2563eb")
        plt.title("Registros por departamento")
        plt.xlabel("Departamento")
        plt.ylabel("Cantidad de registros")
        plt.tight_layout()
        plt.savefig("grafica.png")     # se guarda como imagen
        plt.show()
        self.vista.mensaje("Grafica guardada como 'grafica.png'")