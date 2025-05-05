import math
import pygame
import sys
import json
import os
import random
from PIL import Image

pygame.init()
# Configuración
ANCHO, ALTO = 800, 600
FILAS, COLUMNAS = 6, 12
TAM_CASILLA = 60
MARGEN = 30
COLOR_FONDO = (25, 25, 25)
VELOCIDAD_SCROLL = 1.5

# Paleta de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
MORADO = (102, 0, 204)
AZUL = (0, 200, 200)
COLOR_NIEVE = (255, 255, 255)  # Color blanco para la nieve
COLOR_BG = (255, 239, 204)  # Un fondo más suave y pastel (tono claro de beige)
COLOR_LINEA = (80, 80, 80)  # Gris oscuro para las líneas, pero no completamente negro
COLOR_FIGURA = (178, 128, 255)  # Un morado pastel claro para las figuras
COLOR_OBJETIVO = (144, 238, 144)  # Verde pastel para los objetivos
COLOR_BLOQUEO = (211, 211, 211)  # Gris suave para los bloqueos
COLOR_ESPEJO = (173, 216, 230)  # Azul claro pastel para los espejos
COLOR_TEXTO = (60, 60, 60)  # Gris suave para el texto (en vez de negro total)
COLOR_PANEL = (240, 240, 240)  # Gris claro para el panel (casi blanco)
COLOR_BOTON = (178, 128, 255)  # El mismo morado pastel para los botones
COLOR_BOTON_HOVER = (216, 169, 255)  # Morado pastel un poco más claro para el hover
COLOR_NIVEL_BLOQUEADO = (192, 192, 192)  # Gris pastel para niveles bloqueados
COLOR_NIVEL_DESBLOQUEADO = (144, 238, 144)  # Verde pastel claro para niveles desbloqueados
COLOR_NIVEL_SELECCIONADO = (216, 191, 255)  # Lila pastel para el nivel seleccionado

# ======================================================================
# SISTEMA DE FUENTES
# ======================================================================

try:
    # Intenta cargar fuentes personalizadas
    fuente_pixel = {
        'pequena': pygame.font.Font("Fuentes/PixelOperator.ttf", 28),
        'mediana': pygame.font.Font("Fuentes/PixelOperator.ttf", 40),
        'grande': pygame.font.Font("Fuentes/PixelOperator.ttf", 56),
        'titulo': pygame.font.Font("Fuentes/PixelOperator.ttf", 64)
    }
    if os.path.exists("PixelOperator-Bold.ttf"):
        fuente_pixel['titulo_bold'] = pygame.font.Font("PixelOperator-Bold.ttf", 64)
except:
    # Fallback a fuentes del sistema si no hay fuentes personalizadas
    fuente_pixel = {
        'pequena': pygame.font.SysFont("Arial", 24),
        'mediana': pygame.font.SysFont("Arial", 40),
        'grande': pygame.font.SysFont("Arial", 56),
        'titulo': pygame.font.SysFont("Arial", 64)
    }

# Fuentes adicionales
fuente = pygame.font.SysFont("Arial", 24)
titulo_fuente = pygame.font.SysFont("Arial", 64, bold=True)
boton_fuente = pygame.font.SysFont("Arial", 36, bold=True)

# ======================================================================
# FUNCIONES DE UTILIDAD
# ======================================================================

def cargar_imagen(ruta, escala=None):
    """Carga una imagen y opcionalmente la escala"""
    try:
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, escala) if escala else img
    except:
        # Crea una imagen de relleno si no se encuentra el archivo
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        color = (255, 0, 0) if "pinguino" in ruta.lower() else (0, 200, 200)
        pygame.draw.rect(surf, color, (0, 0, 100, 100), border_radius=10)
        return surf
import pygame
import random

