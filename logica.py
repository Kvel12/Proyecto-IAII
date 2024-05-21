import random

MOVIMIENTOS_CABALLO = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

def iniciar_juego(nivel):
    tablero = [[None] * 8 for _ in range(8)]  # Tablero de 8x8
    yoshi_verde = (random.randint(0, 7), random.randint(0, 7))
    yoshi_rojo = (random.randint(0, 7), random.randint(0, 7))
    while yoshi_verde == yoshi_rojo:  # Asegurar que las posiciones iniciales no coincidan
        yoshi_rojo = (random.randint(0, 7), random.randint(0, 7))
    tablero[yoshi_verde[0]][yoshi_verde[1]] = 'verde'
    tablero[yoshi_rojo[0]][yoshi_rojo[1]] = 'rojo'
    return {
        "tablero": tablero,
        "turno": 'verde',
        "nivel": nivel,
        "puntuacion": {
            "verde": 1,
            "rojo": 1
        },
        "posiciones": {
            "verde": yoshi_verde,
            "rojo": yoshi_rojo
        },
        "profundidad": establecer_profundidad(nivel)
    }

def establecer_profundidad(nivel):
    if nivel == 'principiante':
        return 2
    elif nivel == 'amateur':
        return 4
    elif nivel == 'experto':
        return 6

def obtener_movimientos_validos(juego, color):
    movimientos_validos = []
    x, y = juego['posiciones'][color]
    for mov in MOVIMIENTOS_CABALLO:
        nueva_fila = x + mov[0]
        nueva_columna = y + mov[1]
        if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and juego["tablero"][nueva_fila][nueva_columna] is None:
            movimientos_validos.append((nueva_fila, nueva_columna))
    return movimientos_validos

def realizar_movimiento(juego, movimiento, color):
    x, y = movimiento
    juego["tablero"][x][y] = color
    juego['posiciones'][color] = (x, y)
    juego['puntuacion'][color] += 1

def verificar_fin_juego(juego):
    movimientos_verdes = obtener_movimientos_validos(juego, 'verde')
    movimientos_rojos = obtener_movimientos_validos(juego, 'rojo')
    return not movimientos_verdes and not movimientos_rojos

def movimiento_maquina(juego):
    mejor_movimiento = minimax(juego, juego['profundidad'], True)
    if mejor_movimiento:
        realizar_movimiento(juego, mejor_movimiento, 'verde')
    juego["turno"] = 'rojo'

def minimax(juego, profundidad, es_maximizador):
    if profundidad == 0 or verificar_fin_juego(juego):
        return evaluar_tablero(juego)
    
    if es_maximizador:
        max_eval = float('-inf')
        mejor_movimiento = None
        for movimiento in obtener_movimientos_validos(juego, 'verde'):
            copia_juego = copiar_juego(juego)
            realizar_movimiento(copia_juego, movimiento, 'verde')
            evaluacion = minimax(copia_juego, profundidad - 1, False)
            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = movimiento
        return mejor_movimiento if profundidad == juego['profundidad'] else max_eval
    else:
        min_eval = float('inf')
        for movimiento in obtener_movimientos_validos(juego, 'rojo'):
            copia_juego = copiar_juego(juego)
            realizar_movimiento(copia_juego, movimiento, 'rojo')
            evaluacion = minimax(copia_juego, profundidad - 1, True)
            min_eval = min(min_eval, evaluacion)
        return min_eval

def evaluar_tablero(juego):
    return juego['puntuacion']['verde'] - juego['puntuacion']['rojo']

def copiar_juego(juego):
    return {
        "tablero": [fila[:] for fila in juego["tablero"]],
        "turno": juego["turno"],
        "nivel": juego["nivel"],
        "puntuacion": juego["puntuacion"].copy(),
        "posiciones": juego["posiciones"].copy(),
        "profundidad": juego["profundidad"]
    }
