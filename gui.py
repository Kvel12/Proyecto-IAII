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

    ventana.geometry("300x200")  # Establecer el tamaño de la ventana
    ventana.eval('tk::PlaceWindow . center')  # Centrar la ventana en la pantalla

    tk.Label(ventana, text="Seleccione el nivel").pack(pady=10)

    tk.Button(ventana, text="Principiante", command=lambda: set_nivel('principiante')).pack(pady=5)
    tk.Button(ventana, text="Amateur", command=lambda: set_nivel('amateur')).pack(pady=5)
    tk.Button(ventana, text="Experto", command=lambda: set_nivel('experto')).pack(pady=5)
    
    ventana.mainloop()
    return nivel

def iniciar_interfaz(juego):
    pygame.init()
    pantalla = pygame.display.set_mode((600, 750))  # Incrementar la altura de la pantalla
    pygame.display.set_caption("Yoshi's World")

    # Cargar imágenes de Yoshi
    imagen_yoshi_verde = pygame.image.load('images/YoshiVerde.png')
    imagen_yoshi_rojo = pygame.image.load('images/YoshiRojo.png')

    # Redimensionar las imágenes a 75x75 píxeles
    imagen_yoshi_verde = pygame.transform.scale(imagen_yoshi_verde, (75, 75))
    imagen_yoshi_rojo = pygame.transform.scale(imagen_yoshi_rojo, (75, 75))
    logica.movimiento_maquina(juego)  # La máquina inicia el juego

    juego_terminado = False
    while not juego_terminado:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego_terminado = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if juego["turno"] == 'rojo':
                    x, y = event.pos
                    movimiento = convertir_coordenadas_a_casilla(x, y)
                    if movimiento in logica.obtener_movimientos_validos(juego, 'rojo'):
                        logica.realizar_movimiento(juego, movimiento, 'rojo')
                        juego["turno"] = 'verde'
                        if logica.verificar_fin_juego(juego):
                            mostrar_ganador(juego)
                            juego_terminado = True
                        else:
                            logica.movimiento_maquina(juego)
                            if logica.verificar_fin_juego(juego):
                                mostrar_ganador(juego)
                                juego_terminado = True

        if not logica.obtener_movimientos_validos(juego, 'rojo') and juego["turno"] == 'rojo':
            juego["turno"] = 'verde'
            logica.movimiento_maquina(juego)

        dibujar_tablero(pantalla, juego, imagen_yoshi_verde, imagen_yoshi_rojo)
        mostrar_puntuacion(pantalla, juego)
        pygame.display.update()

def convertir_coordenadas_a_casilla(x, y):
    fila = y // 75
    columna = x // 75
    return fila, columna

def dibujar_tablero(pantalla, juego, imagen_yoshi_verde, imagen_yoshi_rojo):
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
        pantalla.blit(imagen_yoshi_verde, (j * 75, i * 75))

    # Dibujar indicador de posición actual de Yoshi rojo
    if juego["posiciones"]["rojo"] is not None:
        i, j = juego["posiciones"]["rojo"]
        pantalla.blit(imagen_yoshi_rojo, (j * 75, i * 75))

def mostrar_puntuacion(pantalla, juego):
    font = pygame.font.SysFont(None, 36)
    texto_verde = font.render(f"Verde: {juego['puntuacion']['verde']}", True, (0, 0, 0))
    texto_rojo = font.render(f"Rojo: {juego['puntuacion']['rojo']}", True, (0, 0, 0))
    
    # Crear un fondo blanco detrás de los puntajes
    fondo_puntajes = pygame.Surface((600, 50))
    fondo_puntajes.fill((255, 255, 255))
    
    # Calcular las posiciones de los puntajes
    margen_lateral = 20
    x_verde = margen_lateral
    x_rojo = fondo_puntajes.get_width() - margen_lateral - texto_rojo.get_width()
    y_puntajes = (fondo_puntajes.get_height() - texto_verde.get_height()) // 2
    
    # Crear un fondo blanco para el texto "Yoshi's World"
    fondo_titulo = pygame.Surface((600, 50))
    fondo_titulo.fill((255, 255, 255))
    
    # Renderizar el texto "Yoshi's World"
    texto_titulo = font.render("Yoshi's World", True, (0, 0, 0))
    
    # Calcular la posición del texto "Yoshi's World"
    x_titulo = (fondo_titulo.get_width() - texto_titulo.get_width()) // 2
    y_titulo = (fondo_titulo.get_height() - texto_titulo.get_height()) // 2
    
    # Crear un fondo blanco para el texto "Yoshi Verde"
    fondo_yoshi_verde = pygame.Surface((600, 50))
    fondo_yoshi_verde.fill((255, 255, 255))
    
    # Renderizar el texto "Yoshi Verde"
    texto_yoshi_verde = font.render("Yoshi Verde", True, (0, 0, 0))
    
    # Calcular la posición del texto "Yoshi Verde"
    x_yoshi_verde = (fondo_yoshi_verde.get_width() - texto_yoshi_verde.get_width()) // 2
    y_yoshi_verde = (fondo_yoshi_verde.get_height() - texto_yoshi_verde.get_height()) // 2
    
    pantalla.blit(fondo_titulo, (0, 600))  # Mostrar el fondo blanco para el título
    pantalla.blit(texto_titulo, (x_titulo, 600 + y_titulo))  # Mostrar el texto del título
    pantalla.blit(fondo_puntajes, (0, 650))  # Mostrar el fondo blanco para los puntajes
    pantalla.blit(texto_verde, (x_verde, 650 + y_puntajes))  # Mostrar puntaje verde
    pantalla.blit(texto_rojo, (x_rojo, 650 + y_puntajes))  # Mostrar puntaje rojo
    pantalla.blit(fondo_yoshi_verde, (0, 700))  # Mostrar el fondo blanco para el texto "Yoshi Verde"
    pantalla.blit(texto_yoshi_verde, (x_yoshi_verde, 700 + y_yoshi_verde))  # Mostrar el texto "Yoshi Verde"


def mostrar_ganador(juego):
    total_verde = juego['puntuacion']['verde']
    total_rojo = juego['puntuacion']['rojo']
    if total_verde > total_rojo:
        print("¡Yoshi verde gana!")
    elif total_rojo > total_verde:
        print("¡Yoshi rojo gana!")
    else:
        print("¡Empate!")
