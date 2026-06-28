
import tkinter as tk 
from tkinter import messagebox # ventanas emergentes de tkinter
import json # libreria para leer y escribir datos en formato JSON


# musica
try: # intentam cargar pygame para el sonido, si no esta instalado o falla, el juego debe seguir funcionando igual, solo que sin sonido
    import pygame              
    pygame.mixer.init() # inicia el sistema de audio de pygame
    SONIDO_DISPONIBLE = True # se puede reproducir sonido
except Exception:
    SONIDO_DISPONIBLE = False # si algo falla, marca que NO hay sonido y el juego sigue


def reproducir_musica(nombredelarchivo): # reproduce una musica de fondo en loop
    if not SONIDO_DISPONIBLE: # si no hay sonido disponible, no hace nada
        return
    try:
        pygame.mixer.music.load(nombredelarchivo) # carga la cancion de fondo
        pygame.mixer.music.play(-1) # -1 = repetir para siempre (loop)
    except Exception:
        pass # si falla lo ignora


# archivo JSON
ARCHIVO_DATOS = "usuarios.json" # nombre del archivo donde se guardan usuarios y puntajes


def cargar_datos(): # lee el archivo JSON y devuelve dos diccionarios: usuarios y puntajes
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f: # abre el archivo para leer
            datos = json.load(f) # convierte el texto JSON a diccionario
        usuarios = datos.get("usuarios", {}) # diccionario usuario - contrasena
        puntajes = datos.get("puntajes", {}) # diccionario usuario - [victorias_def, victorias_atk]
        return usuarios, puntajes
    except (FileNotFoundError, json.JSONDecodeError):
        # FileNotFoundError: el archivo no existe todavia (primera vez que se juega)
        # json.JSONDecodeError: el archivo existe pero esta corrupto o vacio
        return {}, {} # en ambos casos arrancamos sin datos para no romper el juego


def guardar_datos(usuarios, puntajes): # guarda los usuarios y puntajes en el archivo JSON
    datos = {"usuarios": usuarios, "puntajes": puntajes} # arma un solo diccionario con todo
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f: # abre el archivo para escribir
        json.dump(datos, f, indent=4, ensure_ascii=False) # lo escribe en JSON ordenado y legible


# paleta de colores
C_FONDO       = "#0a0a1a"   
C_CYAN        = "#00ffcc"   
C_CYAN_OSC    = "#005544"   
C_AZUL        = "#0044ff"   
C_AZUL_CLARO  = "#4488ff"   
C_MORADO      = "#8800ff"   
C_MORADO_CLAR = "#aa44ff"   
C_VERDE       = "#00ff44"   
C_ROJO        = "#ff2244"   
C_GRIS        = "#1a2a3a"  
C_GRIS_CLARO  = "#2a3a4a"  
C_PANEL       = "#0d1a2a"  
C_TEXTO       = "#aabbcc"  
C_AMARILLO    = "#ffcc00" 


# facciones
FACCIONES = {
    "VIRUS": {                              
        "descripcion": "Codigo malicioso rojo",
        "torre": C_ROJO,                    
        "muro": "#5a1a1a",                  
        "base": "#aa0000",                  
        "unidad": C_ROJO,                   
    },
    "GLITCH": {                           
        "descripcion": "Datos corruptos morados",
        "torre": C_MORADO_CLAR,
        "muro": "#4a2a5a",
        "base": C_MORADO,
        "unidad": C_MORADO_CLAR,
    },
    "BOTS": {                              
        "descripcion": "Red automatizada azul",
        "torre": C_AZUL_CLARO,
        "muro": "#1a3a5a",
        "base": C_AZUL,
        "unidad": C_AZUL_CLARO,
    },
}


# sprites

# sprites pantalla inicio
SPRITE_VIRUS = [                 
    [0,0,1,1,1,0,0],
    [0,1,2,1,2,1,0],
    [0,1,1,1,1,1,0],
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [1,1,0,1,0,1,1],
    [0,1,0,0,0,1,0],
]
COL_VIRUS = {1: C_ROJO, 2: "#ff8800"}   

SPRITE_BOT = [                   
    [0,1,1,1,1,1,0],
    [1,1,2,1,2,1,1],
    [1,1,1,1,1,1,1],
    [1,2,1,1,1,2,1],
    [0,1,1,1,1,1,0],
    [0,0,1,0,1,0,0],
    [0,0,1,0,1,0,0],
]
COL_BOT = {1: C_AZUL_CLARO, 2: "#ffffff"}  

# sprites torres
SPRITES_TORRE = {
    "BOTS":{                     
        "basica": [
            [0,0,1,0,0,0,0],[0,0,1,0,0,0,0],[0,1,1,1,1,0,0],
            [0,1,2,2,1,0,0],[0,1,1,1,1,0,0],[0,1,0,0,1,0,0],[0,0,0,0,0,0,0]],
        "pesada":[
            [1,0,0,0,0,0,1],[1,0,0,0,0,0,1],[1,1,1,1,1,1,1],
            [1,2,1,2,1,2,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1],[1,0,1,0,1,0,1]],
        "magica": [
            [0,0,2,2,2,0,0],[0,2,1,1,1,2,0],[0,0,1,1,1,0,0],
            [0,1,1,1,1,1,0],[0,1,2,1,2,1,0],[0,1,1,1,1,1,0],[0,1,0,0,0,1,0]],
    },
    "VIRUS": {                   
        "basica": [
            [0,0,1,1,1,0,0],[0,1,2,2,2,1,0],[0,1,2,2,2,1,0],
            [0,1,2,2,2,1,0],[0,0,1,2,1,0,0],[0,0,0,1,0,0,0],[0,0,0,0,0,0,0]],
        "pesada": [
            [0,1,1,1,1,1,0],[1,1,2,2,2,1,1],[1,2,2,1,2,2,1],
            [1,2,1,1,1,2,1],[1,2,2,1,2,2,1],[0,1,2,2,2,1,0],[0,0,1,1,1,0,0]],
        "magica": [
            [0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,2,2,2,1,1],
            [1,1,2,3,2,1,1],[1,1,2,2,2,1,1],[0,1,1,1,1,1,0],[0,0,1,1,1,0,0]],
    },
    "GLITCH":{                   
        "basica": [
            [0,0,0,0,0,0,0],[0,1,1,0,1,1,0],[0,1,2,0,2,1,0],
            [0,0,0,1,0,0,0],[0,1,2,0,2,1,0],[0,1,1,0,1,1,0],[0,0,0,0,0,0,0]],
        "pesada": [
            [1,1,0,1,1,1,0],[1,2,1,1,2,1,1],[0,1,1,2,1,1,0],
            [1,1,2,1,2,1,1],[0,1,1,2,1,1,0],[1,2,1,1,2,1,1],[1,1,0,1,1,0,1]],
        "magica": [
            [0,1,0,1,0,1,0],[1,1,2,1,2,1,1],[0,2,1,1,1,2,0],
            [1,1,1,2,1,1,1],[0,2,1,1,1,2,0],[1,1,2,1,2,1,1],[0,1,0,1,0,1,0]],
    },
}


COLOR_SPRITE_TORRE = {
    "VIRUS": {1: "#FF2244", 2: "#FF8800", 3: "#FFFFFF"},
    "GLITCH": {1: "#AA44FF", 2: "#FFFFFF"},
    "BOTS": {1: "#4488FF", 2: "#FFFFFF"},
}

# sprites enemigos
SPRITES_ENEMIGO = {
    "VIRUS": {
        "replicante": {"sprite": [
            [0,0,1,1,1,0,0],[0,1,2,1,2,1,0],[0,1,1,1,1,1,0],
            [0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,0,1,0,1,1],[0,1,0,0,0,1,0]],
            "colores": {1:"#ff2244", 2:"#ff8800"}},
        "pesada": {"sprite": [
            [1,1,1,1,1,1,1],[1,2,1,1,1,2,1],[1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1],[1,2,1,1,1,2,1],[1,1,1,1,1,1,1],[1,1,1,1,1,1,1]],
            "colores": {1:"#ff2244", 2:"#ff8800"}},
        "rapida": {"sprite": [
            [0,1,1,1,0,0,0],[1,2,1,2,1,0,0],[0,1,1,1,1,1,0],
            [0,0,0,1,2,1,1],[0,0,0,1,1,1,0]],
            "colores": {1:"#00ff44", 2:"#ff2244"}},
    },
    "GLITCH": {
        "replicante": {"sprite": [
            [0,1,1,0,1,1,0],[1,2,1,1,1,2,1],[0,1,1,1,1,1,0],
            [1,1,0,1,0,1,1],[0,1,1,1,1,1,0],[0,2,1,0,1,2,0],[0,1,0,0,0,1,0]],
            "colores": {1:"#aa44ff", 2:"#ffffff"}},
        "pesada": {"sprite": [
            [1,1,1,1,1,1,1],[1,2,2,1,2,2,1],[1,2,1,1,1,2,1],
            [1,1,1,1,1,1,1],[1,2,1,1,1,2,1],[1,1,2,1,2,1,1],[1,1,1,1,1,1,1]],
            "colores": {1:"#aa44ff", 2:"#000000"}},
        "rapida": {"sprite": [
            [0,0,1,1,1,0,0],[0,1,2,1,2,1,0],[1,1,1,1,1,1,1],
            [0,1,1,1,1,1,0],[0,0,1,0,1,0,0]],
            "colores": {1:"#aa44ff", 2:"#ffffff"}},
    },
    "BOTS": {
        "replicante": {"sprite": [
            [0,1,1,1,1,1,0],[1,1,2,1,2,1,1],[1,1,1,1,1,1,1],
            [1,2,1,1,1,2,1],[0,1,1,1,1,1,0],[0,0,1,0,1,0,0],[0,0,1,0,1,0,0]],
            "colores": {1:"#4488ff", 2:"#ffffff"}},
        "pesada": {"sprite": [
            [1,0,1,1,1,0,1],[1,1,1,1,1,1,1],[1,2,1,1,1,2,1],
            [1,1,1,1,1,1,1],[1,2,1,1,1,2,1],[1,1,1,1,1,1,1],[1,0,1,1,1,0,1]],
            "colores": {1:"#0044ff", 2:"#4488ff"}},
        "rapida": {"sprite": [
            [0,0,1,1,1,0,0],[0,1,1,1,1,1,0],[1,1,2,2,2,1,1],
            [0,1,1,1,1,1,0],[0,0,1,1,1,0,0]],
            "colores": {1:"#4488ff", 2:"#ffffff"}},
    },
}

