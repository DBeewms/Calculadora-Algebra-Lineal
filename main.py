import sys
import operaciones
import menu
import gui


def ejecutar():
    print("Seleccione método:")
    print("  1) Eliminación de Gauss (forma escalonada)")
    print("  2) Gauss-Jordan (forma escalonada reducida por filas)")
    opcion = input("Opción (1/2): ").strip()
    M = menu.leer_matriz_aumentada()
    if opcion == "1":
        R, pivotes, pasos = operaciones.eliminacion_gauss(M)
        respuesta = operaciones.analizar_solucion_gauss(R, pivotes)
    else:
        R, pivotes, pasos = operaciones.gauss_jordan(M)
        respuesta = operaciones.analizar_solucion(R, pivotes)
    ver = input("Mostrar pasos del procedimiento? (s/n): ").strip().lower()
    if ver == "s":
        menu.mostrar_pasos(pasos)
    menu.mostrar_resultado(R, respuesta)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() in {"cli", "-c", "--cli"}:
        ejecutar()
    else:
        gui.run_gui()
