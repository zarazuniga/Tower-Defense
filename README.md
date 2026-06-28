# Tower-Defense
Proyecto 2

## Descripcion

Juego de estrategia por turnos para dos jugadores, hecho en Python con interfaz
grafica Tkinter. Un jugador defiende una base central construyendo torres y
muros, mientras el otro ataca enviando unidades para destruirla. Se juegan tres
rondas y gana quien gane mas rondas. El juego tiene una ambientacion de
ciberseguridad, con tres facciones (Virus, Glitch y Bots), cada una con su
propio estilo de pixel art.

## Objetivos

- Aplicar la programacion orientada a objetos en un proyecto real
- Practicar el uso de interfaces graficas con Tkinter
- Manejar el guardado y la carga de datos en archivos
- Construir la logica de un juego completo por turnos

## Integrantes

- Sebastian Hernandez
- Zara Zuñiga

## Tecnologias utilizadas

- Python 3
- Tkinter
- pygame
- JSON

## Requisitos

- Tener instalado Python 3
- Tkinter
- pygame (solo para la musica de fondo)
  

## Ejecucion

Ejecutar el archivo principal con el comando:

   python Tower_Defense_proyecto2.py

El archivo de datos se crea solo al registrar el primer jugador. Para escuchar
musica, colocar un archivo llamado musica.mp3 en la misma carpeta.

## Funcionalidades

- Registro e inicio de sesion como defensor o atacante
- Guardado de usuarios y puntajes en un archivo
- Seleccion de faccion (Virus, Glitch o Bots)
- Tablero de 10x10 con tres fases: construccion, despliegue y combate
- Combate por turnos con habilidades especiales para torres y unidades
- Sistema de rondas y condiciones de victoria
- Economia con costos, recompensas e ingreso por ronda
- Ranking global de jugadores
- Pixel art para torres, unidades, base y muros
- Musica de fondo en loop

## Estructura del proyecto

- Tower_Defense_proyecto2.py: archivo principal con la interfaz, las clases, los sprites y la
  logica del juego
- usuarios.json: datos de jugadores y puntajes (se crea automaticamente)
- musica.mp3: musica de fondo (opcional)

El codigo esta organizado en clases: Jugador, Muro, Torre, Unidad y Base para los
elementos del juego, VentanaPartida para el tablero y las fases, y
AplicacionJuego para el menu, el login y la navegacion.
