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

    # Configuración de tamaño de la ventana
    ventana.geometry("450x300")

    # Configuración de la fuente
    font_titulo = ("Helvetica", 20, "bold")
    font_botones = ("Helvetica", 16)
    
    tk.Label(ventana, text="Seleccione el nivel", font=font_titulo).pack(pady=20)
    
    tk.Button(ventana, text="Principiante", command=lambda: set_nivel('principiante'), font=font_botones, width=15).pack(pady=10)
    tk.Button(ventana, text="Amateur", command=lambda: set_nivel('amateur'), font=font_botones, width=15).pack(pady=10)
    tk.Button(ventana, text="Experto", command=lambda: set_nivel('experto'), font=font_botones, width=15).pack(pady=10)
    
    ventana.mainloop()
    return nivel

def iniciar_interfaz(juego):
    pygame.init()
    pantalla = pygame.display.set_mode((600, 675))  # Aumentar la altura de la ventana
    pygame.display.set_caption("Yoshi's World")

    # Cargar imágenes de Yoshi
    imagen_yoshi_verde = pygame.image.load('images/YoshiVerde.png')
    imagen_yoshi_rojo = pygame.image.load('images/YoshiRojo.png')

    # Redimensionar las imágenes a 75x75 píxeles
    imagen_yoshi_verde = pygame.transform.scale(imagen_yoshi_verde, (75, 75))
    imagen_yoshi_rojo = pygame.transform.scale(imagen_yoshi_rojo, (75, 75))

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

        pantalla.fill((255, 255, 255))  # Rellenar toda la ventana con blanco
        dibujar_tablero(pantalla, juego, imagen_yoshi_verde, imagen_yoshi_rojo)
        mostrar_informacion(pantalla, juego)
        pygame.display.update()

def convertir_coordenadas_a_casilla(x, y):
    fila = y // 75
    columna = x // 75
    return fila, columna

def dibujar_tablero(pantalla, juego, imagen_yoshi_verde, imagen_yoshi_rojo):
    colores_fondo = [(240, 217, 181), (181, 136, 99)]  # Colores del tablero de ajedrez
    for i in range(8):
        for j in range(8):
            color_fondo = colores_fondo[(i + j) % 2]
            pygame.draw.rect(pantalla, color_fondo, (j * 75, i * 75, 75, 75))
            if juego["tablero"][i][j] is not None:
                color_yoshi = (0, 255, 0) if juego["tablero"][i][j] == 'verde' else (255, 0, 0)
                pygame.draw.circle(pantalla, color_yoshi, (j * 75 + 37, i * 75 + 37), 30)

    # Dibujar indicador de posición actual de Yoshi verde
    if juego["posiciones"]["verde"] is not None:
        i, j = juego["posiciones"]["verde"]
        pantalla.blit(imagen_yoshi_verde, (j * 75, i * 75))

    # Dibujar indicador de posición actual de Yoshi rojo
    if juego["posiciones"]["rojo"] is not None:
        i, j = juego["posiciones"]["rojo"]
        pantalla.blit(imagen_yoshi_rojo, (j * 75, i * 75))

def mostrar_informacion(pantalla, juego):
    font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
    color_jugador = font.render(f"Tu eres el yoshi {juego['turno'].capitalize()}", True, (0, 0, 0))
    texto_verde = font.render(f"Verde: {juego['puntuacion']['verde']}", True, (0, 255, 0))
    texto_rojo = font.render(f"Rojo: {juego['puntuacion']['rojo']}", True, (255, 0, 0))
    
    pantalla.blit(color_jugador, (150, 600))
    pantalla.blit(texto_verde, (75, 630))
    pantalla.blit(texto_rojo, (380, 630))


def mostrar_ganador(juego):
    total_verde = juego['puntuacion']['verde']
    total_rojo = juego['puntuacion']['rojo']
    if total_verde > total_rojo:
        print("¡Yoshi verde gana!")
    elif total_rojo > total_verde:
        print("¡Yoshi rojo gana!")
    else:
        print("¡Empate!")
