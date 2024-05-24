import tkinter as tk
from tkinter import font
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

    # Configuración de la fuente
    font_titulo = ("Helvetica", 20, "bold")
    font_botones = ("Helvetica", 16)

    tk.Label(ventana, text="Seleccione el nivel", font=font_titulo).pack(pady=20)

    tk.Button(ventana, text="Principiante", command=lambda: set_nivel('principiante'), font=font_botones, width=15).pack(pady=10)
    tk.Button(ventana, text="Amateur", command=lambda: set_nivel('amateur'), font=font_botones, width=15).pack(pady=10)
    tk.Button(ventana, text="Experto", command=lambda: set_nivel('experto'), font=font_botones, width=15).pack(pady=10)

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Obtener las dimensiones de la ventana
    ancho_ventana = 450
    alto_ventana = 300

    # Calcular la posición para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)

    # Establecer la geometría de la ventana para centrarla
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    ventana.mainloop()
    return nivel

def iniciar_interfaz(juego):
    pygame.init()
    pantalla = pygame.display.set_mode((860, 675))
    pygame.display.set_caption("Yoshi's World")

    # Cargar imágenes de Yoshi
    imagen_yoshi_verde = pygame.image.load('images/YoshiVerde.png')
    imagen_yoshi_rojo = pygame.image.load('images/YoshiRojo.png')

    # Redimensionar las imágenes de Yoshi
    imagen_yoshi_verde = pygame.transform.scale(imagen_yoshi_verde, (75, 75))
    imagen_yoshi_rojo = pygame.transform.scale(imagen_yoshi_rojo, (75, 75))
    fondo_bienvenida = pygame.image.load('images/Bienvenida.png')

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
                            mostrar_ganador(juego, pantalla)
                        else:
                            logica.movimiento_maquina(juego)
                            if logica.verificar_fin_juego(juego):
                                mostrar_ganador(juego, pantalla)

        # Si el turno es del Yoshi rojo y no tiene movimientos válidos, pasar el turno al Yoshi verde
        if juego["turno"] == 'rojo' and not logica.obtener_movimientos_validos(juego, 'rojo'):
            juego["turno"] = 'verde'
            logica.movimiento_maquina(juego)
            if logica.verificar_fin_juego(juego):
                mostrar_ganador(juego, pantalla)

        pantalla.fill((255, 255, 255))  # Rellenar toda la ventana con blanco
        dibujar_tablero(pantalla, juego, imagen_yoshi_verde, imagen_yoshi_rojo)
        mostrar_informacion(pantalla, juego)

        imagen_fondo_redimensionada = pygame.transform.scale(fondo_bienvenida, (270, 200))

        pantalla.blit(imagen_fondo_redimensionada, (600, 480))  # Mostrar la imagen de fondo en la parte inferior de la ventana
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
    Yoshis_world_font = pygame.font.Font('fonts/SuperMarioBrosWii.otf', 80).render("Yoshi's World", True, (0, 0, 0))

    font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
    mensaje_bienvenida = font.render("Bienvenid@ a ", True, (0, 0, 0))
    puntos = font.render("Puntos", True, (0, 0, 0))

    # Mostrar el mensaje de bienvenida en la parte inferior del tablero
    pantalla.blit(mensaje_bienvenida, (20, 615))
    pantalla.blit(Yoshis_world_font, (240, 605))

    # Mostrar el turno del jugador y las puntuaciones en el panel derecho
    pantalla.blit(font.render("Tu eres el Yoshi", True, (0, 0, 0)), (620, 30))
    pantalla.blit(font.render("Rojo", True, (255, 0, 0)), (700, 60))

    # Cambiar el color del texto del turno al color del Yoshi que tiene el turno
    color_turno = (0, 255, 0) if juego['turno'] == 'verde' else (255, 0, 0)
    pantalla.blit(font.render("Turno de yoshi", True, (0, 0, 0)), (630, 100))
    pantalla.blit(font.render(juego['turno'].capitalize(), True, color_turno), (700, 130))

    pantalla.blit(puntos, (630, 180))
    pantalla.blit(font.render(f"Verde: {juego['puntuacion']['verde']}", True, (0, 255, 0)), (630, 220))
    pantalla.blit(font.render(f"Rojo: {juego['puntuacion']['rojo']}", True, (255, 0, 0)), (630, 260))

    # Verificar si un Yoshi se queda sin movimientos
    if not logica.obtener_movimientos_validos(juego, juego['turno']):
        yoshi_sin_movimientos = 'verde' if juego['turno'] == 'verde' else 'rojo'
        color_sin_movimientos = (0, 255, 0) if yoshi_sin_movimientos == 'verde' else (255, 0, 0)
        yoshi_sin_movimientos_line1 = font.render(f"¡El Yoshi {yoshi_sin_movimientos.capitalize()}", True, color_sin_movimientos)
        yoshi_sin_movimientos_line2 = font.render(f" se quedó", True, color_sin_movimientos)
        yoshi_sin_movimientos_line3 = font.render(f" sin movimientos!", True, color_sin_movimientos)
        pantalla.blit(yoshi_sin_movimientos_line1, (610, 320))
        pantalla.blit(yoshi_sin_movimientos_line2, (610, 350))
        pantalla.blit(yoshi_sin_movimientos_line3, (610, 380))

    # Verificar si ningún Yoshi puede mover más
    if not logica.obtener_movimientos_validos(juego, 'verde') and not logica.obtener_movimientos_validos(juego, 'rojo'):
        fin_del_juego_texto = font.render("¡Fin del juego!", True, (0, 0, 0))
        pantalla.blit(fin_del_juego_texto, (640, 450))
        mostrar_ganador(juego, pantalla)


def mostrar_ganador(juego, pantalla):
    total_verde = juego['puntuacion']['verde']
    total_rojo = juego['puntuacion']['rojo']
    font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
    if total_verde > total_rojo:
        ganador_texto = font.render("¡Yoshi verde gana!", True, (0, 255, 0))  # Color verde
    elif total_rojo > total_verde:
        ganador_texto = font.render("¡Yoshi rojo gana!", True, (255, 0, 0))  # Color rojo
    else:
        ganador_texto = font.render("¡Empate!", True, (0, 0, 0))  # Color negro
    
    pantalla.blit(ganador_texto, (610, 500))

