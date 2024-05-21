import tkinter as tk
import pygame
import logica

def seleccionar_nivel():
    def set_nivel(n):
        nonlocal nivel
        nivel = n
        ventana.destroy()
    
    nivel = None
    ventana = tk.Tk()
    ventana.title("Seleccionar Nivel")
    
    tk.Label(ventana, text="Seleccione el nivel").pack(pady=10)
    
    tk.Button(ventana, text="Principiante", command=lambda: set_nivel('principiante')).pack(pady=5)
    tk.Button(ventana, text="Amateur", command=lambda: set_nivel('amateur')).pack(pady=5)
    tk.Button(ventana, text="Experto", command=lambda: set_nivel('experto')).pack(pady=5)
    
    ventana.mainloop()
    return nivel

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

        if not logica.obtener_movimientos_validos(juego, 'rojo') and juego["turno"] == 'rojo':
            juego["turno"] = 'verde'
            logica.movimiento_maquina(juego)

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
            # Dibujar los cuadrados blancos con márgenes negras
            pygame.draw.rect(pantalla, (255, 255, 255), (j * 75, i * 75, 75, 75))
            pygame.draw.rect(pantalla, (0, 0, 0), (j * 75, i * 75, 75, 75), 1)
            if juego["tablero"][i][j] is not None:
                color_yoshi = (0, 255, 0) if juego["tablero"][i][j] == 'verde' else (255, 0, 0)
                pygame.draw.circle(pantalla, color_yoshi, (j * 75 + 37, i * 75 + 37), 30)

    # Dibujar indicador de posición actual de Yoshi verde
    if juego["posiciones"]["verde"] is not None:
        i, j = juego["posiciones"]["verde"]
        pygame.draw.circle(pantalla, (255, 255, 255), (j * 75 + 37, i * 75 + 37), 10)

    # Dibujar indicador de posición actual de Yoshi rojo
    if juego["posiciones"]["rojo"] is not None:
        i, j = juego["posiciones"]["rojo"]
        pygame.draw.circle(pantalla, (255, 255, 255), (j * 75 + 37, i * 75 + 37), 10)

def mostrar_puntuacion(pantalla, juego):
    font = pygame.font.SysFont(None, 36)
    texto_verde = font.render(f"Verde: {juego['puntuacion']['verde']}", True, (0,0, 0))
    texto_rojo = font.render(f"Rojo: {juego['puntuacion']['rojo']}", True, (0,0, 0))
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