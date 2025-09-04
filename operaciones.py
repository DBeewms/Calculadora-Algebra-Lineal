
# operaciones.py

import utilidades as u
from utilidades import (
    texto_fraccion,
    copiar_matriz,
    es_cero,
    es_uno,
    negativo_fraccion,
    dividir_fracciones,
    sumar_fracciones,
    restar_fracciones,
    multiplicar_fracciones,
    simplificar_fraccion,
)

# Las operaciones sobre fracciones y utilidades están en utilidades.py

def copiar_matriz(M):
    return u.copiar_matriz(M)

def fila_intercambiar(M, i, j):
    temp = M[i]
    M[i] = M[j]
    M[j] = temp

def fila_escalar(M, i, c):
    columnas = len(M[i])
    j = 0
    while j < columnas:
        M[i][j] = multiplicar_fracciones(M[i][j], c)
        j = j + 1

def fila_sumar_multiplo(M, i, j, c):
    columnas = len(M[i])
    k = 0
    while k < columnas:
        termino = multiplicar_fracciones(c, M[j][k])
        M[i][k] = sumar_fracciones(M[i][k], termino)
        k = k + 1

def gauss_jordan(M):
    R = copiar_matriz(M)
    m = len(R)
    n = len(R[0]) - 1
    pasos = []
    fila_pivote = 0
    col = 0
    while col < n and fila_pivote < m:
        r = fila_pivote
        pivote_en = -1
        while r < m:
            if not es_cero(R[r][col]):
                pivote_en = r
                break
            r = r + 1
        if pivote_en == -1:
            col = col + 1
            continue
        if pivote_en != fila_pivote:
            fila_intercambiar(R, fila_pivote, pivote_en)
            pasos.append("F" + str(fila_pivote+1) + " ↔ F" + str(pivote_en+1))
        piv = R[fila_pivote][col]
        if not es_uno(piv):
            inv = dividir_fracciones([1,1], piv)
            fila_escalar(R, fila_pivote, inv)
            pasos.append("F" + str(fila_pivote+1) + " → (1/" + texto_fraccion(piv) + ")·F" + str(fila_pivote+1))
        r = 0
        while r < m:
            if r != fila_pivote and not es_cero(R[r][col]):
                factor = R[r][col]
                fila_sumar_multiplo(R, r, fila_pivote, negativo_fraccion(factor))
                pasos.append("F" + str(r+1) + " → F" + str(r+1) + " − (" + texto_fraccion(factor) + ")·F" + str(fila_pivote+1))
            r = r + 1
        fila_pivote = fila_pivote + 1
        col = col + 1
    pivotes = []
    r = 0
    c = 0
    while c < n and r < m:
        if es_uno(R[r][c]):
            limpio = True
            rr = 0
            while rr < m:
                if rr != r and not es_cero(R[rr][c]):
                    limpio = False
                    break
                rr = rr + 1
            if limpio:
                pivotes.append(c)
                r = r + 1
        c = c + 1
    return [R, pivotes, pasos]

def analizar_solucion(R, pivotes):
    m = len(R)
    n = len(R[0]) - 1
    i = 0
    while i < m:
        todos_ceros = True
        j = 0
        while j < n:
            if not es_cero(R[i][j]):
                todos_ceros = False
                break
            j = j + 1
        if todos_ceros and not es_cero(R[i][n]):
            return {"solucion": "INCONSISTENTE"}
        i = i + 1
    x_p = []
    j = 0
    while j < n:
        x_p.append([0,1])
        j = j + 1
    r = 0
    k = 0
    while k < len(pivotes):
        columna_pivote = pivotes[k]
        x_p[columna_pivote] = R[r][n]
        r = r + 1
        k = k + 1
    if len(pivotes) == n:
        return {"solucion": "UNICA", "x_p": x_p}
    libres = []
    c = 0
    while c < n:
        es_libre = True
        q = 0
        while q < len(pivotes):
            if c == pivotes[q]:
                es_libre = False
                break
            q = q + 1
        if es_libre:
            libres.append(c)
        c = c + 1
    # No se devuelven vectores dirección: se devuelve la solución particular y los índices de variables libres
    return {"solucion": "INFINITAS", "x_p": x_p, "libres": libres}
