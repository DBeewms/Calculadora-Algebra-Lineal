
# main.py

import operaciones
import menu

def ejecutar():
    M = menu.leer_matriz_aumentada()
    R, pivotes, pasos = operaciones.gauss_jordan(M)
    respuesta = operaciones.analizar_solucion(R, pivotes)
    ver = input("Mostrar pasos de eliminación? (s/n): ").strip().lower()
    if ver == "s":
        menu.mostrar_pasos(pasos)
    menu.mostrar_resultado(R, respuesta)

if __name__ == "__main__":
    ejecutar()
