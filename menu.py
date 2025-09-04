
# menu.py

import operaciones
import utilidades as u

def leer_matriz_aumentada():
    m = int(input("Número de ecuaciones m = ").strip())
    n = int(input("Número de incógnitas n = ").strip())
    matriz = []
    i = 0
    while i < m:
        linea = input("Ingrese fila " + str(i+1) + " (valores separados por espacios, incluida b): ").strip().split()
        if len(linea) != n + 1:
            print("Cantidad incorrecta de valores. Deben ser", n+1)
            continue
        fila = []
        j = 0
        while j < len(linea):
            fr = u.crear_fraccion_desde_cadena(linea[j])
            fila.append(fr)
            j = j + 1
        matriz.append(fila)
        i = i + 1
    return matriz

def imprimir_matriz_aumentada(M):
    if len(M) == 0:
        print("[]")
        return
    filas = len(M)
    columnas_totales = len(M[0])
    columnas_A = columnas_totales - 1
    anchos = []
    j = 0
    while j < columnas_totales:
        maximo = 0
        i = 0
        while i < filas:
            texto = u.texto_fraccion(M[i][j])
            largo = len(texto)
            if largo > maximo:
                maximo = largo
            i = i + 1
        anchos.append(maximo)
        j = j + 1
    i = 0
    while i < filas:
        izquierda = ""
        j = 0
        while j < columnas_A:
            if j > 0:
                izquierda = izquierda + "  "
            txt = u.texto_fraccion(M[i][j])
            espacios = anchos[j] - len(txt)
            k = 0
            while k < espacios:
                izquierda = izquierda + " "
                k = k + 1
            izquierda = izquierda + txt
            j = j + 1
        txt_b = u.texto_fraccion(M[i][columnas_A])
        espacios_b = anchos[columnas_A] - len(txt_b)
        pad = ""
        k = 0
        while k < espacios_b:
            pad = pad + " "
            k = k + 1
        print("[ " + izquierda + " | " + pad + txt_b + " ]")
        i = i + 1

# Se eliminó imprimir_vector: mostramos componentes por separado

def mostrar_pasos(pasos):
    if not pasos:
        print("No se realizaron operaciones (la matriz ya estaba en RREF o vacía).")
        return
    i = 0
    while i < len(pasos):
        print(str(i+1) + ". " + pasos[i])
        i = i + 1

def mostrar_resultado(R, info):
    solucion = info["solucion"]
    if solucion == "INCONSISTENTE":
        print("Solución:", solucion)
        print("RREF([A|b]):")
        imprimir_matriz_aumentada(R)
        return
    if solucion == "UNICA":
        print("Solución:", solucion)
        i = 0
        while i < len(info["x_p"]):
            print("x" + str(i+1) + " = " + u.texto_fraccion(info["x_p"][i]))
            i = i + 1
        print("RREF([A|b]):")
        imprimir_matriz_aumentada(R)
        return
    if solucion == "INFINITAS":
        print("Solución:", solucion)
        print("Solución particular (valores conocidos, 0 para libres):")
        i = 0
        while i < len(info["x_p"]):
            print("x" + str(i+1) + " = " + operaciones.texto_fraccion(info["x_p"][i]))
            i = i + 1
        if "libres" in info and len(info["libres"]) > 0:
            nombres_libres = ""
            contador_libres = 0
            while contador_libres < len(info["libres"]):
                idx = info["libres"][contador_libres]
                nombres_libres = nombres_libres + "x" + str(idx+1)
                if contador_libres < len(info["libres"]) - 1:
                    nombres_libres = nombres_libres + ", "
                contador_libres = contador_libres + 1
            print("Variables libres:", nombres_libres)
        print("RREF([A|b]):")
        imprimir_matriz_aumentada(R)
