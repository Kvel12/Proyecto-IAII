import gui
import logica

# Función principal del programa
def main():
    nivel = gui.seleccionar_nivel() # Seleccionar el nivel de dificultad
    juego = logica.iniciar_juego(nivel) # Iniciar el juego
    gui.iniciar_interfaz(juego) # Iniciar la interfaz gráfica

if __name__ == "__main__":
    main()
