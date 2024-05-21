import gui
import logica

def main():
    nivel = gui.seleccionar_nivel()
    juego = logica.iniciar_juego(nivel)
    gui.iniciar_interfaz(juego)

if __name__ == "__main__":
    main()
