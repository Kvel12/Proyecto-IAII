import pygame
import logica

def seleccionar_nivel():
    while True:
        nivel = input("Seleccione el nivel (principiante, amateur, experto): ").lower()
        if nivel in ['principiante', 'amateur', 'experto']:
            return nivel
        else:
            print("Nivel no válido. Intente de nuevo.")

def iniciar_interfaz(juego):
    pygame.init()
    pantalla = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Yoshi's World")

    logica.movimiento_maquina(juego)  # La máquina inicia el juego

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if juego["turno"] == 'rojo':
                    x, y = event.pos
                    movimiento = convertir_coordenadas_a_casilla(x, y)
                    if movimiento in logica.obtener_movimientos_validos(juego, 'rojo'):
                        logica.realizar_movimiento(juego, movimiento, 'rojo')
                        juego["turno"] = 'verde'
                        if logica.verificar_fin_juego(juego):
                            mostrar_ganador(juego)
                            pygame.quit()
                            quit()
                        else:
                            logica.movimiento_maquina(juego)
                            if logica.verificar_fin_juego(juego):
                                mostrar_ganador(juego)
                                pygame.quit()
                                quit()

        dibujar_tablero(pantalla, juego)
        mostrar_puntuacion(pantalla, juego)
        pygame.display.update()

def convertir_coordenadas_a_casilla(x, y):
    fila = y // 75
    columna = x // 75
    return fila, columna

def dibujar_tablero(pantalla, juego):
    for i in range(8):
        for j in range(8):
            color = (255, 255, 255) if (i + j) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(pantalla, color, (j * 75, i * 75, 75, 75))
            if juego["tablero"][i][j] is not None:
                color_yoshi = (0, 255, 0) if juego["tablero"][i][j] == 'verde' else (255, 0, 0)
                pygame.draw.circle(pantalla, color_yoshi, (j * 75 + 37, i * 75 + 37), 30)

def mostrar_puntuacion(pantalla, juego):
    font = pygame.font.SysFont(None, 36)
    texto_verde = font.render(f"Verde: {juego['puntuacion']['verde']}", True, (0, 255, 0))
    texto_rojo = font.render(f"Rojo: {juego['puntuacion']['rojo']}", True, (255, 0, 0))
    pantalla.blit(texto_verde, (20, 560))
    pantalla.blit(texto_rojo, (450, 560))

def mostrar_ganador(juego):
    total_verde = juego['puntuacion']['verde']
    total_rojo = juego['puntuacion']['rojo']
    if total_verde > total_rojo:
        print("¡Yoshi verde gana!")
    elif total_rojo > total_verde:
        print("¡Yoshi rojo gana!")
    else:
        print("¡Empate!")
