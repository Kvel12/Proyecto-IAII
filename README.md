# Juego de Yoshi

Este proyecto implementa un juego de estrategia basado en el tablero. En este juego, dos Yoshis, uno verde y uno rojo, compiten para ocupar la mayor cantidad de casillas en un tablero de 8x8.

## Estructura del proyecto

- **main.py:** Punto de entrada del juego.
- **gui.py:** Interfaz gráfica con funciones para la selección de nivel y visualización del tablero.
- **logica.py:** Lógica del juego, incluyendo movimientos, inteligencia artificial y evaluación del tablero.
- **README.md:** Este archivo, que proporciona una visión general del proyecto y las instrucciones para ejecutarlo.

## Funcionalidades

1. **Selección de nivel:** Al iniciar el juego, se le pedirá al jugador que seleccione un nivel de dificultad.
2. **Movimientos automáticos:** El juego incluye una inteligencia artificial que controla al Yoshi verde.
3. **Indicadores de posición:** Se incluyen indicadores en forma de puntos blancos para mostrar la posición actual de los Yoshis en el tablero.
4. **Fin de juego:** El juego termina cuando ninguno de los dos Yoshis puede realizar movimientos válidos.

## Funciones en `main.py`

- **`main()`:** Punto de entrada del programa que inicia la interfaz gráfica y el ciclo principal del juego.

## Funciones en `gui.py`

- **`seleccionar_nivel()`:** Muestra una ventana para que el jugador seleccione un nivel de dificultad.
- **`iniciar_interfaz(juego)`:** Inicia la interfaz gráfica del juego y maneja los eventos del usuario.

## Funciones en `logica.py`

- **`iniciar_juego(nivel)`:** Crea un nuevo juego con el nivel seleccionado.
- **`obtener_movimientos_validos(juego, color)`:** Obtiene los movimientos válidos para un Yoshi de un color dado.
- **`realizar_movimiento(juego, movimiento, color)`:** Realiza un movimiento en el tablero.
- **`verificar_fin_juego(juego)`:** Verifica si el juego ha terminado.
- **`movimiento_maquina(juego)`:** Controla el movimiento automático del Yoshi verde.
- **`minimax(juego, profundidad, es_maximizador, alfa, beta)`:** Implementa el algoritmo Minimax con poda alfa-beta para la inteligencia artificial.
- **`evaluar_tablero(juego)`:** Evalúa el estado del tablero y retorna una puntuación.
- **`copiar_juego(juego)`:** Crea una copia profunda del estado del juego.

## Ejecución del juego

Para ejecutar el juego, simplemente ejecute el archivo `main.py` utilizando Python:

```bash
python main.py
