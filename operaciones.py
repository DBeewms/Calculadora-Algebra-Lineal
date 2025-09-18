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
    """Aplica Gauss-Jordan para obtener forma escalonada reducida.
    Devuelve resultado final, columnas pivote y procedimiento"""
    R = copiar_matriz(M)
    m = len(R)
    n = len(R[0]) - 1
    pasos = []  # historial

    def registrar(operacion):
        pasos.append({"operacion": operacion, "matriz": copiar_matriz(R)})
    fila_pivote = 0
    col = 0
    # Recorre columnas buscando pivotes y los normaliza
    while col < n and fila_pivote < m:
        # Buscar fila con entrada no cero en la columna actual
        r = fila_pivote
        pivote_en = -1
        while r < m:
            if not es_cero(R[r][col]):
                pivote_en = r
                break
            r += 1
        if pivote_en == -1:
            col += 1
            continue
        if pivote_en != fila_pivote:
            fila_intercambiar(R, fila_pivote, pivote_en)
            registrar("Intercambiar F" + str(fila_pivote+1) + " ↔ F" + str(pivote_en+1))
        piv = R[fila_pivote][col]
        if not es_uno(piv):
            inv = dividir_fracciones([1,1], piv)
            fila_escalar(R, fila_pivote, inv)
            registrar("F" + str(fila_pivote+1) + " → (1/" + texto_fraccion(piv) + ")·F" + str(fila_pivote+1))
        # Anular el resto de la columna
        r = 0
        while r < m:
            if r != fila_pivote and not es_cero(R[r][col]):
                factor = R[r][col]
                fila_sumar_multiplo(R, r, fila_pivote, negativo_fraccion(factor))
                registrar("F" + str(r+1) + " → F" + str(r+1) + " − (" + texto_fraccion(factor) + ")·F" + str(fila_pivote+1))
            r += 1
        fila_pivote += 1
        col += 1
    # Estado final
    registrar("Matriz en forma escalonada reducida por filas (final)")
    # Identificar columnas pivote
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
                rr += 1
            if limpio:
                pivotes.append(c)
                r += 1
        c += 1
    return [R, pivotes, pasos]

def eliminacion_gauss(M):
    # Eliminación de Gauss para forma escalonada superior
    R = copiar_matriz(M)
    m = len(R)
    n = len(R[0]) - 1
    pasos = []

    def registrar(op):
        pasos.append({"operacion": op, "matriz": copiar_matriz(R)})

    fila_pivote = 0
    col = 0
    while col < n and fila_pivote < m:
        r = fila_pivote
        pivote_en = -1
        while r < m:
            if not es_cero(R[r][col]):
                pivote_en = r
                break
            r += 1
        if pivote_en == -1:
            col += 1
            continue
        if pivote_en != fila_pivote:
            fila_intercambiar(R, fila_pivote, pivote_en)
            registrar("Intercambiar F" + str(fila_pivote+1) + " ↔ F" + str(pivote_en+1))
        piv = R[fila_pivote][col]
        if not es_uno(piv):
            inv = dividir_fracciones([1,1], piv)
            fila_escalar(R, fila_pivote, inv)
            registrar("F" + str(fila_pivote+1) + " → (1/" + texto_fraccion(piv) + ")·F" + str(fila_pivote+1))
        r = fila_pivote + 1
        while r < m:
            if not es_cero(R[r][col]):
                factor = R[r][col]
                fila_sumar_multiplo(R, r, fila_pivote, negativo_fraccion(factor))
                registrar("F" + str(r+1) + " → F" + str(r+1) + " − (" + texto_fraccion(factor) + ")·F" + str(fila_pivote+1))
            r += 1
        fila_pivote += 1
        col += 1
    registrar("Matriz en forma escalonada")
    # Detecta columnas pivote
    pivotes = []
    r = 0
    c = 0
    while c < n and r < m:
        if not es_cero(R[r][c]):
            # asegurar que es primer no cero
            k = 0
            es_primero = True
            while k < c:
                if not es_cero(R[r][k]):
                    es_primero = False
                    break
                k += 1
            if es_primero:
                pivotes.append(c)
                r += 1
        c += 1
    return [R, pivotes, pasos]

def analizar_solucion_gauss(R, pivotes):
    # Resuelve sistema a partir de forma escalonada y analiza con eliminación gaussiana
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
            j += 1
        if todos_ceros and not es_cero(R[i][n]):
            return {"solucion": "INCONSISTENTE", "tipo_forma": "ESCALONADA"}
        i += 1
    solucion_particular = []
    j = 0
    while j < n:
        solucion_particular.append([0,1])
        j += 1
    libres = []
    c = 0
    while c < n:
        es_libre = True
        k = 0
        while k < len(pivotes):
            if pivotes[k] == c:
                es_libre = False
                break
            k += 1
        if es_libre:
            libres.append(c)
        c += 1
    fila = m - 1
    while fila >= 0:
        # encontrar pivote
        piv_col = -1
        col = 0
        while col < n:
            if not es_cero(R[fila][col]):
                piv_col = col
                break
            col += 1
        if piv_col != -1:
            suma = [0,1]
            j = piv_col + 1
            while j < n:
                if not es_cero(R[fila][j]):
                    suma = sumar_fracciones(suma, multiplicar_fracciones(R[fila][j], solucion_particular[j]))
                j += 1
            rhs = R[fila][n]
            resto = restar_fracciones(rhs, suma)
            piv = R[fila][piv_col]
            if not es_uno(piv):
                valor = dividir_fracciones(resto, piv)
            else:
                valor = resto
            solucion_particular[piv_col] = valor
        fila -= 1
    if len(pivotes) == n:
        return {"solucion": "UNICA", "solucion_particular": solucion_particular, "tipo_forma": "ESCALONADA"}
    return {"solucion": "INFINITAS", "solucion_particular": solucion_particular, "libres": libres, "tipo_forma": "ESCALONADA"}

def analizar_solucion(R, pivotes):
    # Analiza solución con Gauss-Jordan
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
            return {"solucion": "INCONSISTENTE", "tipo_forma": "ESCALONADA_REDUCIDA", "pivotes": pivotes}
        i = i + 1
    solucion_particular = []
    j = 0
    while j < n:
        solucion_particular.append([0,1])
        j = j + 1
    r = 0
    k = 0
    while k < len(pivotes):
        columna_pivote = pivotes[k]
        solucion_particular[columna_pivote] = R[r][n]
        r = r + 1
        k = k + 1
    if len(pivotes) == n:
        return {"solucion": "UNICA", "solucion_particular": solucion_particular, "tipo_forma": "ESCALONADA_REDUCIDA", "pivotes": pivotes}
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
    return {"solucion": "INFINITAS", "solucion_particular": solucion_particular, "libres": libres, "tipo_forma": "ESCALONADA_REDUCIDA", "pivotes": pivotes}