# sprite base central
SPRITE_BASE = [
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [1,1,2,3,2,2,4,4,2,2,3,2,1,1],
    [1,1,2,2,2,2,4,4,2,2,2,2,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [1,1,3,3,3,3,3,3,3,3,3,3,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [1,1,2,4,4,4,4,4,4,4,4,2,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [1,1,2,3,2,3,2,3,2,3,2,3,1,1],
    [1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
]

COLOR_SPRITE_BASE = {
    "VIRUS":  {1:"#3a1a1a", 2:"#0a0505", 3:"#ff2244", 4:"#ff8800"},
    "GLITCH": {1:"#2a1a3a", 2:"#08040a", 3:"#aa44ff", 4:"#ffffff"},
    "BOTS":   {1:"#1a2a3a", 2:"#04080a", 3:"#4488ff", 4:"#00ffcc"},
}

# sprite muros
SPRITE_MURO = [
    [2,2,2,2,2,2,2],
    [4,4,4,4,4,4,4],
    [2,2,2,2,2,2,2],
    [3,3,3,3,3,3,3],
    [2,2,2,2,2,2,2],
    [4,4,4,4,4,4,4],
    [2,2,2,2,2,2,2],
]

COLOR_SPRITE_MURO = {
    "VIRUS":  {2:"#3a0d0d", 3:"#ff6644", 4:"#ff8800"},
    "GLITCH": {2:"#2a1040", 3:"#cc88ff", 4:"#ffffff"},
    "BOTS":   {2:"#0d2040", 3:"#66bbff", 4:"#00ffcc"},
}


def dibujar_pixel(canvas, ox, oy, sprite, px, colores):
    # dibuja un sprite sobre el lienzo, empezando en la esquina (ox, oy)
    # px es el tamano en pixeles de cada cuadradito y colores dice que color es cada numero
    for fi, fila in enumerate(sprite): # recorre cada fila de la matriz
        for ci, v in enumerate(fila): # recorre cada valor de la fila
            if v and v in colores: # solo dibuja si el valor no es 0 y tiene color asignado
                canvas.create_rectangle(
                    ox + ci*px, oy + fi*px, # esquina superior izquierda del cuadradito
                    ox + ci*px + px, oy + fi*px + px, # esquina inferior derecha
                    fill=colores[v], outline="") # lo pinta del color correspondiente sin borde



# dibujos
def dibujar_estrellas(canvas):
    puntos = [  # lista de estrellas: cada una es (x, y, tamano)
        (60,420,1),(180,390,2),(350,410,1),(500,380,2),(700,400,1),
        (850,415,2),(1000,385,1),(1150,405,2),(1300,395,1),(1450,420,2),
        (120,260,1),(430,245,2),(780,255,1),(1050,240,2),(1380,250,1),
        (250,150,2),(600,130,1),(950,160,2),(1250,140,1),
    ]
    for px, py, pt in puntos: # para cada estrella (posicion px,py y tamano pt)...
        canvas.create_rectangle(px, py, px+pt, py+pt, fill=C_AZUL_CLARO, outline="") # ...la dibuja


def dibujar_suelo(canvas):
    canvas.create_rectangle(0, 780, 1500, 840, fill=C_PANEL, outline="")        
    canvas.create_rectangle(0, 780, 1500, 783, fill=C_GRIS_CLARO, outline="")   
    canvas.create_rectangle(0, 837, 1500, 840, fill=C_GRIS_CLARO, outline="")   
    for x in range(0, 1500, 40):                                                
        canvas.create_rectangle(x, 809, x+20, 811, fill=C_GRIS_CLARO, outline="")


def dibujar_torre(canvas, tx, ty, color_top):
    canvas.create_rectangle(tx, ty+60, tx+50, ty+90, fill=C_GRIS, outline="")         
    canvas.create_rectangle(tx, ty+60, tx+50, ty+63, fill=C_AZUL_CLARO, outline="")   
    canvas.create_rectangle(tx+8, ty+20, tx+42, ty+60, fill=C_GRIS, outline="")       
    canvas.create_rectangle(tx+8, ty+20, tx+42, ty+23, fill=color_top, outline="")    
    canvas.create_rectangle(tx+20, ty, tx+30, ty+20, fill=color_top, outline="")      
    canvas.create_rectangle(tx+16, ty+32, tx+34, ty+48, fill=C_CYAN_OSC, outline="")  
    canvas.create_rectangle(tx+18, ty+34, tx+32, ty+46, fill=color_top, outline="")   


def dibujar_servidor(canvas):
    sx, sy = 680, 680             
    canvas.create_rectangle(sx, sy, sx+140, sy+90, fill="#0a1a2a", outline="")       
    canvas.create_rectangle(sx, sy, sx+140, sy+4,  fill=C_AZUL_CLARO, outline="")    
    canvas.create_rectangle(sx, sy+44, sx+140, sy+48, fill=C_GRIS_CLARO, outline="") 
    for i, col in enumerate([C_VERDE, C_CYAN, C_VERDE, C_CYAN, C_VERDE]):           
        canvas.create_rectangle(sx+8+i*24, sy+10, sx+18+i*24, sy+18, fill=col, outline="")
    canvas.create_rectangle(sx+8, sy+54, sx+60, sy+60, fill=C_AZUL, outline="")      
    canvas.create_rectangle(sx+70, sy+54, sx+132, sy+60, fill=C_AZUL, outline="")   
    canvas.create_rectangle(sx+8, sy+66, sx+132, sy+72, fill=C_GRIS_CLARO, outline="")  


def dibujar_escena_completa(canvas):
    # Dibuja todo el fondo decorativo de la pantalla de inicio 
    dibujar_estrellas(canvas)                                  
    dibujar_suelo(canvas)                                      
    dibujar_servidor(canvas)                                   
    dibujar_torre(canvas, 200, 650, C_CYAN)                   
    dibujar_torre(canvas, 1250, 650, C_MORADO_CLAR)            
    dibujar_pixel(canvas, 80, 795, SPRITE_VIRUS, 5, COL_VIRUS) 
    dibujar_pixel(canvas, 1360, 795, SPRITE_BOT, 5, COL_BOT)   

def dibujar_fondo_simple(canvas):
    # Dibuja un fondo decorativo mas simple para las pantallas internas sin servidor ni torres
    dibujar_estrellas(canvas)                                  
    dibujar_suelo(canvas)                                      
    dibujar_pixel(canvas, 80, 795, SPRITE_VIRUS, 5, COL_VIRUS)
    dibujar_pixel(canvas, 1360, 795, SPRITE_BOT, 5, COL_BOT) 

# clases
class Jugador:
    def __init__(self, nombre, contraseña, victorias_defensor=0, victorias_atacante=0):
        self.nombre = nombre # nombre de usuario
        self.contraseña = contraseña # contrasena del usuario
        self.victorias_defensor = victorias_defensor # cuantas veces gano como defensor
        self.victorias_atacante = victorias_atacante # cuantas veces gano como atacante
        self.dinero = 0 # dinero disponible en la partida actual

    def recibir_dinero(self, cantidad): # le suma dinero al jugador 
        self.dinero += cantidad

    def puede_pagar(self, costo): # devuelve True si el jugador tiene dinero suficiente para pagar costo
        return self.dinero >= costo

    def gastar(self, costo): # intenta gastar dinero si alcanza, lo resta y devuelve True si no, devuelve False
        if self.puede_pagar(costo):
            self.dinero -= costo
            return True
        return False

    def sumar_victoria_defensor(self): # suma una victoria como defensor
        self.victorias_defensor += 1

    def sumar_victoria_atacante(self): # suma una victoria como atacante
        self.victorias_atacante += 1


class Muro: # representa un muro defensivo
    def __init__(self):
        self.tipo = "muro"        
        self.vida = 120           
        self.vida_maxima = 120    

    def recibir_daño(self, cantidad): # le baja vida al muro cuando lo atacan
        self.vida -= cantidad
        if self.vida < 0:         
            self.vida = 0

    def esta_vivo(self): # devuelve True si el muro todavia tiene vida
        return self.vida > 0


class Torre: # representa una torre defensiva. segun su tipo tiene distintas estadisticas y habilidad
    def __init__(self, tipo):
        self.tipo = tipo # tipo de torre: basica, pesada o magica

        if tipo == "basica": # torre basica
            self.nombre = "Torre Basica"
            self.costo = 50
            self.vida= 100
            self.daño = 15
            self.alcance = 2
            self.habilidad = "Disparo doble"
            self.turnos_habilidad = 3

        elif tipo == "pesada": # torre pesada
            self.nombre = "Torre Pesada"
            self.costo = 150
            self.vida= 300
            self.daño = 30
            self.alcance = 1
            self.habilidad = "Daño en Area"
            self.turnos_habilidad = 4

        elif tipo == "magica": # torre magica
            self.nombre = "Torre Magica"
            self.costo = 100
            self.vida= 80
            self.daño = 10
            self.alcance = 3
            self.habilidad = "Congelar Unidad"
            self.turnos_habilidad = 5

        self.vida_maxima = self.vida  # guarda la vida maxima para barra de vuda
        self.contador_turnos = 0 # cuenta turnos para saber cuando activar la habilidad

    def recibir_daño(self, cantidad): # baja vida a la torre cuando la atacan
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_viva(self): # la torre todavia tiene vida
        return self.vida > 0

    def pasar_turno(self): # suma un turno al contador y devuelve True si ya toca activar la habilidad
        self.contador_turnos += 1
        return self.contador_turnos >= self.turnos_habilidad

    def activar_habilidad(self, unidades_en_rango): # activa la habilidad especial de la torre sobre las unidades que tenga en rango
        self.contador_turnos = 0  # rerinicia el contador despues de usar la habilidad

        if self.tipo == "basica": # disparo doble
            if unidades_en_rango:
                unidades_en_rango[0].recibir_daño(self.daño * 2)
            return "Disparo doble: " + str(self.daño * 2) + " de daño"

        elif self.tipo == "pesada": # dano en area
            for u in unidades_en_rango:
                u.recibir_daño(self.daño)
            return "Daño en area a " + str(len(unidades_en_rango)) + " unidades"

        elif self.tipo == "magica": # congelar
            if unidades_en_rango:
                unidades_en_rango[0].congelado = True
            return "Unidad congelada"



class Unidad: # representa una unidad atacante segun su tipo tiene distintas estadisticas y habilidad
    def __init__(self, tipo, nombre=None):
        self.tipo = tipo # tipo de unidad: replicante, pesada o rapida

        if tipo == "replicante": # replicante
            self.nombre = nombre
            self.costo = 50
            self.vida= 100
            self.daño = 15
            self.velocidad = 2
            self.habilidad = "Replicarse"
            self.turnos_habilidad = 3

        elif tipo == "pesada": # pesada
            self.nombre = nombre
            self.costo = 150
            self.vida= 400
            self.daño = 30
            self.velocidad = 1
            self.habilidad = "Sobrecarga"
            self.turnos_habilidad = 4

        elif tipo == "rapida": # rapida
            self.nombre = nombre
            self.costo = 75
            self.vida= 60
            self.daño = 10
            self.velocidad = 4
            self.habilidad = "Bypass"
            self.turnos_habilidad = 2

        self.vida_maxima = self.vida # vida maxima
        self.contador_turnos = 0 # cuenta turnos para activar la habilidad
        self.ignora_muro = False # si esta en True atraviesa el proximo muro
        self.fila = None # fila donde esta en el tablero
        self.columna = None # columna donde esta en el tablero
        self.congelado = False # si esta en True pierde el movimiento de este turno
        self.ya_se_replico = False # si esta en True ya no puede volver a replicarse

    def recibir_daño(self, cantidad): # le baja vida a la unidad cuando la atacan
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_viva(self): # devuelve True si la unidad todavia tiene vida
        return self.vida > 0

    def pasar_turno(self): # suma un turno al contador y devuelve True si ya toca activar la habilidad
        self.contador_turnos += 1
        return self.contador_turnos >= self.turnos_habilidad

    def activar_habilidad(self, torres_en_rango=None): # activa la habilidad especial de la unidad segun su tipo
        self.contador_turnos = 0  # reinicia el contador

        if self.tipo == "replicante": # replicarse: crea 1 copia con poca vida
            if self.ya_se_replico: # si ya se replico antes no lo hace de nuevo
                return None
            self.ya_se_replico = True # marca que esta original ya uso su copia
            copia = Unidad("replicante", self.nombre + "(copia)") # crea la copia
            copia.vida = 30 # la copia nace con poca vida
            copia.vida_maxima = 30
            copia.ya_se_replico = True # la copia nace marcada no se puede replicar
            return copia # devuelve la copia para agregarla al tablero

        elif self.tipo == "pesada": # sobrecarga
            if torres_en_rango:
                for t in torres_en_rango:
                    t.recibir_daño(self.daño)
            return "Sobrecarga a las torres en rango"

        elif self.tipo == "rapida": # bypass
            self.ignora_muro = True
            return "Bypass activado: ignora el proximo muro"


class Base: # base central
    def __init__(self, faccion = "VIRUS"):
        self.vida = 500 # vida total de la base
        self.vida_maxima = 500 # vida maxima
        self.faccion = faccion # faccion del defensor

    def recibir_daño(self, cantidad): # le baja vida a la base cuando la atacan
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_viva(self): # devuelve True si la base todavia tiene vida
        return self.vida > 0


# tablero
FILAS = 10 # filas del tablero
COLUMNAS = 10 # columnas del tablero
TAM = 56 # tamano en pixeles de cada casilla
ORIGEN_X = 40 # coordenada X donde empieza el tablero en el lienzo
ORIGEN_Y = 90 # coordenada Y donde empieza el tablero en el lienzo

COSTO_MURO = 20 # cuanto cuesta un muro
COSTO_UNIDAD_MIN = 50 # costo de la unidad mas barata


# economia
DINERO_INICIAL = 300 # dinero con el que arrancan ambos jugadores 
INGRESO_POR_RONDA = 150 # dinero que reciben al inicio de cada ronda nueva

RECOMPENSA_DEF_POR_UNIDAD = {"replicante": 25, "pesada": 75, "rapida": 35} # dinero que gana el defensor por eliminar cada tipo de unidad

RECOMPENSA_ATK_POR_TORRE = {"basica": 25, "pesada": 75, "magica": 50} # dinero que gana el atacante por destruir cada tipo de torre

RECOMPENSA_ATK_POR_GOLPE_TORRE = 2 # dinero que gana el atacante por cada golpe a una torre
RECOMPENSA_ATK_POR_GOLPE_BASE = 3 # dinero que gana el atacante por cada golpe a la base

RONDAS_POR_PARTIDA = 3 # cuantas rondas se juegan en total por partida
MAX_TURNOS_COMBATE = 60 # limite de turnos del combate para que la ronda no sea infinita


# funciones
def distancia_alcance_torre(f1, c1, f2, c2): # distancia"Manhattan: cuantos pasos hay entre dos casillas (sin diagonales)
    return abs(f1-f2) + abs(c1 - c2)


def celdas_base(cuadricula): # devuelve la lista de casillas (fila, col) que forman la base central
    lista = []
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if cuadricula[f][c] == "base": # La base se guarda como el texto "base"
                lista.append((f,c))
    return lista


def base_mas_cercana(fil, col, cuadricula): # devuelve la casilla de la base mas cercana a la posicion (fil, col)
    bases = celdas_base(cuadricula)
    if not bases: # si por alguna razon no hay base, apunta al centro
        return (FILAS // 2, COLUMNAS // 2) # elige la casilla de base con menor distancia respecto a (fil, col)
    return min(bases, key = lambda b: distancia_alcance_torre(fil,col, b[0], b[1]))


def siguiente_paso(fil, col, cuadricula): # calcula la siguiente casilla hacia la que se debe mover una unidad para acercarse a la base
    of, oc = base_mas_cercana(fil, col, cuadricula) # posicion objetivo
    df = of - fil # cuanto falta en filas
    dc = oc - col # cuanto falta en columnas

    # si falta mas camino vertical se mueve en vertical sino en horizontal
    if abs(df) >= abs(dc) and df != 0:
        paso_fila = 1 if df > 0 else -1 # decide si baja o sube 
        return (fil + paso_fila, col)
    elif dc!= 0:
        paso_col = 1 if dc > 0 else -1 # decide si va a la derecha o izquierda 
        return (fil, col + paso_col)
    else:
        return (fil,col) # ya esta en la base no se mueve


def dentro_del_tablero(fil, col): # devuelve True si la casilla (fil, col) esta dentro de los limites del tablero 
    return 0 <= fil < FILAS and 0 <= col <COLUMNAS

#clase ventada partida
class VentanaPartida:
    def __init__(self, app, nombre_def, nombre_atk, faccion_def, faccion_atk):
        # guarda la informacion de la partida y prepara todo para empezar
        self.app = app # referencia a la aplicacion principal
        self.nombre_def = nombre_def # nombre del jugador defensor
        self.nombre_atk = nombre_atk # nombre del jugador atacante
        self.faccion_def = faccion_def # faccion del defensor 
        self.faccion_atk = faccion_atk # faccion del atacante


        # crea los objetos Jugador para defensor y atacante y les da su dinero inicial
        self.jugador_def = Jugador(nombre_def, "")
        self.jugador_atk = Jugador(nombre_atk, "")
        self.jugador_def.recibir_dinero(DINERO_INICIAL)
        self.jugador_atk.recibir_dinero(DINERO_INICIAL)

        # estado general de la partida
        self.ronda = 1 # numero de ronda actual
        self.vict_def = 0 # rondas ganadas por el defensor
        self.vict_atk = 0 # rondas ganadas por el atacante
        self.fase = "construccion" # fase actual
        self.turno = 0 # Numero de turno dentro del combate
        self.daño_base_ronda = 0 # dano total que recibio la base en la ronda
        self.auto_activo = False # si el modo automatico del combate esta activo

        # herramientas
        self.herramienta = "muro" # lo que el defensor va a colocar
        self.tipo_unidad_sel = "replicante" # la unidad que el atacante va a colocar

        # estado tablero
        self.cuadricula = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)] 
        self.unidades = [] # lista de unidades atacantes en el mapa.
        self.base = Base(self.faccion_def)  # objeto base central

        # crea la ventana de la partida
        self.ventana = tk.Toplevel(self.app.ventana_principal)
        self.ventana.title("Partida")
        self.ventana.geometry("1040x760")
        self.ventana.configure(bg = C_FONDO)
        self.ventana.resizable(False, False)   

        self._colocar_base() # marca las 4 casillas centrales como base
        self._construir_ui() # crea el lienzo del tablero y el panel lateral
        self._ir_a_fase("construccion") # arranca en la fase de construccion del defensor

    def _colocar_base(self): # marca el bloque 2x2 del centro del tablero como base central
        for f in (4,5):
            for c in (4,5):
                self.cuadricula[f][c] = "base"

    def _limpiar_tablero_para_nueva_ronda(self): # vacia el tablero y reinicia la base para empezar una ronda nueva
        self.cuadricula = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self._colocar_base() # vuelve a poner la base en el centro
        self.unidades = [] # borra las unidades de la ronda anterior
        self.base = Base(self.faccion_def) # crea una base nueva con vida llena
        self.turno = 0 # reinicia el contador de turnos
        self.daño_base_ronda = 0 # reinicia el dano acumulado a la base

    def _construir_ui(self): # crea el lienzo del tablero y el panel de control 
        self.canvas = tk.Canvas(self.ventana, width= 620, height= 680,  bg= C_FONDO, highlightthickness= 0)
        self.canvas.place (x=0, y= 0)
        self.canvas.bind("<Button-1>", self._click) # conecta el clic izquierdo con el metodo _click

        # panel de control de la derecha
        self.panel = tk.Frame(self.ventana, width= 380, height= 740, bg= C_PANEL, highlightthickness= 0)
        self.panel.place (x= 630, y= 10)
        self.panel.pack_propagate(False) # evita que el panel cambie de tamano segun su contenido

    def _limpiar_panel(self): # borra todos los widgets del panel
        for w in self.panel.winfo_children():
            w.destroy()

    def _ir_a_fase(self, fase): # cambia a una fase del juego y arma el panel correspondiente
        self.fase = fase
        if fase == "construccion":
            # si el defensor no tiene ni para el muro mas barato no puede defender entc pierde la ronda
            if self._defensor_sin_recursos():
                self._dibujar_tablero()
                self._fin_ronda("atacante")
                return
            self._panel_construccion()
        elif fase == "ataque":
            # si el atacante no tiene unidades ni dinero para desplegar no puede atacar entc pierde la ronda
            if self._atacante_sin_recursos():
                self._dibujar_tablero()
                self._fin_ronda("defensor")
                return
            self._panel_ataque()
        elif fase == "combate":
            self._panel_combate()
        self._dibujar_tablero() # redibuja el tablero al cambiar de fase

    def _defensor_sin_recursos(self): # el defensor no puede defender si no le alcanza ni para el muro mas barato
        return not self.jugador_def.puede_pagar(COSTO_MURO)

    def _atacante_sin_recursos(self): # el atacante no puede atacar si no tiene unidades vivas y tampoco dinero para la mas barata
        hay_unidades_vivas = any(u.esta_viva() for u in self.unidades)
        return (not hay_unidades_vivas) and (not self.jugador_atk.puede_pagar(COSTO_UNIDAD_MIN))

    def _panel_construccion(self): # arma el panel derecho de la fase de construccion
        self._limpiar_panel()

        # encabezados con la rond, fase, defensor y faccion
        tk.Label(self.panel, text="RONDA " + str(self.ronda), font=("Courier", 16, "bold"),fg=C_AMARILLO, bg=C_PANEL).pack(pady=(14, 2))
        tk.Label(self.panel, text="FASE DE CONSTRUCCION", font=("Courier", 13, "bold"),fg=C_CYAN, bg=C_PANEL).pack()
        tk.Label(self.panel, text="DEFENSOR: " + self.nombre_def,font=("Courier", 10), fg=C_AZUL_CLARO, bg=C_PANEL).pack()
        tk.Label(self.panel, text="Faccion: " + self.faccion_def,font=("Courier", 9, "italic"), fg=C_TEXTO, bg=C_PANEL).pack()

        # etiqueta que muestra el dinero del defensor
        self.lbl_dinero = tk.Label(self.panel, text="", font=("Courier", 17, "bold"),fg=C_VERDE, bg=C_PANEL)
        self.lbl_dinero.pack(pady=10)

        tk.Label(self.panel, text="QUE QUERES COLOCAR?", font=("Courier", 10, "bold"),fg=C_CYAN, bg=C_PANEL).pack(pady=(4, 6))

        # lista de cosas que puede colocar
        opciones = [
            ("MURO  ", "muro", COSTO_MURO),
            ("TORRE BASICA  ", "basica", 50),
            ("TORRE PESADA  ", "pesada", 150),
            ("TORRE MAGICA  ", "magica", 100),
        ]

        self.botones = {} # se guardan los botones para poder resaltarlos
        for texto, herram, costo in opciones: # crea un boton por cada opcion
            b = tk.Button(self.panel, text=texto + str(costo),font=("Courier", 11, "bold"), width=22, height=1,relief="flat", bd=0,command=lambda h=herram: self._seleccionar_herramienta(h))
            b.pack(pady=3)
            self.botones[herram] = b

        # boton para borrar
        b_borrar = tk.Button(self.panel, text="BORRAR (devuelve dinero)",font=("Courier", 11, "bold"), width=22, height=1,relief="flat", bd=0,command=lambda: self._seleccionar_herramienta("borrar"))
        b_borrar.pack(pady=(10, 4))
        self.botones["borrar"] = b_borrar

        # etiqueta de avisos
        self.lbl_aviso = tk.Label(self.panel, text="Hace clic en una casilla",font=("Courier", 9, "italic"), fg=C_AZUL_CLARO,bg=C_PANEL, wraplength=320)
        self.lbl_aviso.pack(pady=10)

        # boton para terminar la construccion y pasar a la fase del atacante
        tk.Button(self.panel, text="TERMINAR CONSTRUCCION >>",font=("Courier", 11, "bold"), width=24, height=1,relief="flat", bd=0, fg=C_FONDO, bg=C_VERDE,command=self._terminar_construccion).pack(pady=(8, 4))

        # marcador de rondas ganadas
        self.lbl_marcador = tk.Label(self.panel, text="", font=("Courier", 10),fg=C_TEXTO, bg=C_PANEL)
        self.lbl_marcador.pack(pady=6)

        self._seleccionar_herramienta("muro") # deja el muro seleccionado por defecto
        self._actualizar_marcadores() # actualiza los textos de dinero y marcador

    def _panel_ataque(self): # arma el panel derecho de la FASE DE DESPLIEGUE
        self._limpiar_panel()

        # encabezados con la ronda, fase, el atacante y su faccion
        tk.Label(self.panel, text="RONDA " + str(self.ronda), font=("Courier", 16, "bold"),fg=C_AMARILLO, bg=C_PANEL).pack(pady=(14, 2))
        tk.Label(self.panel, text="FASE DE DESPLIEGUE", font=("Courier", 13, "bold"),fg=C_MORADO_CLAR, bg=C_PANEL).pack()
        tk.Label(self.panel, text="ATACANTE: " + self.nombre_atk,font=("Courier", 10), fg=C_AZUL_CLARO, bg=C_PANEL).pack()
        tk.Label(self.panel, text="Faccion: " + self.faccion_atk,font=("Courier", 9, "italic"), fg=C_TEXTO, bg=C_PANEL).pack()

        # etiqueta que muestra el dinero del atacante.
        self.lbl_dinero = tk.Label(self.panel, text="", font=("Courier", 17, "bold"),fg=C_VERDE, bg=C_PANEL)
        self.lbl_dinero.pack(pady=10)

        tk.Label(self.panel, text="QUE UNIDAD QUERES?", font=("Courier", 10, "bold"),fg=C_MORADO_CLAR, bg=C_PANEL).pack(pady=(4, 6))


        # lista de unidades que puede desplegar texto, tipo, costo
        opciones = [
            ("REPLICANTE  ", "replicante", 50),
            ("PESADA (Tanque)  ", "pesada", 150),
            ("RAPIDA  ", "rapida", 75),
        ]
        self.botones = {}
        for texto, tipo, costo in opciones:    # crea un boton por cada unidad
            b = tk.Button(self.panel, text=texto + str(costo),font=("Courier", 11, "bold"), width=22, height=1,relief="flat", bd=0,command=lambda t=tipo: self._seleccionar_unidad(t))
            b.pack(pady=3)
            self.botones[tipo] = b

        # boton para quitar una unidad ya colocada y devolver su dinero
        b_borrar = tk.Button(self.panel, text="QUITAR (devuelve dinero)",font=("Courier", 11, "bold"), width=22, height=1,relief="flat", bd=0,command=lambda: self._seleccionar_unidad("borrar"))
        b_borrar.pack(pady=(10, 4))
        self.botones["borrar"] = b_borrar

        # etiqueta de avisos para el atacante
        self.lbl_aviso = tk.Label(self.panel,text="Coloca tus unidades en las 2 columnas de cada borde lateral.",font=("Courier", 9, "italic"), fg=C_AZUL_CLARO,bg=C_PANEL, wraplength=320)
        self.lbl_aviso.pack(pady=10)

        # boton para iniciar el combate
        tk.Button(self.panel, text="INICIAR COMBATE >>",font=("Courier", 11, "bold"), width=24, height=1,relief="flat", bd=0, fg=C_FONDO, bg=C_ROJO,command=self._terminar_despliegue).pack(pady=(8, 4))

        self.lbl_marcador = tk.Label(self.panel, text="", font=("Courier", 10),fg=C_TEXTO, bg=C_PANEL)
        self.lbl_marcador.pack(pady=6)

        self._seleccionar_unidad("replicante") # deja la replicante seleccionada por defecto
        self._actualizar_marcadores()

    def _panel_combate(self): # arma el panel derecho de la FASE DE COMBATE
        self._limpiar_panel()

        tk.Label(self.panel, text="RONDA " + str(self.ronda), font=("Courier", 16, "bold"),fg=C_AMARILLO, bg=C_PANEL).pack(pady=(14, 2))
        tk.Label(self.panel, text="COMBATE", font=("Courier", 14, "bold"),fg=C_ROJO, bg=C_PANEL).pack()

        # etiqueta con la vida de la base
        self.lbl_base = tk.Label(self.panel, text="", font=("Courier", 12, "bold"),fg=C_VERDE, bg=C_PANEL)
        self.lbl_base.pack(pady=(12, 2))

        # etiqueta con el turno actual y las unidades vivas
        self.lbl_turno = tk.Label(self.panel, text="", font=("Courier", 11),fg=C_CYAN, bg=C_PANEL)
        self.lbl_turno.pack(pady=2)

        # etiquetas con el dinero de ambos jugadores
        self.lbl_dinero_def = tk.Label(self.panel, text="", font=("Courier", 10),fg=C_CYAN, bg=C_PANEL)
        self.lbl_dinero_def.pack(pady=2)
        self.lbl_dinero_atk = tk.Label(self.panel, text="", font=("Courier", 10),fg=C_MORADO_CLAR, bg=C_PANEL)
        self.lbl_dinero_atk.pack(pady=2)

        # boton para avanzar 1 turno manualmente
        tk.Button(self.panel, text="SIGUIENTE TURNO",font=("Courier", 12, "bold"), width=22, height=1,relief="flat", bd=0, fg=C_FONDO, bg=C_CYAN,command=self._siguiente_turno).pack(pady=(14, 4))

        # boton para activar o pausar el modo automatico
        self.btn_auto = tk.Button(self.panel, text="AUTO (jugar solo)",font=("Courier", 11, "bold"), width=22, height=1,relief="flat", bd=0, fg=C_FONDO, bg=C_AMARILLO,command=self._alternar_auto)
        self.btn_auto.pack(pady=4)

        # registro del ultimo evento del combate
        self.lbl_log = tk.Label(self.panel, text="Comienza el combate...",font=("Courier", 9), fg=C_TEXTO, bg=C_PANEL,wraplength=320, justify="left", height=4)
        self.lbl_log.pack(pady=10)

        self.lbl_marcador = tk.Label(self.panel, text="", font=("Courier", 10),fg=C_TEXTO, bg=C_PANEL)
        self.lbl_marcador.pack(pady=6)
        self._actualizar_marcadores()

        # el combate arranca pausado, el jugador decide ir turno por turno o activar el modo auto
        self.auto_activo = False
        self.btn_auto.config(text="AUTO (jugar solo)", bg=C_AMARILLO)

    def _dibujar_tablero(self): # dibuja el tablero
        self.canvas.delete("all") # borra el dibujo anterior antes de redibujar

        # colores de las facciones elegidas por los jugadores
        Col_torre = FACCIONES[self.faccion_def]["torre"]
        Col_muro = FACCIONES[self.faccion_def]["muro"]
        Col_base = FACCIONES[self.faccion_def]["base"]
        Col_unidad = FACCIONES[self.faccion_atk]["unidad"]

        # titulo arriba del tablero segun la fase
        titulo = {"construccion": "CONSTRUI TU DEFENSA","ataque": "COLOCA TUS UNIDADES","combate": "TURNO " + str(self.turno)}.get(self.fase,"")
        self.canvas.create_text(ORIGEN_X, 50, text=titulo, anchor="w", font=("Courier", 15, "bold"), fill=C_CYAN)

        # recorre todas las casillas del tablero para dibujarlas
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = ORIGEN_X + col * TAM # coordenada X de la esquina de la casilla
                y1 = ORIGEN_Y + fila * TAM # coordenada Y de la esquina de la casilla
                x2, y2 = x1 + TAM, y1 + TAM # esquina opuesta de la casilla
                contenido = self.cuadricula[fila][col] # que hay en esa casilla

                # en la fase de ataque las zonas de despliegue se pintan de otro color
                if self.fase == "ataque" and self._es_zona_despliegue(fila, col) \
                        and contenido is None:
                    fondo = C_GRIS_CLARO
                else:
                    fondo = C_FONDO
                self.canvas.create_rectangle(x1,y1,x2,y2, fill=fondo, outline=C_GRIS, width=1) # dibuja la casilla

                # dibuja lo que haya en la casilla
                if contenido == "base":
                    self._dibujar_relleno(x1,y1,x2,y2, Col_base, "") # la base se dibuja completa mas abajo
                elif isinstance(contenido, Muro):
                    # muro
                    colores_muro = COLOR_SPRITE_MURO[self.faccion_def]
                    dibujar_pixel(self.canvas, x1 + 4, y1 + 6, SPRITE_MURO, 7, colores_muro)
                    self._barra_vida(x1, y1, x2, contenido.vida, contenido.vida_maxima)
                elif isinstance(contenido, Torre):
                    # torre
                    sprite = SPRITES_TORRE[self.faccion_def][contenido.tipo]
                    colores = COLOR_SPRITE_TORRE[self.faccion_def]
                    dibujar_pixel(self.canvas, x1 + 4, y1 + 6, sprite, 7, colores)
                    self._barra_vida(x1, y1, x2, contenido.vida, contenido.vida_maxima)

        # dibuja la base central
        bx1 = ORIGEN_X + 4 * TAM    
        by1 = ORIGEN_Y + 4 * TAM    
        colores_base = COLOR_SPRITE_BASE[self.faccion_def]
        dibujar_pixel(self.canvas, bx1 + 7 , by1 + 7, SPRITE_BASE, 7, colores_base)  # +7 para centrarlo

        # barra de vida de la base
        bx2 = ORIGEN_X + 6 * TAM
        self._barra_vida(bx1, by1 - 4, bx2, self.base.vida, self.base.vida_maxima, alto=6)

        # dibuja unidades atacantes
        for u in self.unidades:
            if u.fila is None: # si la unidad no esta colocada se la salta
                continue
            ux = ORIGEN_X + u.columna * TAM  
            uy = ORIGEN_Y + u.fila * TAM     

            # toma el sprite del enemigo segun la faccion del atacante y su tipo
            datos_sprite = SPRITES_ENEMIGO[self.faccion_atk][u.tipo]
            sprite_u = datos_sprite["sprite"]
            alto_sprite = len(sprite_u) * 7        
            ancho_sprite = len(sprite_u[0]) * 7  
            off_x = (TAM - ancho_sprite) // 2  
            off_y = (TAM - alto_sprite) // 2 
            dibujar_pixel(self.canvas, ux + off_x, uy + off_y, sprite_u, 7, datos_sprite["colores"])

            # barra de vida de la unidad
            self._barra_vida(ux,uy, ux + TAM, u.vida, u.vida_maxima)
            # si esta congelada le dibuja un borde celeste alrededor
            if u.congelado:
                self.canvas.create_rectangle(ux + 10, uy + 10, ux + TAM -10, uy + TAM -10, outline= "#88ddff", width= 2)

    def _dibujar_relleno(self, x1, y1, x2, y2, color, texto=""): # pinta el interior de una casilla con un margen
        self.canvas.create_rectangle(x1 + 4, y1 + 4, x2 - 4, y2 - 4, fill=color, outline="")

    def _barra_vida(self, x1, y1, x2, vida, vida_maxima, alto=4): # dibuja una barra de vida
        if vida_maxima <= 0:
            return
        ancho_total = x2 - x1 - 8 # ancho total de la barra
        proporcion = vida / vida_maxima # fraccion de vida que queda (0 a 1)
    
        self.canvas.create_rectangle(x1 + 4, y1 + 2, x1 + 4 + ancho_total, y1 + 2 + alto,fill=C_ROJO, outline="") # fondo rojo vida perdida
        self.canvas.create_rectangle(x1 + 4, y1 + 2, x1 + 4 + ancho_total * proporcion,y1 + 2 + alto, fill=C_VERDE, outline="") # verde encima vida

    # interaccion
    def _celda_desde_pixel(self, x, y): # convierte la posicion de un clic (en pixeles) a una casilla (fila, columna)
        if x < ORIGEN_X or y < ORIGEN_Y: # si el clic cayo antes del tablero no es valido
            return None
        col = (x - ORIGEN_X) // TAM # calcula la columna por division entera
        fila = (y - ORIGEN_Y) // TAM # calcula la fila
        if dentro_del_tablero(fila, col):
            return (fila, col)
        return None # si cayo fuera del tablero devuelve None

    def _es_zona_despliegue(self, fila, col): # devuelve True si la casilla esta en las 2 columnas de algun borde lateral
        return col <= 1 or col >= COLUMNAS -2

    def _click(self, event): # se ejecuta cada vez que el jugador hace clic en el tablero
        celda = self._celda_desde_pixel(event.x, event.y)
        if celda is None: # si el clic fue fuera del tablero no hace nada
            return
        fila, col = celda

        if self.fase == "construccion": # en construccion
            if self.herramienta == "borrar":
                self._borrar(fila, col)
            else:
                self._colocar_construccion(fila, col)
        elif self.fase == "ataque":  # en despliegue
            if self.tipo_unidad_sel == "borrar":
                self._borrar_unidad(fila, col)
            else:
                self._colocar_unidad(fila, col)
        # en combate no se hace clic solo se avanza con los botones de turno

        self._dibujar_tablero() # redibuja para mostrar el cambio
        self._actualizar_marcadores() # actualiza dinero y marcador

    def _avisar(self, mensaje): # muestra un mensaje en la etiqueta de avisos del panel
        if hasattr(self, "lbl_aviso"):
            self.lbl_aviso.config(text=mensaje)

    def _actualizar_marcadores(self): # actualiza los textos de dinero, vida de la base, turno y marcador segun la fase
        marcador = ("DEF " + str(self.vict_def) + "  -  " + str(self.vict_atk) + " ATK" + "   (Ronda " + str(self.ronda) + "/" + str(RONDAS_POR_PARTIDA) + ")")
        if hasattr(self, "lbl_marcador"):
            self.lbl_marcador.config(text=marcador)

        if self.fase == "construccion" and hasattr(self, "lbl_dinero"):
            self.lbl_dinero.config(text="Dinero:" + str(self.jugador_def.dinero)) # dinero del defensor
        elif self.fase == "ataque" and  hasattr(self, "lbl_dinero"):
            self.lbl_dinero.config(text= "Dinero:" + str(self.jugador_atk.dinero)) # dinero del atacante
        elif self.fase == "combate":
            if hasattr(self, "lbl_base"):
                self.lbl_base.config(text= "BASE:" + str(self.base.vida) + "/" + str(self.base.vida_maxima))
            if hasattr(self, "lbl_turno"):
                vivas = len([u for u in self.unidades if u.esta_viva()]) # cuenta unidades vivas
                self.lbl_turno.config(text="Turno " + str(self.turno) + "|   Unidades:" + str(vivas))
            if hasattr(self, "lbl_dinero_def"):
                self.lbl_dinero_def.config(text="Defensor: " + str(self.jugador_def.dinero))
            if hasattr(self, "lbl_dinero_atk"):
                self.lbl_dinero_atk.config(text="Atacante: " + str(self.jugador_atk.dinero))

    def _seleccionar_herramienta(self, herramienta): # marca que herramienta de construccion esta activa y resalta su boton
        self.herramienta = herramienta
        for h, boton in self.botones.items():
            if h == herramienta:
                boton.configure(fg=C_FONDO, bg=C_CYAN) # boton seleccionado 
            else:
                boton.configure(fg=C_CYAN, bg=C_GRIS) # botones normales

    def _colocar_construccion(self, fila, col): # coloca un muro o una torre en la casilla si se puede y si alcanza el dinero
        contenido = self.cuadricula[fila][col]

        if contenido == "base": # no se puede construir sobre la base
            self._avisar("No podes construir sobre la base")
            return
        if contenido is not None: # no se puede construir sobre algo ya colocado
            self._avisar("Esa casilla ya esta ocupada")
            return

        # calcula el costo segun lo que se quiere colocar
        if self.herramienta == "muro":
            costo = COSTO_MURO
        else:
            costo = Torre(self.herramienta).costo

        if not self.jugador_def.puede_pagar(costo): # verifica que alcance el dinero
            self._avisar("No te alcanza el dinero")
            return

        # cobra y coloca el objeto en la cuadricula
        self.jugador_def.gastar(costo)
        if self.herramienta == "muro":
            self.cuadricula[fila][col] = Muro()
        else:
            self.cuadricula[fila][col] = Torre(self.herramienta)
        self._avisar("Colocado!")
        

    def _borrar(self, fila, col): # borra lo que haya en la casilla y le devuelve el dinero al defensor
        contenido = self.cuadricula[fila][col]
        if contenido is None: # si no hay nada no hace nada
            return
        if contenido == "base": # no se puede borrar la base
            self._avisar("No podes borrar la base")
            return

        # devuelve el dinero segun lo que habia
        if isinstance(contenido, Muro):
            self.jugador_def.recibir_dinero(COSTO_MURO)
        elif isinstance(contenido, Torre):
            self.jugador_def.recibir_dinero(contenido.costo)

        self.cuadricula[fila][col] = None # vacia la casilla
        self._avisar("Borrado, dinero devuelto")

    def _terminar_construccion(self): # termina la construccion y pasa a la fase del atacante
        self._ir_a_fase("ataque")

    def _seleccionar_unidad(self, tipo): # marca que tipo de unidad va a colocar el atacante y resalta su boton
        self.tipo_unidad_sel = tipo
        for t, boton in self.botones.items():
            if t == tipo:
                boton.configure(fg=C_FONDO, bg=C_MORADO_CLAR) # boton seleccionado
            else:
                boton.configure(fg=C_MORADO_CLAR, bg=C_GRIS) # botones normales

    def _colocar_unidad(self, fila, col): # coloca una unidad atacante en la casilla si esta en la zona de despliegue
        if not self._es_zona_despliegue(fila, col): # solo en los bordes laterales
            self._avisar("Solo podes desplegar en los bordes laterales")
            return
        if self.cuadricula[fila][col] is not None: # la casilla no debe tener muro, torre, base
            self._avisar("Esa casilla esta ocupada")
            return
        for u in self.unidades: # no puede haber otra unidad en esa casilla
            if u.fila == fila and u.columna == col:
                self._avisar("Ya hay una unidad ahi")
                return

        costo = Unidad(self.tipo_unidad_sel).costo # costo de la unidad elegida
        if not self.jugador_atk.puede_pagar(costo): # verifica que alcance el dinero
            self._avisar("No te alcanza el dinero")
            return

        # cobra y crea la unidad en esa posicion
        self.jugador_atk.gastar(costo)
        unidad = Unidad(self.tipo_unidad_sel, self.tipo_unidad_sel)
        unidad.fila = fila
        unidad.columna = col
        self.unidades.append(unidad)
        self._avisar("Unidad desplegada!")

    def _borrar_unidad(self, fila, col): # quita una unidad de esa casilla y le devuelve el dinero al atacante
        for u in self.unidades:
            if u.fila == fila and u.columna == col:
                self.jugador_atk.recibir_dinero(u.costo) # devuelve lo que costo
                self.unidades.remove(u) # la saca de la lista
                self._avisar("Unidad quitada, dinero devuelto")
                return
        self._avisar("No hay ninguna unidad ahi")

    def _terminar_despliegue(self): # termina el despliegue y pasa al combate si no hay unidades gana el defensor
        if len(self.unidades) == 0:
            messagebox.showinfo("Sin unidades","No desplegaste unidades. La ronda es para el DEFENSOR.")
            self._fin_ronda("defensor")
            return
        self._ir_a_fase("combate")

    # logica del combate
    def _alternar_auto(self): # activa o desactiva el modo automatico
        self.auto_activo = not self.auto_activo
        if self.auto_activo:
            self.btn_auto.config(text="PAUSAR", bg=C_ROJO) # cambia el boton a "PAUSAR"
            self._paso_automatico() # arranca el ciclo automatico
        else:
            self.btn_auto.config(text="AUTO (jugar solo)", bg=C_AMARILLO)  # vuelve a "AUTO"

    def _paso_automatico(self): # da un turno y se vuelve a llamar a si misma cada 600 ms mientras el auto este activo
        if not self.auto_activo or self.fase != "combate":  # si se apago o ya no es combate para
            return
        self._siguiente_turno()
        if self.auto_activo and self.ventana.winfo_exists():
            self.ventana.after(600, self._paso_automatico) # vuelve a llamarse en 600 ms

    def _torres_disparan(self): # cada torre busca unidades en su alcance y las ataca
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                contenido = self.cuadricula[fila][col]
                if not isinstance(contenido, Torre): # solo nos interesan las torres
                    continue
                torre = contenido
                # busca las unidades vivas que esten dentro del alcance de la torre
                en_rango = []
                for u in self.unidades:
                    if u.esta_viva() and u.fila is not None:
                        if distancia_alcance_torre(fila, col, u.fila, u.columna) <= torre.alcance:
                            en_rango.append(u)

                listo = torre.pasar_turno() # pregunta si ya toca usar la habilidad
                if listo and en_rango:
                    # Uua su habilidad especial 
                    texto = torre.activar_habilidad(en_rango)
                    self._log("Torre " + torre.tipo + ": " + str(texto))
                elif en_rango:
                    # disparo normal a la unidad mas cercana
                    objetivo = min(en_rango,
                                   key=lambda u: distancia_alcance_torre(fila, col, u.fila, u.columna))
                    objetivo.recibir_daño(torre.daño)

    def _hay_unidad_en(self, fila, col, ignorar=None): # devuelve True si hay una unidad viva en esa casilla 
        for u in self.unidades:
            if u is ignorar:
                continue
            if u.esta_viva() and u.fila == fila and u.columna == col:
                return True
        return False

    def _casilla_libre_cerca(self, fila, col): # busca una casilla vecina vacia 
        for df, dc in [(-1,0),(1,0),(0,-1),(0,1)]: # revisa arriba, abajo, izquierda y derecha
            nf, nc = fila + df, col + dc
            if not dentro_del_tablero(nf, nc): # debe estar dentro del tablero
                continue
            if self.cuadricula[nf][nc] is not None: # no debe tener muro, torre, base
                continue
            if self._hay_unidad_en(nf, nc): # no debe tener otra unidad
                continue
            return (nf, nc) # encontro una casilla libre
        return None # no hay lugar libre al lado

    def _unidades_avanzan(self): # cada unidad usa su habilidad si toca y luego avanza hacia la base atacando lo que encuentre
        copias_nuevas = [] # se guardan las copias creadas por los replicantes

        for u in self.unidades:
            if not u.esta_viva() or u.fila is None: # salta unidades muertas o sin posicion
                continue

            # pregunta si le toca usar su habilidad este turno
            listo = u.pasar_turno()
            if listo:
                torres_cerca = self._torres_adyacentes(u.fila, u.columna)
                resultado = u.activar_habilidad(torres_cerca)
                if isinstance(resultado, Unidad): # si devolvio una Unidad es una copia del replicante
                    libre = self._casilla_libre_cerca(u.fila, u.columna) # busca lugar al lado
                    if libre is not None:
                        resultado.fila, resultado.columna = libre
                        copias_nuevas.append(resultado) # guarda la copia para agregarla luego
                        self._log("Unidad replicante se duplico")
                else:
                    self._log("Unidad " + u.tipo + ": " + str(resultado))

            # si esta congelada pierde el movimiento de ESTE turno y luego se descongela
            if u.congelado:
                u.congelado = False
                continue

            # la unidad intenta moverse 'velocidad' casillas hacia la base
            for _ in range(u.velocidad):
                sf, sc = siguiente_paso(u.fila, u.columna, self.cuadricula) # calcula el siguiente paso
                if (sf, sc) == (u.fila, u.columna):
                    break # no hay a donde avanzar
                destino = self.cuadricula[sf][sc] # que hay en la casilla de destino

                if destino == "base": # llego a la base, la ataca y el atacante gana dinero
                    self.base.recibir_daño(u.daño)
                    self.daño_base_ronda += u.daño
                    self.jugador_atk.recibir_dinero(RECOMPENSA_ATK_POR_GOLPE_BASE)
                    break

                elif isinstance(destino, Torre): # hay una torre en el camino, la ataca
                    destino.recibir_daño(u.daño)
                    self.jugador_atk.recibir_dinero(RECOMPENSA_ATK_POR_GOLPE_TORRE)
                    break

                elif isinstance(destino, Muro): # hay un muro, si tiene bypass activo lo atraviesa sino lo ataca
                    if u.ignora_muro:
                        u.ignora_muro = False # gasta el bypass
                        u.fila, u.columna = sf, sc # atraviesa el muro
                    else:
                        destino.recibir_daño(u.daño) # ataca el muro y no avanza
                        break

                else: # avanza solo si no hay otra unidad ahi
                    if self._hay_unidad_en(sf, sc, ignorar=u):
                        break
                    u.fila, u.columna = sf, sc

        # agrega al tablero las copias creadas por los replicantes
        self.unidades.extend(copias_nuevas)

    def _torres_adyacentes(self, fila, col): # devuelve la lista de torres que estan a distancia 1 de la casilla dada
        torres = []
        for f in range(FILAS):
            for c in range(COLUMNAS):
                if isinstance(self.cuadricula[f][c], Torre):
                    if distancia_alcance_torre(fila, col, f, c) <= 1:
                        torres.append(self.cuadricula[f][c])
        return torres

    def _limpiar_muertos(self): # quita las unidades, torres y muros destruidos y reparte el dinero ganado
        vivas = []
        for u in self.unidades:
            if u.esta_viva():
                vivas.append(u) # las vivas se mantienen
            else:
                self.jugador_def.recibir_dinero(RECOMPENSA_DEF_POR_UNIDAD[u.tipo]) # el defensor gana dinero.
        self.unidades = vivas

        # quita torres y muros destruidos, si era torre el atacante gana dinero
        for f in range(FILAS):
            for c in range(COLUMNAS):
                celda = self.cuadricula[f][c]
                if isinstance(celda, Torre) and not celda.esta_viva():
                    self.jugador_atk.recibir_dinero(RECOMPENSA_ATK_POR_TORRE[celda.tipo])
                    self.cuadricula[f][c] = None
                elif isinstance(celda, Muro) and not celda.esta_vivo():
                    self.cuadricula[f][c] = None

    def _siguiente_turno(self): # ejecuta un turno completo de combate en orden
        if self.fase != "combate":
            return
        self.turno += 1
        self._torres_disparan() # 1. disparan las torres
        self._unidades_avanzan() # 2. avanzan las unidades
        self._limpiar_muertos() # 3. se limpian los muertos y se reparte dinero
        self._dibujar_tablero() # 4. se redibuja todo
        self._actualizar_marcadores() # 5. se actualizan los marcadores
        self._verificar_fin_combate() # 6. se revisa si la ronda termino

    def _log(self, texto): # muestra el ultimo evento del combate en la etiqueta de registro
        if hasattr(self, "lbl_log"):
            self.lbl_log.config(text=texto)

    def _verificar_fin_combate(self): # revisa si la ronda termino y decide el ganador
        if not self.base.esta_viva(): # la base cayo gana el atacante
            self.auto_activo = False
            self._fin_ronda("atacante")
        elif len([u for u in self.unidades if u.esta_viva()]) == 0: # no quedan enemigos gana el defensor
            self.auto_activo = False
            self._fin_ronda("defensor")
        elif self.turno >= MAX_TURNOS_COMBATE: # se llego al limite de turnos gana el defensor
            self.auto_activo = False
            self._fin_ronda("defensor")

    # rondas y victorias
    def _fin_ronda(self, ganador_rol): # cierra la ronda, suma la victoria al ganador y decide si la partida termino
            if ganador_rol == "defensor":
                self.vict_def += 1
                nombre = self.nombre_def
            else:
                self.vict_atk += 1
                nombre = self.nombre_atk

            self._actualizar_marcadores() # muestra un mensaje con el resultado de la ronda
            messagebox.showinfo("Fin de la ronda " + str(self.ronda),"Gano la ronda el " + ganador_rol.upper() + " (" + nombre + ")\n\n" + "Marcador:  DEFENSOR " + str(self.vict_def) + "  -  " + str(self.vict_atk) + " ATACANTE")

            # si ya se jugaron las 3 rondas termina la partida sino sigue con la proxima
            if self.ronda >= RONDAS_POR_PARTIDA:
                if self.vict_def > self.vict_atk:
                    self._fin_partida("defensor", self.nombre_def)
                else:
                    self._fin_partida("atacante", self.nombre_atk)
            else:
                self._nueva_ronda() # todavia faltan rondas

    def _nueva_ronda(self): # prepara la siguiente ronda limpia el tablero y reparte el dinero nuevo
        bono_atacante = self.daño_base_ronda // 5 # bono del atacante segun el dano que hizo a la base

        self.ronda += 1
        self._limpiar_tablero_para_nueva_ronda() # vacia el tablero y restaura la base

        # ingreso de dinero al inicio de la ronda para ambos jugadores
        self.jugador_def.recibir_dinero(INGRESO_POR_RONDA)
        self.jugador_atk.recibir_dinero(INGRESO_POR_RONDA + bono_atacante)

        self._ir_a_fase("construccion") # vuelve a la fase de construccion del defensor

    def _fin_partida(self, rol_ganador, nombre_ganador):
        # termina la partida guarda la victoria en el ranking y vuelve al menu
        # actualiza el ranking global, cada usuario guarda [victorias_def, victorias_atk]
        if nombre_ganador in self.app.puntajes_globales:
            if rol_ganador == "defensor":
                self.app.puntajes_globales[nombre_ganador][0] += 1 # +1 victoria como defensor
            else:
                self.app.puntajes_globales[nombre_ganador][1] += 1 # +1 victoria como atacante
        self.app.guardar() # escribe los cambios en usuarios.json

        # muestra el mensaje final de la partida
        messagebox.showinfo("FIN DE LA PARTIDA","GANADOR: " + nombre_ganador + "  (" + rol_ganador.upper() + ")\n\n"+ "Marcador final:  DEFENSOR " + str(self.vict_def) + "  -  " + str(self.vict_atk) + " ATACANTE\n\n" + "La victoria se guardo en el ranking.")

        self.ventana.destroy() # cierra la ventana de la partida
        self.app.cargar_pantalla_inicio() # vuelve al menu principal



# aplicacion
class AplicacionJuego:
    def __init__(self, ventana_principal): # configura la ventana principal y carga los datos guardados.
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Tower Defense")
        self.ventana_principal.geometry("1500x900")
        self.ventana_principal.configure(bg=C_FONDO)
        self.ventana_principal.resizable(False, False)

        self.usuarios_registrados, self.puntajes_globales = cargar_datos() # carga los usuarios y puntajes guardados en el archivo

        # quien entro como defensor y quien como atacante
        self.jugador_defensor = ""
        self.jugador_atacante = ""

        # facciones elegidas por cada uno
        self.faccion_def_sel = None
        self.faccion_atk_sel = None

        # lienzo donde se dibuja todo
        self.canvas = tk.Canvas(self.ventana_principal, width=1500, height=900,bg=C_FONDO, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.widgets_flotantes = [] # lista de cosas que se crean encima del lienzo

        self.cargar_pantalla_inicio() # muestra la primera pantalla

    # utilidades de la interfaz
    def _limpiar(self): # borra los dibujos del lienzo y destruye los widgets flotantes
        self.canvas.delete("all")
        for w in self.widgets_flotantes:
            w.destroy()
        self.widgets_flotantes = []

    def _boton(self, x, y, texto, color, comando, ancho=20, tam=16): # crea un boton centrado en (x, y) y lo guarda en la lista de widgets flotantes
        b = tk.Button(self.ventana_principal, text=texto, font=("Courier", tam, "bold"),fg=C_FONDO, bg=color, activebackground=color, activeforeground=C_FONDO,width=ancho, height=1, relief="flat", bd=0, command=comando)
        b.place(x=x, y=y, anchor="center")
        self.widgets_flotantes.append(b)
        return b

    def _entry(self, x, y, oculto=False): # crea un campo de texto centrado en (x, y), si 'oculto' es True muestra asteriscos
        e = tk.Entry(self.ventana_principal, font=("Courier", 16),width=24, fg=C_CYAN, bg=C_GRIS,insertbackground=C_CYAN, relief="flat",highlightthickness=2, highlightbackground=C_CYAN_OSC,highlightcolor=C_CYAN, justify="center",show="*" if oculto else "")
        e.place(x=x, y=y, anchor="center")
        self.widgets_flotantes.append(e)
        return e

    def _panel(self, x1, y1, x2, y2, titulo, color_barra=C_CYAN): # dibuja un panel con un borde y una barra de titulo arriba
        self.canvas.create_rectangle(x1, y1, x2, y2,fill=C_PANEL,outline=color_barra, width=2)
        self.canvas.create_rectangle(x1, y1, x2, y1+50,fill=color_barra, outline="")
        cx = (x1 + x2) // 2
        self.canvas.create_text(cx, y1+25, text=titulo,font=("Courier", 20, "bold"), fill=C_FONDO)

    # pantalla de inicio
    def cargar_pantalla_inicio(self): # dibuja el menu principal con el titulo y los botones
        self._limpiar()
        dibujar_escena_completa(self.canvas)

        self.canvas.create_text(750, 130, text="DEFENSA Y ASALTO",font=("Courier", 60, "bold"), fill=C_CYAN)
        self.canvas.create_line(300, 185, 1200, 185, fill=C_AZUL_CLARO, width=2)
        self.canvas.create_line(460, 192, 1040, 192, fill=C_CYAN_OSC, width=1)
        self.canvas.create_text(750, 225, text="CODE vs CHAOS",font=("Courier", 16), fill=C_AZUL_CLARO)

        self._boton(750, 410, "▶  INICIAR JUEGO",C_CYAN,   self.ir_a_registro)
        self._boton(750, 470, "PUNTAJES",C_MORADO_CLAR, self.ir_a_puntajes)
        self._boton(750, 530, "✖  SALIR",C_ROJO,   self.ventana_principal.quit)

    # pantalla regustro
    def ir_a_registro(self):
       
        self._limpiar()
        dibujar_fondo_simple(self.canvas)

        self._panel(450, 150, 1050, 760, "REGISTRO  /  LOGIN")   # Panel central.

        
        self.canvas.create_text(750, 255, text="NOMBRE DE USUARIO",font=("Courier", 13, "bold"), fill=C_CYAN)
        self.entrada_usuario = self._entry(750, 295)

        
        self.canvas.create_text(750, 350, text="CONTRASEÑA",font=("Courier", 13, "bold"), fill=C_CYAN)
        self.entrada_usuario_contraseña = self._entry(750, 390, oculto=True)

    
        self._boton(750, 450, "REGISTRAR USUARIO",   C_VERDE,self.ejecutar_registro,   ancho=24, tam=13)
        self._boton(750, 500, "ENTRAR COMO DEFENSOR", C_CYAN,self.autentificar_defensor, ancho=24, tam=13)
        self._boton(750, 550, "ENTRAR COMO ATACANTE", C_MORADO_CLAR,self.autentificar_atacante, ancho=24, tam=13)

      
        self.id_estado = self.canvas.create_text(750, 615, text="DEFENSOR: ---     |     ATACANTE: ---",font=("Courier", 14, "italic"), fill=C_AZUL_CLARO)

        self._boton(750, 645, "ELEGIR FACCIONES >>", C_AMARILLO, self.ir_a_facciones, ancho=24, tam=13)  # Avanza a facciones.
        self._boton(750, 700, "◀  VOLVER AL INICIO", C_ROJO, self.cargar_pantalla_inicio, ancho=24, tam=13)  # Vuelve al menu.
        self.ventana_principal.update_idletasks()   # Fuerza a que los campos de texto aparezcan de una.

    def _texto_estado(self):
     
        d = self.jugador_defensor if self.jugador_defensor else "---"
        a = self.jugador_atacante if self.jugador_atacante else "---"
        return "DEFENSOR: " + d + "     |     ATACANTE: " + a

    def ejecutar_registro(self): # registra un usuario nuevo con su contrasena, validando que no este vacio ni repetido.
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_usuario_contraseña.get()

        if usuario == "":
            messagebox.showwarning("Error", "El Usuario no puede estar vacio")
        elif contraseña == "":
            messagebox.showwarning("Error", "La contraseña no puede estar vacia")
        elif usuario in self.usuarios_registrados:
            messagebox.showwarning("Error", "Este usuario ya existe")
        else:
            self.usuarios_registrados[usuario] = contraseña # guarda el usuario
            self.puntajes_globales[usuario] = [0, 0] # le crea su registro de puntajes
            self.guardar()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.entrada_usuario.delete(0, tk.END) # limpia los campos
            self.entrada_usuario_contraseña.delete(0, tk.END)

    def guardar(self): # guarda el estado actual de usuarios y puntajes en el archivo
        guardar_datos(self.usuarios_registrados, self.puntajes_globales)

    def autentificar_defensor(self): # verifica usuario y contrasena y si son correctos lo deja entrar como defensor
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_usuario_contraseña.get()
        if usuario in self.usuarios_registrados and self.usuarios_registrados[usuario] == contraseña:
            self.jugador_defensor = usuario
            self.canvas.itemconfig(self.id_estado, text=self._texto_estado())
            messagebox.showinfo("Exito", "Sesion iniciada como Defensor")
            self.entrada_usuario.delete(0, tk.END)
            self.entrada_usuario_contraseña.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def autentificar_atacante(self): # verifica usuario y contrasena y si son correctos lo deja entrar como atacante
        usuario = self.entrada_usuario.get()
        contraseña = self.entrada_usuario_contraseña.get()
        if usuario in self.usuarios_registrados and self.usuarios_registrados[usuario] == contraseña:
            if usuario == self.jugador_defensor:    # No puede ser defensor y atacante a la vez.
                messagebox.showwarning("Cuidado", "No podes ser Defensor y Atacante a la vez")
            else:
                self.jugador_atacante = usuario
                self.canvas.itemconfig(self.id_estado, text=self._texto_estado())
                messagebox.showinfo("Exito", "Sesion iniciada como Atacante")
                self.entrada_usuario.delete(0, tk.END)
                self.entrada_usuario_contraseña.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # seleccion de facciones
    def ir_a_facciones(self): # dibuja la pantalla donde cada jugador elige su faccion
        if not self.jugador_defensor or not self.jugador_atacante: # deben haber entrado ambos
            messagebox.showwarning("Faltan jugadores", "Deben iniciar sesion el Defensor y el Atacante")
            return
        self._limpiar()
        dibujar_fondo_simple(self.canvas)
        self._panel(250, 120, 1250, 800, "ELIGE TU FACCIÓN", color_barra = C_AMARILLO)

        # columnas con el nombre de cada jugador
        self.canvas.create_text(500, 210, text = "DEFENSOR:" + self.jugador_defensor, font=("Courier", 16, "bold"), fill=C_CYAN)
        self.canvas.create_text(1000, 210, text = "ATACANTE:" + self.jugador_atacante, font=("Courier", 16, "bold"), fill=C_MORADO_CLAR)

        # diccionarios para guardar los botones de faccion de cada jugador
        self.btn_fac_def = {}
        self.btn_fac_atk = {}

        # crea un boton de faccion por cada jugador, y la descripcion en el centro
        y = 290
        for nombre_fac in FACCIONES:
            bd = self._boton(500, y, nombre_fac, C_GRIS, lambda f=nombre_fac: self.elegir_faccion("def",f), ancho = 18, tam= 13)
            self.btn_fac_def[nombre_fac] = bd
            ba = self._boton(1000, y, nombre_fac, C_GRIS, lambda f=nombre_fac: self.elegir_faccion("atk",f), ancho = 18, tam= 13)
            self.btn_fac_atk[nombre_fac] = ba
            self.canvas.create_text(750, y, text=FACCIONES[nombre_fac]["descripcion"], font=("Courier", 9, "italic"), fill=C_TEXTO)
            y += 70

        # texto de estado de la seleccion de cada jugador
        self.id_estado_fac = self.canvas.create_text(750, 600, text="",font=("Courier", 13, "italic"),fill=C_AZUL_CLARO)

        self._boton(750, 680, "COMENZAR PARTIDA", C_VERDE, self.comenzar_partida, ancho= 24, tam= 15)
        self._boton(750, 745, "VOLVER", C_ROJO, self.ir_a_registro, ancho= 24, tam= 13)

        self.actualizar_estado_facciones()

    def elegir_faccion(self, rol, faccion): # guarda la faccion elegida por un jugador evitando que ambos elijan la misma
        if rol == "def":
            if faccion == self.faccion_atk_sel:
                messagebox.showwarning("Repetida", "El atacante ya eligio esa faccion")
                return
            self.faccion_def_sel = faccion
        else:
            if faccion == self.faccion_def_sel:
                messagebox.showwarning("Repetida", "El defensor ya eligio esa faccion")
                return
            self.faccion_atk_sel = faccion
        self.actualizar_estado_facciones()

    def actualizar_estado_facciones(self): # resalta los botones de las facciones elegidas y actualiza el texto de estado
        for fac, b in self.btn_fac_def.items():
            b.configure(bg= C_CYAN if fac == self.faccion_def_sel else C_GRIS)
        for fac, b in self.btn_fac_atk.items():
            b.configure(bg= C_MORADO_CLAR if fac == self.faccion_atk_sel else C_GRIS)
        d = self.faccion_def_sel if self.faccion_def_sel else "___"
        a = self.faccion_atk_sel if self.faccion_atk_sel else "___"
        self.canvas.itemconfig(self.id_estado_fac, text = "Defensor:" + d + "    |      Atacante: " + a)

    def comenzar_partida(self): # valida que ambos hayan elegido faccion y abre la ventana de la partida
        if not self.faccion_def_sel or not self.faccion_atk_sel:
            messagebox.showwarning("Faltan facciones","Ambos jugadores deben elegir facción.")
            return

        # abre la ventana de la partida con los datos de ambos jugadores
        VentanaPartida(self, self.jugador_defensor, self.jugador_atacante, self.faccion_def_sel, self.faccion_atk_sel)


    # puntajes
    def ir_a_puntajes(self):
        # dibuja el ranking global
        self._limpiar()
        dibujar_fondo_simple(self.canvas)
        self._panel(300, 120, 1200, 800, "RANKING GLOBAL", color_barra=C_MORADO_CLAR)

        # arma una lista a partir de los puntajes
        datos = []
        for usuario, v in self.puntajes_globales.items():
            if isinstance(v, list) and len(v) >= 2:
                datos.append((usuario, v[0], v[1]))
            else:
                datos.append((usuario, 0, 0)) # =si el dato es invalido lo toma como 0

        rank_def = sorted(datos, key=lambda t: t[1], reverse=True) # ordena por victorias de defensor
        rank_atk = sorted(datos, key=lambda t: t[2], reverse=True) # ordena por victorias de atacante

        ESPACIADO = 32      
        LIMITE_Y = 715     

        # ranking de DEFENSORES
        self.canvas.create_text(520, 215, text="DEFENSORES",font=("Courier", 16, "bold"), fill=C_CYAN)
        self.canvas.create_line(370, 240, 670, 240, fill=C_CYAN_OSC, width=1)
        y = 280
        if not rank_def:
            self.canvas.create_text(520, y, text="Sin jugadores aún", font=("Courier", 12), fill=C_TEXTO)
        for i, (usuario, vd, va) in enumerate(rank_def, start=1):
            if y > LIMITE_Y:      # Si ya no cabe, para.
                break
            self.canvas.create_text(400, y, text=str(i) + ".", font=("Courier", 12), fill=C_AMARILLO, anchor="w")
            self.canvas.create_text(440, y, text=usuario, font=("Courier", 12), fill="#ffffff", anchor="w")
            self.canvas.create_text(650, y, text=str(vd), font=("Courier", 12, "bold"), fill=C_CYAN, anchor="e")
            y += ESPACIADO

        # ranking de ATACANTES
        self.canvas.create_text(980, 215, text="ATACANTES",font=("Courier", 16, "bold"), fill=C_MORADO_CLAR)
        self.canvas.create_line(830, 240, 1130, 240, fill=C_CYAN_OSC, width=1)
        y = 280
        if not rank_atk:
            self.canvas.create_text(980, y, text="Sin jugadores aún", font=("Courier", 12), fill=C_TEXTO)
        for i, (usuario, vd, va) in enumerate(rank_atk, start=1):
            if y > LIMITE_Y:
                break
            self.canvas.create_text(860, y, text=str(i) + ".", font=("Courier", 12), fill=C_AMARILLO, anchor="w")
            self.canvas.create_text(900, y, text=usuario, font=("Courier", 12), fill="#ffffff", anchor="w")
            self.canvas.create_text(1110, y, text=str(va), font=("Courier", 12, "bold"), fill=C_MORADO_CLAR, anchor="e")
            y += ESPACIADO

        self._boton(750, 755, "<  VOLVER AL INICIO", C_CYAN, self.cargar_pantalla_inicio, ancho=24, tam=13)


if __name__ == "__main__":
    raiz = tk.Tk()                      
    app = AplicacionJuego(raiz)         
    reproducir_musica("musica.mp3")    
    raiz.mainloop()                  