def mostrar_creditos():
    reloj = pygame.time.Clock()
    scroll_y = ALTO
    particulas = []
    ejecutando = True
    creditos_terminados = False

    donacion = pygame.image.load("Img/Qr.jpg")
    donacion = pygame.transform.scale(donacion, (300, 300))

    try:
        fuente_normal = pygame.font.Font("Fuentes/visitor1.ttf", 48)
        fuente_bold = pygame.font.Font("Fuentes/visitor2.ttf", 48)
        fuente_pequena = pygame.font.Font("Fuentes/visitor1.ttf", 28)
        print("✔ Fuentes cargadas correctamente")
    except Exception as e:
        print(f"✖ Error: {e}")
        print("⚠ Usando Arial como respaldo")
        fuente_normal = pygame.font.SysFont("Arial", 48)
        fuente_bold = pygame.font.SysFont("Arial", 48, bold=True)
        fuente_pequena = pygame.font.SysFont("Arial", 28)

    fuente_grande = fuente_bold
    fuente_mediana = fuente_normal

    pygame.mixer.music.load("Sonidos/creditos.wav")

    creditos = [
        {"texto": "DESARROLLADO POR", "tipo": "grande"},
        {"texto": "EQUIPO REFLEJO PERDIDO", "tipo": "mediana"},
        {"texto": "PROGRAMACION:", "tipo": "mediana"},
        {"texto": "Anghelo Johan Montalvo Molina", "tipo": "pequena"},
        {"texto": "DESARROLLADOR WEB", "tipo": "mediana"},
        {"texto": "Gustavo Choré Parra", "tipo": "pequena"},
        {"texto": "DISEÑO DE JUEGO:", "tipo": "mediana"},
        {"texto": "Anghelo Johan Montalvo Molina", "tipo": "pequena"},
        {"texto": "Gustavo Choré Parra", "tipo": "pequena"},
        {"texto": "ARTE Y DISEÑO:", "tipo": "mediana"},
        {"texto": "Anghelo Johan Montalvo Molina", "tipo": "pequena"},
        {"texto": "Gustavo Choré Parra", "tipo": "pequena"},
        {"texto": "MUSICA Y SONIDO:", "tipo": "mediana"},
        {"texto": "Leonardo Zarcillo Lino", "tipo": "pequena"},
        {"texto": "Anghelo Johan Montalvo Molina", "tipo": "pequena"},
        {"texto": "Documentacion y Creditos", "tipo": "mediana"},
        {"texto": "Roque Alexander Justiniano Santivañez", "tipo": "pequena"},
        {"texto": "¡GRACIAS POR JUGAR!", "tipo": "grande"},
    ]

    def crear_particula():
        return {
            "x": random.randint(0, ANCHO),
            "y": random.randint(0, ALTO),
            "vel_x": random.uniform(-0.5, 0.5),
            "vel_y": random.uniform(-1, -2),
            "tam": random.randint(2, 4),
            "color": (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        }

    def dibujar_texto(texto, y_pos, tipo_fuente):
        if tipo_fuente == "grande":
            fuente = fuente_grande
            color = (178, 128, 255)
        elif tipo_fuente == "mediana":
            fuente = fuente_mediana
            color = (144, 238, 144)
        else:
            fuente = fuente_pequena
            color = (200, 200, 200)

        texto_surf = fuente.render(texto, True, color)
        texto_rect = texto_surf.get_rect(center=(ANCHO // 2, y_pos))
        ventana.blit(texto_surf, texto_rect)

    pygame.mixer.music.play(-1)
    for _ in range(100):
        particulas.append(crear_particula())

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                ejecutando = False
        ventana.fill(COLOR_FONDO)

        for p in particulas[:]:
            p["x"] += p["vel_x"]
            p["y"] += p["vel_y"]
            if p["y"] < 0 or p["x"] < 0 or p["x"] > ANCHO:
                particulas.remove(p)
                particulas.append(crear_particula())
            pygame.draw.circle(ventana, p["color"], (int(p["x"]), int(p["y"])), p["tam"])

        if not creditos_terminados:
            y_pos = scroll_y
            for credito in creditos:
                dibujar_texto(credito["texto"], y_pos, credito["tipo"])
                y_pos += 60
            scroll_y -= VELOCIDAD_SCROLL
            if y_pos < 0:
                creditos_terminados = True
        else:
            texto_qr = fuente_mediana.render("Escanea para donar y ", True, (255, 255, 255))
            texto_qr2 = fuente_mediana.render("apoyar el desarrollo", True, (255, 255, 255))
            texto_rect = texto_qr.get_rect(center=(ANCHO // 2, 40))
            texto_rect2 = texto_qr2.get_rect(center=(ANCHO // 2, 90))
            ventana.blit(texto_qr, texto_rect)
            ventana.blit(texto_qr2, texto_rect2)
            img_rect = donacion.get_rect(center=(ANCHO // 2, ALTO // 2))
            ventana.blit(donacion, img_rect)
            salir = fuente_pequena.render("Presiona ESC para salir", True, (255, 255, 255))
            ventana.blit(salir, (ANCHO // 2 - salir.get_width() // 2, ALTO - 50))

        pygame.display.flip()
        reloj.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()
def ejecutar_trailer():
    """Muestra la secuencia de trailer introductorio"""
    global ventana, ANCHO, ALTO
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Sonidos/cinematica.wav")
    pygame.mixer.music.play(-1)
    # Carga de assets del trailer
    pingu_img = cargar_imagen("Img/penguin1.png", (80, 80))
    fondo_1 = cargar_imagen("Img/fondo_trailer.jpg", (ANCHO, ALTO))
    fondo_2 = cargar_imagen("Img/fondo_trailer2.png", (ANCHO, ALTO))
    fondo_3 = cargar_imagen("Img/fondo_trailer3.png", (ANCHO, ALTO))

    class TextoPixel:
        """Clase para manejar texto con estilo pixel"""
        def __init__(self, texto, tipo_fuente, color, pos_x, pos_y, efecto=None, duracion=4.0, con_sombra=True):
            self.texto = texto
            self.fuente = fuente_pixel.get(tipo_fuente, fuente_pixel['mediana'])
            self.color = list(color)
            self.x, self.y = pos_x, pos_y
            self.efecto = efecto
            self.duracion = duracion
            self.tiempo = 0
            self.con_sombra = con_sombra
            
            if tipo_fuente == 'titulo':
                self.superficie = pygame.transform.scale_by(self.fuente.render(texto, True, color[:3]), 2)
            else:
                self.superficie = self.fuente.render(texto, True, color[:3])
        
        def actualizar(self, dt):
            """Actualiza efectos de animación"""
            self.tiempo += dt
            if not self.efecto:
                return
                
            progreso = min(self.tiempo / self.duracion, 2.0)
            
            if self.efecto == "fade":
                self.color[3] = int(progreso * 255)
                self.superficie = self.fuente.render(self.texto, True, self.color[:3])
            elif self.efecto == "wave":
                self.y += math.sin(progreso * 10) * 3
        
        def dibujar(self, superficie):
            """Dibuja el texto en la superficie especificada"""
            if self.con_sombra and self.efecto != "fade":
                sombra = self.fuente.render(self.texto, True, BLANCO)
                superficie.blit(sombra, (self.x - sombra.get_width()//2 + 2, self.y + 2))
            
            superficie.blit(
                self.superficie, 
                (self.x - self.superficie.get_width()//2, self.y)
            )

    class DemoControles:
        """Demo interactiva de controles"""
        def __init__(self):
            self.pingu_pos = [ANCHO//2, ALTO//2]
            self.rotacion = 0
            self.reflejado = False
            self.teclas = {
                pygame.K_LEFT: False, 
                pygame.K_RIGHT: False, 
                pygame.K_UP: False, 
                pygame.K_DOWN: False
            }
            self.mensaje = ""
            self.tiempo_mensaje = 0
        
        def actualizar(self, dt):
            """Actualiza la posición del pingüino"""
            velocidad = 180 * dt
            if self.teclas[pygame.K_LEFT]: self.pingu_pos[0] -= velocidad
            if self.teclas[pygame.K_RIGHT]: self.pingu_pos[0] += velocidad
            if self.teclas[pygame.K_UP]: self.pingu_pos[1] -= velocidad
            if self.teclas[pygame.K_DOWN]: self.pingu_pos[1] += velocidad
            
            # Limita el movimiento dentro de la pantalla
            self.pingu_pos[0] = max(30, min(ANCHO - 30, self.pingu_pos[0]))
            self.pingu_pos[1] = max(30, min(ALTO - 30, self.pingu_pos[1]))
            
            if self.tiempo_mensaje > 0:
                self.tiempo_mensaje -= dt
        
        def manejar_evento(self, evento):
            """Procesa eventos de teclado"""
            if evento.type == pygame.KEYDOWN:
                if evento.key in self.teclas:
                    self.teclas[evento.key] = True
                elif evento.key == pygame.K_r:
                    self.reflejado = not self.reflejado
                    self.mensaje = "Reflejado!" if self.reflejado else "Normal"
                    self.tiempo_mensaje = 1.5
                elif evento.key == pygame.K_e:
                    self.rotacion = (self.rotacion + 90) % 360
                    self.mensaje = f"Rotación: {self.rotacion}°"
                    self.tiempo_mensaje = 1.5
            elif evento.type == pygame.KEYUP:
                if evento.key in self.teclas:
                    self.teclas[evento.key] = False
        
        def dibujar(self, superficie):
            """Dibuja la demo"""
            superficie.blit(fondo_3, (0, 0))
            pygame.draw.line(superficie, AZUL, (ANCHO//2, 0), (ANCHO//2, ALTO), 3)
            
            # Dibuja el pingüino y su reflejo
            pingu = pygame.transform.rotate(pingu_img, self.rotacion)
            if self.reflejado:
                pingu = pygame.transform.flip(pingu, True, False)
            
            superficie.blit(pingu, (self.pingu_pos[0] - pingu.get_width()//2, self.pingu_pos[1] - pingu.get_height()//2))
            
            reflejo = pygame.transform.flip(pingu, True, False)
            superficie.blit(reflejo, (ANCHO - self.pingu_pos[0] - reflejo.get_width()//2, self.pingu_pos[1] - reflejo.get_height()//2))
            
            # Dibuja controles
            controles = ["CONTROLES:", "ESPACIO : Verificar", "Flechas : Mover", "R : Reflejar", "E : Rotar"]
            for i, texto in enumerate(controles):
                txt = TextoPixel(texto, 'pequena', NEGRO, 120, 40 + i*40, con_sombra=False)
                txt.dibujar(superficie)
            
            # Dibuja mensajes
            if self.mensaje and self.tiempo_mensaje > 0:
                txt = TextoPixel(self.mensaje, 'mediana', NEGRO, ANCHO//2, ALTO - 50, con_sombra=False)
                txt.dibujar(superficie)

    # Escenas del trailer
    escenas = [
        {  # Escena 0: Introducción
            "fondo": fondo_1,
            "duracion": 4.0,
            "elementos": [
                {"tipo": "texto", "texto": "En un mundo de hielo...", 
                 "fuente": "mediana", "color": NEGRO + (255,), 
                 "efecto": "fade", "x": ANCHO//2, "y": 150},
                 
                {"tipo": "texto", "texto": "los espejos guardan secretos", 
                 "fuente": "mediana", "color": NEGRO + (255,), 
                 "efecto": "fade", "x": ANCHO//2, "y": 220, "delay": 0.8},
                 
                {"tipo": "sprite", "imagen": pingu_img, 
                 "x": ANCHO//2, "y": 350, "efecto": "fade"}
            ]
        },
        {  # Escena 1: Título principal
            "fondo": fondo_2,
            "duracion": 8.0,
            "elementos": [
                {"tipo": "texto", "texto": "REFLEJO PERDIDO", 
                 "fuente": "titulo", "color": NEGRO + (255,), 
                 "efecto": None, "x": ANCHO//2, "y": ALTO//2 - 100,
                 "con_sombra": False},
                 
                {"tipo": "sprite", "imagen": pingu_img, 
                 "x": ANCHO//2 - 120, "y": ALTO//2 + 50, "efecto": "wave"},
                 
                {"tipo": "sprite", "imagen": pygame.transform.flip(pingu_img, True, False), 
                 "x": ANCHO//2 + 120, "y": ALTO//2 + 50, "efecto": "wave"},
                 
                {"tipo": "texto", "texto": "¿Podrás completar el puzzle?", 
                 "fuente": 36, "color": NEGRO + (255,), 
                 "efecto": None, "x": ANCHO//2, "y": ALTO//2 + 150}
            ]
        },
        {  # Escena 2: Demo interactivo
            "fondo": fondo_3,
            "duracion": 10.0,
            "tipo": "demo"
        }
    ]

    class Escena:
        """Clase base para las escenas del trailer"""
        def __init__(self, definicion):
            self.fondo = definicion["fondo"]
            self.duracion = definicion["duracion"]
            self.elementos = []
            
            if "elementos" in definicion:
                for elem in definicion["elementos"]:
                    if elem["tipo"] == "texto":
                        self.elementos.append(
                            TextoPixel(
                                elem["texto"], elem["fuente"], elem["color"],
                                elem["x"], elem["y"], elem.get("efecto"), 
                                elem.get("duracion", 3.0), elem.get("con_sombra", True)
                            )
                        )
                    elif elem["tipo"] == "sprite":
                        pass
            
            self.tiempo_inicio = pygame.time.get_ticks()
        
        def actualizar(self, dt):
            """Actualiza todos los elementos de la escena"""
            for elem in self.elementos:
                if hasattr(elem, 'actualizar'):
                    elem.actualizar(dt)
        
        def dibujar(self, superficie):
            """Dibuja la escena completa"""
            superficie.blit(self.fondo, (0, 0))
            for elem in self.elementos:
                if hasattr(elem, 'dibujar'):
                    elem.dibujar(superficie)

    class EscenaDemo(Escena):
        """Escena con demo interactiva"""
        def __init__(self, definicion):
            super().__init__(definicion)
            self.demo = DemoControles()
        
        def actualizar(self, dt):
            """Actualiza la demo"""
            self.demo.actualizar(dt)
        
        def dibujar(self, superficie):
            """Dibuja la demo"""
            superficie.blit(self.fondo, (0, 0))
            self.demo.dibujar(superficie)
        
        def manejar_evento(self, evento):
            """Pasa los eventos a la demo"""
            self.demo.manejar_evento(evento)


    # Bucle principal del trailer
    escena_actual = 0
    escena = EscenaDemo(escenas[escena_actual]) if escenas[escena_actual].get("tipo") == "demo" else Escena(escenas[escena_actual])
    tiempo_escena = 0
    transicion_alpha = 0
    en_transicion = False
    reloj_trailer = pygame.time.Clock()  # Reloj específico para el trailer

    ejecutando_trailer = True
    while ejecutando_trailer:
        dt = reloj_trailer.tick(60) / 1500.0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if isinstance(escena, EscenaDemo):
                escena.manejar_evento(evento)
        
        escena.actualizar(dt)
        
        ventana.fill(NEGRO)
        escena.dibujar(ventana)
        
        # Transición entre escenas
        tiempo_escena += dt
        if tiempo_escena >= escena.duracion - 2.0 and not en_transicion:
            en_transicion = True
            transicion_alpha = 0
        
        if en_transicion:
            transicion_alpha += 255 * dt
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, min(255, int(transicion_alpha))))
            ventana.blit(overlay, (0, 0))
            
            if transicion_alpha >= 255:
                escena_actual += 1
                if escena_actual >= len(escenas):
                    ejecutando_trailer = False
                    break
                escena = EscenaDemo(escenas[escena_actual]) if escenas[escena_actual].get("tipo") == "demo" else Escena(escenas[escena_actual])
                tiempo_escena = 0
                en_transicion = False
        
        pygame.display.flip()

    # Transición al juego principal

# ======================================================================
# FUNCIONES DEL JUEGO PRINCIPAL
# ======================================================================


ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Reflejo Perdido")
fuente = pygame.font.SysFont("Arial", 24)
titulo_fuente = pygame.font.SysFont("Arial", 64, bold=True)
boton_fuente = pygame.font.SysFont("Arial", 30, bold=True)
reloj = pygame.time.Clock()
logo_img = pygame.image.load("img/logo.png").convert_alpha()
logo_img = pygame.transform.scale(logo_img, (440, 440))


# Variables de juego
niveles_desbloqueados = 1
nivel_actual = 0  # 0 significa ningún nivel iniciado
pantalla_actual = "menu"
mensaje = ""
reflejada = False   
ARCHIVO_PROGRESO = "progreso.json"
# Sprite o imágenes de las formas
imagen_fondo_nivel = pygame.image.load("Img/fondo.png").convert()
jugador_sprite = pygame.image.load("Img/penguin1.png").convert_alpha()
obstaculo_sprite = pygame.image.load("Img/polar.png").convert_alpha()
imagen_nuevo_juego = pygame.image.load("img/boton1.png").convert_alpha()
# Cargar imágenes de los niveles
fondo_seleccion = pygame.image.load("Img/fondo_niveles.jpg").convert()
fondo_seleccion = pygame.transform.scale(fondo_seleccion, (ANCHO, ALTO))
tam_cuadro = 60  # Asegúrate de que este valor sea coherente
imagen_nivel = pygame.transform.scale(pygame.image.load("Img/cuadro_level.png").convert_alpha(), (tam_cuadro, tam_cuadro))
imagen_seleccionado = pygame.transform.scale(pygame.image.load("Img/cuadro_level.png").convert_alpha(), (tam_cuadro, tam_cuadro))
imagen_bloqueado = pygame.transform.scale(pygame.image.load("Img/cuadro_bloqueo.png").convert_alpha(), (tam_cuadro, tam_cuadro))
imagen_boton_volver = pygame.image.load("Img/boton1.png").convert_alpha()




# Escalados de las imágenes
imagen_boton_volver = pygame.transform.scale(imagen_boton_volver, (110, 50))
imagen_nuevo_juego = pygame.transform.scale(imagen_nuevo_juego, (300, 130))
imagen_continuar = pygame.transform.scale(imagen_nuevo_juego, (250, 80))
imagen_salir = pygame.transform.scale(imagen_nuevo_juego, (250, 80))
imagen_fondo_nivel = pygame.transform.scale(imagen_fondo_nivel, (ANCHO, ALTO))
obstaculo_sprite = pygame.transform.scale(obstaculo_sprite, (TAM_CASILLA - 6, TAM_CASILLA - 6))
# Botones
boton_nuevo_rect = imagen_nuevo_juego.get_rect(center=(ANCHO//2, 390))
boton_continuar_rect = imagen_nuevo_juego.get_rect(center=(ANCHO//2, 460))
boton_salir_rect = imagen_nuevo_juego.get_rect(center=(ANCHO//2, 530))



# Niveles del juego
niveles = [
    {"figura_base": [(0, 0), (1, 0), (0, 1)], "jugador_pos": [1, 1], "objetivo_pos": [1, 1], "bloqueos": [], "reflejos": 1, "movimientos": 1},
    {"figura_base": [(0, 0), (1, 0), (1, 1)], "jugador_pos": [0, 2], "objetivo_pos": [2, 1], "bloqueos": [("pared", 1, 3)], "reflejos": 1, "movimientos": 3},
    {"figura_base": [(0, 0), (0, 1), (0, 2)], "jugador_pos": [0, 0], "objetivo_pos": [2, 2], "bloqueos": [("espejo", 1, 1)], "reflejos": 0, "movimientos": 4},
    {"figura_base": [(0, 0), (1, 0), (2, 0)], "jugador_pos": [0, 5], "objetivo_pos": [2, 1], "bloqueos": [("pared", 1, 5), ("espejo", 2, 4)], "reflejos": 0, "movimientos": 4},
    {"figura_base": [(0, 0), (1, 0), (0, 1), (1, 1)], "jugador_pos": [1, 4], "objetivo_pos": [1, 0], "bloqueos": [("pared", 2, 3), ("espejo", 0, 3)], "reflejos": 1, "movimientos": 6},
    {"figura_base": [(0, 0), (1, 0), (2, 0), (1, 1)], "jugador_pos": [0, 4], "objetivo_pos": [1, 0], "bloqueos": [("pared", 2, 2), ("espejo", 0, 2)], "reflejos": 1, "movimientos": 10},
    {"figura_base": [(0, 0), (0, 1), (1, 1), (2, 1)], "jugador_pos": [1, 4], "objetivo_pos": [0, 1], "bloqueos": [("espejo", 2, 3)], "reflejos": 1, "movimientos": 4},
    {"figura_base": [(0, 1), (1, 1), (2, 1), (2, 0), (2, 2)],"jugador_pos": [0, 0],"objetivo_pos": [2, 2],"bloqueos": [("pared", 1, 0), ("espejo", 1, 2), ("espejo", 0, 2)],"reflejos": 0,"movimientos": 4},
    {"figura_base": [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],"jugador_pos": [2, 0],"objetivo_pos": [0, 0],"bloqueos": [("pared", 1, 1), ("espejo", 2, 1)],"reflejos": 2,"movimientos": 6},
    {"figura_base": [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)],"jugador_pos": [0, 2],"objetivo_pos": [3, 0],"bloqueos": [("pared", 1, 0), ("pared", 0, 1), ("espejo", 2, 0)],"reflejos": 0,"movimientos": 5},
    {"figura_base": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],"jugador_pos": [0, 3],"objetivo_pos": [2, 2],"bloqueos": [("pared", 1, 2), ("espejo", 0, 2), ("espejo", 2, 2)],"reflejos": 0,"movimientos": 3}
]

# Cargar imagen de fondo
fondo = pygame.image.load("Img/fonfo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

def eliminar_fondo(imagen, umbral=240):
    imagen = imagen.convert()
    ancho, alto = imagen.get_size()
    imagen_alpha = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    for x in range(ancho):
        for y in range(alto):
            r, g, b, *_ = imagen.get_at((x, y))
            if r > umbral and g > umbral and b > umbral:
                imagen_alpha.set_at((x, y), (0, 0, 0, 0))
            else:
                imagen_alpha.set_at((x, y), (r, g, b, 255))
    return imagen_alpha

def crear_frames_pinguino():
    ruta = "Img/pinguino.jpg"
    imagen_original = pygame.image.load(ruta)
    imagen_original = pygame.transform.smoothscale(imagen_original, (80, 80))
    imagen_sin_fondo = eliminar_fondo(imagen_original)

    frames = []
    for angulo in range(0, 360, 45):
        rotado = pygame.transform.rotate(imagen_sin_fondo, angulo)
        frame = pygame.Surface((100, 100), pygame.SRCALPHA)
        frame.blit(rotado, (50 - rotado.get_width() // 2, 50 - rotado.get_height() // 2))
        frames.append(frame)
    return frames

class CopoNieve:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(-ALTO, -5)
        self.vel = random.uniform(1, 3)
        self.tam = random.randint(2, 4)
        self.angulo = random.uniform(0, 2 * math.pi)
    
    def actualizar(self):
        self.y += self.vel
        self.x += math.sin(self.angulo) * 1.5
        self.angulo += 0.05
        if self.y > ALTO + 10:
            self.reset()
    
copos_nieve = [CopoNieve() for _ in range(300)]

def dibujar_nieve(ventana):
    for copo in copos_nieve:
        copo.actualizar()
        pygame.draw.circle(ventana, (255, 255, 255), (int(copo.x), int(copo.y)), copo.tam)

def mostrar_pantalla_carga(duracion=5000):
    fuente = pygame.font.SysFont("Arial", 24, bold=True)
    frames_pinguino = crear_frames_pinguino()
    frame_actual = 0
    ultimo_frame = pygame.time.get_ticks()
    copos = [CopoNieve() for _ in range(100)]
    inicio = pygame.time.get_ticks()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        ahora = pygame.time.get_ticks()
        if ahora - ultimo_frame > 80:
            frame_actual = (frame_actual + 1) % len(frames_pinguino)
            ultimo_frame = ahora
        
        for copo in copos:
            copo.actualizar()

        ventana.blit(fondo, (0, 0))  # Fondo con imagen
        for copo in copos:
            pygame.draw.circle(ventana, COLOR_NIEVE, (int(copo.x), int(copo.y)), copo.tam)
        
        ventana.blit(frames_pinguino[frame_actual], (ANCHO // 2 - 50, ALTO // 2 - 50))
        texto = fuente.render("Cargando...", True, COLOR_TEXTO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 + 70))

        pygame.display.update()
        reloj.tick(60)

        if ahora - inicio > duracion:
            ejecutando = False

def cargar_frames_gif(ruta):
    gif = Image.open(ruta)
    frames = []
    try:
        while True:
            frame = gif.convert("RGBA")
            modo = frame.mode
            tam = frame.size
            datos = frame.tobytes()
            surface = pygame.image.fromstring(datos, tam, modo).convert_alpha()
            surface = pygame.transform.scale(surface, (ANCHO, ALTO))
            frames.append(surface)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Cargar los frames del fondo animado
fondos_menu = cargar_frames_gif("Img/inicio.gif")
indice_fondo = 0

def cargar_progreso():
    global niveles_desbloqueados, nivel_actual
    try:
        if os.path.exists(ARCHIVO_PROGRESO):
            with open(ARCHIVO_PROGRESO, 'r') as f:
                data = json.load(f)
                niveles_desbloqueados = data.get('niveles_desbloqueados', 1)
                nivel_actual = data.get('nivel_actual', 0)
                return nivel_actual > 0  # True si hay juego en progreso
    except:
        niveles_desbloqueados = 1
        nivel_actual = 0
    return False

def guardar_progreso():
    data = {
        'niveles_desbloqueados': niveles_desbloqueados,
        'nivel_actual': nivel_actual
    }
    with open(ARCHIVO_PROGRESO, 'w') as f:
        json.dump(data, f)

def cargar_nivel(n):
    global figura_base, jugador_pos, jugador_figura, reflejada
    global objetivo_pos, objetivo_figura, bloqueos
    global reflejos_restantes, movimientos_restantes, nivel_actual, mensaje
    datos = niveles[n]
    figura_base = datos["figura_base"]
    jugador_pos = list(datos["jugador_pos"])
    jugador_figura = list(figura_base)
    objetivo_pos = datos["objetivo_pos"]
    objetivo_figura = [(-x, y) for (x, y) in figura_base]
    bloqueos = datos.get("bloqueos", [])
    reflejos_restantes = datos.get("reflejos", 3)
    movimientos_restantes = datos.get("movimientos", 30)
    reflejada = False
    nivel_actual = n + 1  # Guardamos nivel actual +1 porque 0 es "ningún nivel"
    mensaje = ""
    
    guardar_progreso()
    return True

def reiniciar_nivel():
    global figura_base, jugador_pos, jugador_figura, reflejada
    global objetivo_pos, objetivo_figura, bloqueos
    global reflejos_restantes, movimientos_restantes, mensaje
    # Reiniciar las variables del nivel actual
    datos = niveles[nivel_actual - 1]  # El nivel actual es n+1, pero los índices de los niveles son 0-based
    figura_base = datos["figura_base"]
    jugador_pos = list(datos["jugador_pos"])
    jugador_figura = list(figura_base)
    objetivo_pos = datos["objetivo_pos"]
    objetivo_figura = [(-x, y) for (x, y) in figura_base]
    bloqueos = datos.get("bloqueos", [])
    reflejos_restantes = datos.get("reflejos", 3)
    movimientos_restantes = datos.get("movimientos", 30)
    reflejada = False
    mensaje = ""
    return True

def avanzar_nivel():
    global nivel_actual, niveles_desbloqueados, pantalla_actual, mensaje
    if nivel_actual >= len(niveles):
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill((0, 0, 0))
        for alpha in range(0, 255, 5):
            overlay.set_alpha(alpha)
            ventana.blit(overlay, (0, 0))
            pygame.display.update()
            pygame.time.delay(80)
        mostrar_creditos()
        mensaje = "¡Has completado todos los niveles!"
        guardar_progreso()
    else:
        if nivel_actual >= niveles_desbloqueados - 1:  # -1 porque nivel_actual comienza en 0
            niveles_desbloqueados = nivel_actual + 1
        mostrar_pantalla_carga(1000)  # Mostrar pantalla de carga
        cargar_nivel(nivel_actual)

def figura_dentro_limites(figura, base_pos, limite_x):
    for dx, dy in figura:
        x = base_pos[0] + dx
        y = base_pos[1] + dy
        if x < 0 or x >= limite_x or y < 0 or y >= FILAS:
            return False
        if reflejada and x >= limite_x // 2:
            return False
        for tipo, bx, by in bloqueos:
            if tipo == "pared" and x == bx and y == by:
                return False
    return True

def mover_figura(dx, dy):
    global jugador_pos, movimientos_restantes, mensaje

    nueva_pos = [jugador_pos[0] + dx, jugador_pos[1] + dy]
    
    if figura_dentro_limites(jugador_figura, nueva_pos, COLUMNAS):
        jugador_pos = nueva_pos
        movimientos_restantes -= 1
        mensaje = ""
        if movimientos_restantes < 0:
            mensaje = "¡Te quedaste sin movimientos!"

# Función para centrar el grid y las figuras
def dibujar_grid():
    # Calculamos el margen para centrar el grid
    margen_x = (ANCHO - COLUMNAS * TAM_CASILLA) // 2
    margen_y = (ALTO - FILAS * TAM_CASILLA) // 2

    # Dibujar las líneas verticales
    for x in range(COLUMNAS + 1):
        pygame.draw.line(ventana, COLOR_LINEA, 
                         (margen_x + x * TAM_CASILLA, margen_y), 
                         (margen_x + x * TAM_CASILLA, margen_y + FILAS * TAM_CASILLA), 2)

    # Dibujar las líneas horizontales
    for y in range(FILAS + 1):
        pygame.draw.line(ventana, COLOR_LINEA, 
                         (margen_x, margen_y + y * TAM_CASILLA), 
                         (margen_x + COLUMNAS * TAM_CASILLA, margen_y + y * TAM_CASILLA), 2)

# Función para dibujar figuras centradas
def dibujar_figura(figura, base_pos, imagen):
    margen_x = (ANCHO - COLUMNAS * TAM_CASILLA) // 2
    margen_y = (ALTO - FILAS * TAM_CASILLA) // 2

    for dx, dy in figura:
        x = base_pos[0] + dx
        y = base_pos[1] + dy
        sprite_escalado = pygame.transform.scale(imagen, (TAM_CASILLA - 4, TAM_CASILLA - 4))
        ventana.blit(sprite_escalado, 
                     (margen_x + x * TAM_CASILLA + 2, margen_y + y * TAM_CASILLA + 2))


# Función para dibujar los bloqueos centrados
def dibujar_bloqueos():
    margen_x = (ANCHO - COLUMNAS * TAM_CASILLA) // 2
    margen_y = (ALTO - FILAS * TAM_CASILLA) // 2

    for tipo, x, y in bloqueos:
        if tipo == "pared":
            ventana.blit(obstaculo_sprite, (
                margen_x + x * TAM_CASILLA + 2,
                margen_y + y * TAM_CASILLA + 2
            ))
        else:  # espejos u otros
            pygame.draw.rect(ventana, COLOR_ESPEJO,
                (margen_x + x * TAM_CASILLA + 2,
                 margen_y + y * TAM_CASILLA + 2,
                 TAM_CASILLA - 4, TAM_CASILLA - 4), border_radius=8)

def figuras_coinciden():
    jugador_real = [(jugador_pos[0] + dx, jugador_pos[1] + dy) for dx, dy in jugador_figura]
    objetivo_real = [(COLUMNAS // 2 + objetivo_pos[0] + dx, objetivo_pos[1] + dy) for dx, dy in objetivo_figura]
    jugador_real_trasladado = [(x + COLUMNAS // 2, y) for x, y in jugador_real]
    return set(jugador_real_trasladado) == set(objetivo_real)

def dibujar_texto_con_sombra(texto, fuente, color_texto, color_sombra, rect, offset=(2, 2)):
    # Sombra
    sombra = fuente.render(texto, True, color_sombra)
    ventana.blit(sombra, (
        rect.centerx - sombra.get_width() // 2 + offset[0],
        rect.centery - sombra.get_height() // 2 + offset[1]
    ))
    # Texto principal
    render = fuente.render(texto, True, color_texto)
    ventana.blit(render, (
        rect.centerx - render.get_width() // 2,
        rect.centery - render.get_height() // 2
    ))

def mostrar_menu():
    global pantalla_actual, nivel_actual, niveles_desbloqueados, indice_fondo
    pygame.mixer.music.load("Sonidos/fondo.wav")
    pygame.mixer.music.play(-1)  # -1 para que se repita en bucle
    
    # Mostrar logo en el centro superior
    logo_rect = logo_img.get_rect(center=(ANCHO // 2, 150))
    ventana.blit(logo_img, logo_rect)

    # Verificar si hay progreso guardado
    hay_progreso = cargar_progreso()
    indice_fondo = 0

    while pantalla_actual == "menu":
        ventana.blit(fondos_menu[indice_fondo], (0, 0))
        indice_fondo = (indice_fondo + 1) % len(fondos_menu)
        dibujar_nieve(ventana)
        logo_rect = logo_img.get_rect(center=(ANCHO // 2, 150))
        ventana.blit(logo_img, logo_rect)

        mouse_pos = pygame.mouse.get_pos()
        # --- NUEVO JUEGO ---
        if boton_nuevo_rect.collidepoint(mouse_pos):
            imagen_nuevo_scaled = pygame.transform.scale(imagen_nuevo_juego, (220, 60))
            # Redefinir el rectángulo de colisión con el tamaño escalado
            rect_nuevo = imagen_nuevo_scaled.get_rect(center=boton_nuevo_rect.center)
        else:
            imagen_nuevo_scaled = pygame.transform.scale(imagen_nuevo_juego, (200, 50))
            # Redefinir el rectángulo de colisión con el tamaño original
            rect_nuevo = imagen_nuevo_scaled.get_rect(center=boton_nuevo_rect.center)

        ventana.blit(imagen_nuevo_scaled, rect_nuevo.topleft)

        # --- CONTINUAR ---
        if hay_progreso:
            if boton_continuar_rect.collidepoint(mouse_pos):
                imagen_cont_scaled = pygame.transform.scale(imagen_nuevo_juego, (220, 60))
                rect_continuar = imagen_cont_scaled.get_rect(center=boton_continuar_rect.center)
            else:
                imagen_cont_scaled = pygame.transform.scale(imagen_nuevo_juego, (200, 50))
                rect_continuar = imagen_cont_scaled.get_rect(center=boton_continuar_rect.center)

            ventana.blit(imagen_cont_scaled, rect_continuar.topleft)

        # --- SALIR ---
        if boton_salir_rect.collidepoint(mouse_pos):
            imagen_salir_scaled = pygame.transform.scale(imagen_nuevo_juego, (220, 60))
            rect_salir = imagen_salir_scaled.get_rect(center=boton_salir_rect.center)
        else:
            imagen_salir_scaled = pygame.transform.scale(imagen_nuevo_juego, (200, 50))
            rect_salir = imagen_salir_scaled.get_rect(center=boton_salir_rect.center)

        ventana.blit(imagen_salir_scaled, rect_salir.topleft)

        # --- TEXTOS sobre botones ---
        COLOR_TEXTO = (255, 255, 255)
        COLOR_SOMBRA = (0, 0, 0)
        dibujar_texto_con_sombra("Nuevo Juego", fuente, COLOR_TEXTO, COLOR_SOMBRA, rect_nuevo)
        if hay_progreso:
            dibujar_texto_con_sombra("Continuar", fuente, COLOR_TEXTO, COLOR_SOMBRA, rect_continuar)
        dibujar_texto_con_sombra("Salir", fuente, COLOR_TEXTO, COLOR_SOMBRA, rect_salir)
        pygame.display.flip()
        reloj.tick(30)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_nuevo_rect.collidepoint(mouse_pos):
                    nivel_actual = 0
                    niveles_desbloqueados = 1
                    guardar_progreso()
                    ejecutar_trailer()
                    
                    pygame.mixer.music.stop()
                    pantalla_actual = "seleccion_niveles"
                elif hay_progreso and boton_continuar_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    pantalla_actual = "seleccion_niveles"
                elif boton_salir_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    pygame.mixer.music.stop()
                    sys.exit()

def mostrar_seleccion_niveles():
    global pantalla_actual, nivel_seleccionado, niveles_desbloqueados, mensaje
    pygame.mixer.music.load("Sonidos/niveles.wav")
    pygame.mixer.music.play(-1)

    # Botones
    boton_volver_rect = pygame.Rect(30, ALTO - 80, 150, 50)
    boton_jugar_rect = pygame.Rect(ANCHO//2 - 150, ALTO - 100, 300, 60)

    # Imágenes de botón
    imagen_boton = pygame.image.load("Img/boton1.png").convert_alpha()
    imagen_boton_jugar = pygame.transform.scale(imagen_boton, (300, 60))
    imagen_boton_volver = pygame.transform.scale(imagen_boton, (150, 50))

    if nivel_actual > 0:
        nivel_seleccionado = nivel_actual
    else:
        nivel_seleccionado = 1

    while pantalla_actual == "seleccion_niveles":
        ventana.blit(fondo_seleccion, (0, 0))
        dibujar_nieve(ventana)
        # Título
        titulo = titulo_fuente.render("Selecciona Nivel", True, AZUL)
        ventana.blit(titulo, ((ANCHO - titulo.get_width()) // 2, 50))

        # Mensaje de finalización
        if mensaje:
            texto_final = fuente.render(mensaje, True, COLOR_FIGURA)
            ventana.blit(texto_final, ((ANCHO - texto_final.get_width()) // 2, 120))
            mensaje = ""

        # Cuadrícula de niveles
        niveles_por_fila = 5
        espacio = 20
        inicio_x = (ANCHO - (niveles_por_fila * (tam_cuadro + espacio))) // 2
        inicio_y = 150

        for i in range(len(niveles)):
            fila = i // niveles_por_fila
            columna = i % niveles_por_fila
            x = inicio_x + columna * (tam_cuadro + espacio)
            y = inicio_y + fila * (tam_cuadro + espacio)

            if (i + 1) > niveles_desbloqueados:
                img = imagen_bloqueado
            elif (i + 1) == nivel_seleccionado:
                img = imagen_seleccionado
            else:
                img = imagen_nivel

            ventana.blit(img, (x, y))

            texto_nivel = fuente.render(str(i + 1), True, (255, 255, 255))
            ventana.blit(texto_nivel, (x + tam_cuadro//2 - texto_nivel.get_width()//2,
                                       y + tam_cuadro//2 - texto_nivel.get_height()//2))

            if i + 1 > niveles_desbloqueados:
                candado = fuente.render("X", True, (255, 255, 255))
                ventana.blit(candado, (x + tam_cuadro - 25, y + 5))

        # Mouse
        mouse_pos = pygame.mouse.get_pos()

        # Botón Jugar Nivel
        if nivel_seleccionado <= niveles_desbloqueados:
            if boton_jugar_rect.collidepoint(mouse_pos):
                imagen_jugar = pygame.transform.scale(imagen_boton, (330, 66))
                pos_jugar = (boton_jugar_rect.x - 15, boton_jugar_rect.y - 3)
            else:
                imagen_jugar = imagen_boton_jugar
                pos_jugar = (boton_jugar_rect.x, boton_jugar_rect.y)

            ventana.blit(imagen_jugar, pos_jugar)

            boton_jugar = boton_fuente.render(f"Jugar Nivel {nivel_seleccionado}", True, (255, 255, 255))
            ventana.blit(boton_jugar, (boton_jugar_rect.x + boton_jugar_rect.width//2 - boton_jugar.get_width()//2,
                                       boton_jugar_rect.y + boton_jugar_rect.height//2 - boton_jugar.get_height()//2))
    
        # Botón Volver
        if boton_volver_rect.collidepoint(mouse_pos):
            imagen_volver = pygame.transform.scale(imagen_boton, (165, 55))
            pos_volver = (boton_volver_rect.x - 7, boton_volver_rect.y - 2)
        else:
            imagen_volver = imagen_boton_volver
            pos_volver = (boton_volver_rect.x, boton_volver_rect.y)

        ventana.blit(imagen_volver, pos_volver)

        texto_volver = fuente.render("Volver", True, (255, 255, 255))
        ventana.blit(texto_volver, (boton_volver_rect.x + boton_volver_rect.width//2 - texto_volver.get_width()//2,
                                    boton_volver_rect.y + boton_volver_rect.height//2 - texto_volver.get_height()//2))

        pygame.display.flip()
        reloj.tick(30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and nivel_seleccionado > 1:
                    nivel_seleccionado -= 1
                elif evento.key == pygame.K_RIGHT and nivel_seleccionado < len(niveles):
                    nivel_seleccionado += 1
                elif evento.key == pygame.K_RETURN and nivel_seleccionado <= niveles_desbloqueados:
                    pantalla_actual = "juego"
                    cargar_nivel(nivel_seleccionado - 1)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Botón Volver al Menú
                if boton_volver_rect.collidepoint(mouse_pos):
                    pantalla_actual = "menu"
                    pygame.mixer.music.stop()
                
                # Botón Jugar Nivel
                elif (boton_jugar_rect.collidepoint(mouse_pos) and 
                      nivel_seleccionado <= niveles_desbloqueados):
                    pygame.mixer.music.stop()
                    pantalla_actual = "juego"
                    mostrar_pantalla_carga(2000)  # Mostrar pantalla de carga
                    cargar_nivel(nivel_seleccionado - 1)
                
                # Selección de niveles
                for i in range(len(niveles)):
                    fila = i // 5
                    columna = i % 5
                    x = inicio_x + columna * (tam_cuadro + espacio)
                    y = inicio_y + fila * (tam_cuadro + espacio)
                    if x <= mouse_pos[0] <= x + tam_cuadro and y <= mouse_pos[1] <= y + tam_cuadro:
                        if (i + 1) <= niveles_desbloqueados:
                            nivel_seleccionado = i + 1

# Cargar progreso al iniciar
cargar_progreso()
# Bucle principal del juego
while True:

    if pantalla_actual == "menu":
        mostrar_menu()
        
    elif pantalla_actual == "seleccion_niveles":
        mostrar_seleccion_niveles()
    elif pantalla_actual == "juego":
        ventana.blit(imagen_fondo_nivel,(0,0))
        
        # Panel de información
        pygame.draw.rect(ventana, COLOR_PANEL, (MARGEN+27, 10, 160, 80), border_radius=8)
        texto_reflejos = fuente.render(f"Reflejos: {reflejos_restantes}", True, COLOR_TEXTO)
        ventana.blit(texto_reflejos, (MARGEN + 40, 15))
        texto_movimientos = fuente.render(f"Movimientos: {movimientos_restantes}", True, COLOR_TEXTO)
        ventana.blit(texto_movimientos, (MARGEN + 40, 45))
        
        # Elementos del juego
        dibujar_grid()
        dibujar_bloqueos()
        pygame.draw.line(ventana, COLOR_LINEA, 
            (((ANCHO - COLUMNAS * TAM_CASILLA) // 2) + (COLUMNAS * TAM_CASILLA) // 2, (ALTO - FILAS * TAM_CASILLA) // 2), 
            (((ANCHO - COLUMNAS * TAM_CASILLA) // 2) + (COLUMNAS * TAM_CASILLA) // 2, (ALTO - FILAS * TAM_CASILLA) // 2 + FILAS * TAM_CASILLA), 8)



        dibujar_figura(jugador_figura, jugador_pos, jugador_sprite)
        dibujar_figura(objetivo_figura, [COLUMNAS // 2 + objetivo_pos[0], objetivo_pos[1]], jugador_sprite)

        
        # Botón Volver
        rect_boton_volver = pygame.Rect(ANCHO - 120, 15, 110, 40)
        ventana.blit(imagen_boton_volver, rect_boton_volver)
        texto_volver = fuente.render("Volver", True, (255, 255, 255))
        
        ventana.blit(texto_volver, (
            rect_boton_volver.x + 55 - texto_volver.get_width() // 2,
            rect_boton_volver.y + 10))
        
        # Mensajes
        if mensaje:
            resultado = fuente.render(mensaje, True, (0, 150, 0) if mensaje == "¡Correcto!" else (200, 0, 0))
            ventana.blit(resultado, (MARGEN, 100))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():

            pygame.mixer.init()  # Inicializa el módulo de sonido de Pygame
            sonido_mover = pygame.mixer.Sound("Sonidos/movimiento.wav")  # Carga el archivo de sonido
            pygame.mixer.init()  # Inicializa el módulo de sonido de Pygame
            sonido_avanzar = pygame.mixer.Sound("Sonidos/sonido_avanzar.wav")  # Carga el archivo de sonido
            pygame.mixer.init()  # Inicializa el módulo de sonido de Pygame
            sonido_incorrecto = pygame.mixer.Sound("Sonidos/error.wav")  # Carga el archivo de sonido
            
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ANCHO - 120 <= mouse_pos[0] <= ANCHO - 10 and 10 <= mouse_pos[1] <= 50:
                    pantalla_actual = "seleccion_niveles"
                    mensaje = ""
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if figuras_coinciden():
                        mensaje = "¡Correcto!"
                        pygame.display.update()
                        sonido_avanzar.play()
                        avanzar_nivel()
                    else:
                        mensaje = "¡Incorrecto!"
                        sonido_incorrecto.play()
                elif evento.key == pygame.K_f:
                    reiniciar_nivel()
                    sonido_mover.play()
                elif evento.key == pygame.K_r and reflejos_restantes > 0:
                    reflejada = not reflejada
                    jugador_figura = [(-x, y) for (x, y) in jugador_figura]
                    reflejos_restantes -= 1
                    sonido_mover.play()
                elif evento.key == pygame.K_e:
                    if movimientos_restantes > 0:
                        rotada = [(-dy, dx) for dx, dy in jugador_figura]
                        if figura_dentro_limites(rotada, jugador_pos, COLUMNAS):
                            jugador_figura = rotada
                            movimientos_restantes -= 1
                            sonido_mover.play()
                    else:
                        mensaje = "¡Sin movimientos!"

                else:
                    if movimientos_restantes > 0:
                        nueva_pos = jugador_pos[:]
                        movimiento = False  # bandera para saber si se movió

                        if evento.key == pygame.K_LEFT:
                            nueva_pos[0] -= 1
                            movimiento = True
                        elif evento.key == pygame.K_RIGHT:
                            nueva_pos[0] += 1
                            movimiento = True
                        elif evento.key == pygame.K_UP:
                            nueva_pos[1] -= 1
                            movimiento = True
                        elif evento.key == pygame.K_DOWN:
                            nueva_pos[1] += 1
                            movimiento = True

                        if movimiento and figura_dentro_limites(jugador_figura, nueva_pos, COLUMNAS):
                            jugador_pos = nueva_pos
                            movimientos_restantes -= 1
                            sonido_mover.play()
                    else:
                        mensaje = "¡Sin movimientos!"

                    sonido_mover.play()



        if not reflejada:
            base_x, base_y = jugador_pos
            for tipo, x, y in bloqueos:
                if tipo == "espejo" and x == base_x and y == base_y:
                    reflejada = True
                    jugador_figura = [(-dx, dy) for dx, dy in jugador_figura]
                    break
    
    reloj.tick(60)
