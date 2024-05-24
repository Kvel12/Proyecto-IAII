import random
import time

# Movimientos posibles para el yoshi en forma de cabello en un tablero de ajedrez
MOVIMIENTOS_CABALLO = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

# Funciones de lógica del juego
def iniciar_juego(nivel): # Iniciar un nuevo juego
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

# Función para establecer la profundidad del árbol de búsqueda según el nivel seleccionado
def establecer_profundidad(nivel):
    if nivel == 'principiante':
        return 2
    elif nivel == 'amateur':
        return 4
    elif nivel == 'experto':
        return 6

# Función para obtener los movimientos válidos de un yoshi en el tablero
def obtener_movimientos_validos(juego, color):
    movimientos_validos = []
    x, y = juego['posiciones'][color]
    for mov in MOVIMIENTOS_CABALLO:
        nueva_fila = x + mov[0]
        nueva_columna = y + mov[1]
        if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and juego["tablero"][nueva_fila][nueva_columna] is None:
            movimientos_validos.append((nueva_fila, nueva_columna))
    return movimientos_validos

# Función para realizar un movimiento en el tablero
def realizar_movimiento(juego, movimiento, color):
    x, y = movimiento
    juego["tablero"][x][y] = color
    juego['posiciones'][color] = (x, y)
    juego['puntuacion'][color] += 1

# Función para verificar si el juego ha terminado
def verificar_fin_juego(juego):
    movimientos_verdes = obtener_movimientos_validos(juego, 'verde')
    movimientos_rojos = obtener_movimientos_validos(juego, 'rojo')
    return not movimientos_verdes and not movimientos_rojos

# Función para el movimiento de la máquina
def movimiento_maquina(juego):
    turno_actual = juego["turno"]
    movimientos_validos = obtener_movimientos_validos(juego, turno_actual)

    # Realizar el movimiento de la máquina si hay movimientos válidos
    if movimientos_validos:
        mejor_movimiento = minimax(juego, juego['profundidad'], turno_actual == 'verde')
        if mejor_movimiento is not None:  # Verificar si hay un movimiento válido
            realizar_movimiento(juego, mejor_movimiento, turno_actual)
            time.sleep(1)  # Agregar un retraso de 1 segundo (ajustar según sea necesario)

    # Mostrar mensaje si no hay movimientos válidos para la máquina
    else:
        print(f"¡Yoshi {turno_actual} no tiene movimientos válidos!")
        # Pasar el turno al otro jugador si no hay movimientos válidos para el jugador actual
        otro_jugador = 'rojo' if turno_actual == 'verde' else 'verde'
        otro_movimientos_validos = obtener_movimientos_validos(juego, otro_jugador)
        if otro_movimientos_validos:
            print(f"Turno para ¡Yoshi {otro_jugador}!")
            juego["turno"] = otro_jugador
        else:
            # Si ninguno de los jugadores puede moverse, el juego termina
            print("¡Fin del juego!")
            mostrar_ganador(juego)
            return  # Termina la función para no pasar el turno

    # Pasar el turno al otro jugador incluso si la máquina no tiene movimientos válidos
    juego["turno"] = 'rojo' if turno_actual == 'verde' else 'verde'

# Función para el algoritmo Minimax con poda alfa-beta para la toma de decisiones de la máquina (IA)
def minimax(juego, profundidad, es_maximizador, alfa=float('-inf'), beta=float('inf')):
    if profundidad == 0 or verificar_fin_juego(juego):
        return evaluar_tablero(juego)

    # Maximizar el movimiento de la máquina (verde) y minimizar el movimiento del jugador (rojo)
    if es_maximizador:
        max_eval = float('-inf')
        mejor_movimiento = None
        for movimiento in obtener_movimientos_validos(juego, 'verde'):
            copia_juego = copiar_juego(juego)
            realizar_movimiento(copia_juego, movimiento, 'verde')
            evaluacion = minimax(copia_juego, profundidad - 1, False, alfa, beta)
            if evaluacion is not None and evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = movimiento
            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break  # Poda beta
        return mejor_movimiento if profundidad == juego['profundidad'] else max_eval
    else:
        min_eval = float('inf')
        mejor_movimiento = None
        for movimiento in obtener_movimientos_validos(juego, 'rojo'):
            copia_juego = copiar_juego(juego)
            realizar_movimiento(copia_juego, movimiento, 'rojo')
            evaluacion = minimax(copia_juego, profundidad - 1, True, alfa, beta)
            if evaluacion is not None and evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = movimiento
            beta = min(beta, evaluacion)
            if beta <= alfa:
                break  # Poda alfa
        return mejor_movimiento if profundidad == juego['profundidad'] else min_eval

# Función para evaluar el tablero y determinar la puntuación de la máquina (verde) y el jugador (rojo)
def evaluar_tablero(juego):
    return juego['puntuacion']['verde'] - juego['puntuacion']['rojo']

# Función para copiar el estado actual del juego
def copiar_juego(juego):
    return {
        "tablero": [fila[:] for fila in juego["tablero"]],
        "turno": juego["turno"],
        "nivel": juego["nivel"],
        "puntuacion": juego["puntuacion"].copy(),
        "posiciones": juego["posiciones"].copy(),
        "profundidad": juego["profundidad"]
    }
 
# Función para mostrar el ganador del juego en la consola
def mostrar_ganador(juego): 
    puntuacion_verde = juego['puntuacion']['verde']
    puntuacion_rojo = juego['puntuacion']['rojo']
    if puntuacion_verde > puntuacion_rojo:
        mensaje_ganador = "¡Yoshi verde gana!"
    elif puntuacion_rojo > puntuacion_verde:
        mensaje_ganador = "¡Yoshi rojo gana!"
    else:
        mensaje_ganador = "¡Es un empate!"
    print(mensaje_ganador)
    return mensaje_ganador

       
