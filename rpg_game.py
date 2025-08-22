import random
import time
import os

class GameUtils:
    @staticmethod
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def pausa(mensaje="Presiona Enter para continuar..."):
        input(f"\n{mensaje}")

class InterfazUsuario:
    @staticmethod
    def mostrar_estado(jugador):
        print("\n" + "="*50)
        print(f"👤 {jugador.nombre} (Nivel {jugador.nivel})")
        print(f"❤️  Vida: {jugador.vida}/{jugador.vida_maxima}")
        print(f"💙 Maná: {jugador.mana}/{jugador.mana_maxima}")
        print(f"⚔️  Fuerza: {jugador.fuerza} | 🛡️  Defensa: {jugador.defensa}")
        print(f"⭐ EXP: {jugador.experiencia}/{jugador.exp_siguiente_nivel}")
        print(f"💰 Oro: {jugador.oro}")
        print(f"🗡️  Arma: {jugador.arma} | 🛡️  Armadura: {jugador.armadura}")
        print("="*50)

    @staticmethod
    def mostrar_inventario(jugador):
        print("\n📦 INVENTARIO:")
        if not jugador.inventario:
            print("Tu inventario está vacío.")
        else:
            for item, cantidad in jugador.inventario.items():
                print(f"  • {item}: {cantidad}")

    @staticmethod
    def mostrar_mapa(jugador, laberinto):
        print("\n🗺️  MAPA DEL LABERINTO:")
        print("="*40)
        for ubicacion, datos in laberinto.ubicaciones.items():
            estado = "✅" if datos["visitado"] else "❓"
            actual = " <- AQUÍ" if ubicacion == jugador.ubicacion else ""
            print(f"{estado} {ubicacion.replace('_', ' ').title()}{actual}")
        print("="*40)

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.nivel = 1
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.mana_maxima = 50
        self.mana = self.mana_maxima
        self.fuerza = 10
        self.defensa = 5
        self.experiencia = 0
        self.exp_siguiente_nivel = 100
        self.oro = 50
        self.inventario = {"Poción de vida": 2, "Poción de maná": 1}
        self.arma = "Espada oxidada"
        self.armadura = "Ropa vieja"
        self.ubicacion = "entrada"

    def subir_nivel(self):
        if self.experiencia >= self.exp_siguiente_nivel:
            self.nivel += 1
            self.vida_maxima += 20
            self.vida = self.vida_maxima
            self.mana_maxima += 10
            self.mana = self.mana_maxima
            self.fuerza += 3
            self.defensa += 2
            self.experiencia -= self.exp_siguiente_nivel
            self.exp_siguiente_nivel = int(self.exp_siguiente_nivel * 1.5)
            print(f"\n🌟 ¡NIVEL SUBIDO! Ahora eres nivel {self.nivel}!")
            print(f"Estadísticas mejoradas: Vida +20, Maná +10, Fuerza +3, Defensa +2")

    def usar_item(self, item):
        if item in self.inventario and self.inventario[item] > 0:
            if item == "Poción de vida":
                curacion = min(30, self.vida_maxima - self.vida)
                self.vida += curacion
                print(f"Recuperaste {curacion} puntos de vida. Vida actual: {self.vida}/{self.vida_maxima}")
            elif item == "Poción de maná":
                recuperacion = min(20, self.mana_maxima - self.mana)
                self.mana += recuperacion
                print(f"Recuperaste {recuperacion} puntos de maná. Maná actual: {self.mana}/{self.mana_maxima}")
            
            self.inventario[item] -= 1
            if self.inventario[item] == 0:
                del self.inventario[item]
            return True
        return False

class SistemaCombate:
    def __init__(self, interfaz):
        self.interfaz = interfaz
    
    def ejecutar_combate(self, jugador, enemigo):
        print(f"\n⚔️  ¡COMBATE CONTRA {enemigo.nombre.upper()}!")
        print(f"💀 {enemigo.nombre}: {enemigo.vida} HP")
        
        while jugador.vida > 0 and enemigo.vida > 0:
            print(f"\n❤️  Tu vida: {jugador.vida}/{jugador.vida_maxima}")
            print(f"💀 {enemigo.nombre}: {enemigo.vida}/{enemigo.vida_maxima}")
            
            if not self._turno_jugador(jugador, enemigo):
                continue  # Acción inválida, repetir turno
            
            # Ataque del enemigo (si sigue vivo)
            if enemigo.vida > 0:
                self._turno_enemigo(jugador, enemigo)
        
        return self._resolver_combate(jugador, enemigo)
    
    def _turno_jugador(self, jugador, enemigo):
        print("\n¿Qué quieres hacer?")
        print("1. Atacar")
        print("2. Usar hechizo (cuesta 10 maná)")
        print("3. Usar item")
        print("4. Intentar huir")
        
        eleccion = input("\nElige una opción (1-4): ").strip()
        
        if eleccion == "1":
            return self._atacar(jugador, enemigo)
        elif eleccion == "2":
            return self._usar_hechizo(jugador, enemigo)
        elif eleccion == "3":
            return self._usar_item(jugador)
        elif eleccion == "4":
            return self._intentar_huir()
        else:
            print("❌ Opción inválida.")
            return False
    
    def _atacar(self, jugador, enemigo):
        daño = max(1, jugador.fuerza + random.randint(-3, 3) - enemigo.defensa)
        enemigo.vida -= daño
        print(f"🗡️  ¡Atacaste a {enemigo.nombre} causando {daño} de daño!")
        return True
    
    def _usar_hechizo(self, jugador, enemigo):
        if jugador.mana >= 10:
            jugador.mana -= 10
            daño = max(1, int(jugador.fuerza * 1.5) + random.randint(0, 5) - enemigo.defensa)
            enemigo.vida -= daño
            print(f"✨ ¡Lanzaste un hechizo causando {daño} de daño!")
            return True
        else:
            print("❌ No tienes suficiente maná.")
            return False
    
    def _usar_item(self, jugador):
        self.interfaz.mostrar_inventario(jugador)
        if jugador.inventario:
            item = input("¿Qué item quieres usar? ").strip()
            if jugador.usar_item(item):
                return True
            else:
                print("❌ No tienes ese item o no puedes usarlo.")
                return False
        else:
            print("❌ No tienes items para usar.")
            return False
    
    def _intentar_huir(self):
        if random.random() < 0.3:  # 30% de probabilidad de huir
            print("💨 ¡Lograste escapar!")
            return "huir"
        else:
            print("❌ ¡No pudiste escapar!")
            return True
    
    def _turno_enemigo(self, jugador, enemigo):
        daño_enemigo = max(1, enemigo.ataque + random.randint(-2, 2) - jugador.defensa)
        jugador.vida -= daño_enemigo
        print(f"💥 {enemigo.nombre} te atacó causando {daño_enemigo} de daño!")
    
    def _resolver_combate(self, jugador, enemigo):
        if jugador.vida <= 0:
            print("\n💀 ¡HAS SIDO DERROTADO!")
            return False
        elif enemigo.vida <= 0:
            print(f"\n🎉 ¡Derrotaste a {enemigo.nombre}!")
            jugador.experiencia += enemigo.exp_recompensa
            jugador.oro += enemigo.oro_recompensa
            print(f"Ganaste {enemigo.exp_recompensa} EXP y {enemigo.oro_recompensa} oro!")
            jugador.subir_nivel()
            return True
        else:  # Jugador huyó
            return False

class GestorExploracion:
    def __init__(self, interfaz):
        self.interfaz = interfaz
    
    def explorar_ubicacion(self, jugador, laberinto, sistema_combate):
        ubicacion_actual = laberinto.ubicaciones[jugador.ubicacion]
        
        # Descripción de la ubicación
        print(f"\n🌍 {ubicacion_actual['descripcion']}")
        
        # Marcar como visitado y generar eventos
        if not ubicacion_actual["visitado"]:
            ubicacion_actual["visitado"] = True
            
            # Encuentro con enemigo
            if not self._manejar_encuentro_enemigo(jugador, ubicacion_actual, laberinto, sistema_combate):
                return False
            
            # Encontrar tesoro
            self._manejar_tesoro(jugador, ubicacion_actual)
        
        return True
    
    def _manejar_encuentro_enemigo(self, jugador, ubicacion_actual, laberinto, sistema_combate):
        if ubicacion_actual["enemigos"] and random.random() < 0.6:
            nombre_enemigo = random.choice(ubicacion_actual["enemigos"])
            enemigo_plantilla = laberinto.enemigos_disponibles[nombre_enemigo]
            
            # Crear nueva instancia para combate
            enemigo_combate = Enemigo(
                enemigo_plantilla.nombre, 
                enemigo_plantilla.vida_maxima,
                enemigo_plantilla.ataque, 
                enemigo_plantilla.defensa, 
                enemigo_plantilla.exp_recompensa, 
                enemigo_plantilla.oro_recompensa
            )
            
            print(f"\n⚠️  ¡Un {nombre_enemigo} aparece bloqueando tu camino!")
            return sistema_combate.ejecutar_combate(jugador, enemigo_combate)
        return True
    
    def _manejar_tesoro(self, jugador, ubicacion_actual):
        if ubicacion_actual["tesoros"] and random.random() < 0.4:
            tesoro = random.choice(ubicacion_actual["tesoros"])
            print(f"\n💎 ¡Encontraste: {tesoro}!")
            
            self._aplicar_efecto_tesoro(jugador, tesoro)
    
    def _aplicar_efecto_tesoro(self, jugador, tesoro):
        if tesoro == "Oro":
            oro_encontrado = random.randint(20, 50)
            jugador.oro += oro_encontrado
            print(f"Ganaste {oro_encontrado} piezas de oro!")
        elif tesoro in ["Poción de vida", "Poción de maná"]:
            jugador.inventario[tesoro] = jugador.inventario.get(tesoro, 0) + 1
        elif tesoro == "Espada élfica":
            jugador.arma = "Espada élfica"
            jugador.fuerza += 5
            print("¡Tu fuerza aumentó en 5 puntos!")
        elif tesoro == "Armadura bendita":
            jugador.armadura = "Armadura bendita"
            jugador.defensa += 8
            print("¡Tu defensa aumentó en 8 puntos!")

class Enemigo:
    def __init__(self, nombre, vida, ataque, defensa, exp_recompensa, oro_recompensa):
        self.nombre = nombre
        self.vida_maxima = vida
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.exp_recompensa = exp_recompensa
        self.oro_recompensa = oro_recompensa

class Laberinto:
    def __init__(self):
        self.ubicaciones = {
            "entrada": {
                "descripcion": "Estás en la entrada del misterioso Laberinto del Tiempo. Puedes ver tres caminos.",
                "conexiones": {"norte": "bosque", "este": "cueva", "oeste": "ruinas"},
                "enemigos": [],
                "tesoros": [],
                "visitado": False
            },
            "bosque": {
                "descripcion": "Un bosque oscuro y misterioso. Los árboles susurran secretos antiguos.",
                "conexiones": {"sur": "entrada", "norte": "templo", "este": "lago"},
                "enemigos": ["Lobo salvaje", "Araña gigante"],
                "tesoros": ["Poción de vida"],
                "visitado": False
            },
            "cueva": {
                "descripcion": "Una cueva húmeda con cristales brillantes en las paredes.",
                "conexiones": {"oeste": "entrada", "norte": "mina", "este": "dragon_lair"},
                "enemigos": ["Murciélago vampiro", "Troll de cueva"],
                "tesoros": ["Gema mágica", "Oro"],
                "visitado": False
            },
            "ruinas": {
                "descripcion": "Ruinas de una civilización perdida. Hay inscripciones extrañas en las piedras.",
                "conexiones": {"este": "entrada", "norte": "biblioteca"},
                "enemigos": ["Esqueleto guerrero", "Espíritu vengativo"],
                "tesoros": ["Espada élfica", "Pergamino mágico"],
                "visitado": False
            },
            "templo": {
                "descripcion": "Un templo sagrado con una luz dorada que emana del altar.",
                "conexiones": {"sur": "bosque"},
                "enemigos": ["Guardián del templo"],
                "tesoros": ["Armadura bendita", "Reliquia sagrada"],
                "visitado": False
            },
            "lago": {
                "descripcion": "Un lago cristalino con una extraña niebla sobre su superficie.",
                "conexiones": {"oeste": "bosque"},
                "enemigos": ["Sirena malévola"],
                "tesoros": ["Tridente acuático"],
                "visitado": False
            },
            "mina": {
                "descripcion": "Una mina abandonada llena de túneles oscuros y ecos extraños.",
                "conexiones": {"sur": "cueva"},
                "enemigos": ["Golem de piedra"],
                "tesoros": ["Pico encantado", "Oro"],
                "visitado": False
            },
            "dragon_lair": {
                "descripcion": "¡La guarida del dragón! Un lugar ardiente lleno de tesoros... y peligro mortal.",
                "conexiones": {"oeste": "cueva"},
                "enemigos": ["Dragón ancestral"],
                "tesoros": ["Tesoro del dragón"],
                "visitado": False
            },
            "biblioteca": {
                "descripcion": "Una biblioteca antigua con libros que contienen conocimiento prohibido.",
                "conexiones": {"sur": "ruinas"},
                "enemigos": ["Bibliotecario fantasma"],
                "tesoros": ["Libro de hechizos", "Varita mágica"],
                "visitado": False
            }
        }
        
        self.enemigos_disponibles = {
            "Lobo salvaje": Enemigo("Lobo salvaje", 30, 12, 2, 25, 15),
            "Araña gigante": Enemigo("Araña gigante", 25, 15, 1, 30, 20),
            "Murciélago vampiro": Enemigo("Murciélago vampiro", 20, 18, 0, 20, 12),
            "Troll de cueva": Enemigo("Troll de cueva", 50, 20, 8, 50, 35),
            "Esqueleto guerrero": Enemigo("Esqueleto guerrero", 35, 16, 5, 40, 25),
            "Espíritu vengativo": Enemigo("Espíritu vengativo", 40, 22, 3, 45, 30),
            "Guardián del templo": Enemigo("Guardián del templo", 80, 25, 10, 100, 75),
            "Sirena malévola": Enemigo("Sirena malévola", 60, 28, 6, 80, 60),
            "Golem de piedra": Enemigo("Golem de piedra", 90, 30, 15, 120, 90),
            "Dragón ancestral": Enemigo("Dragón ancestral", 150, 40, 20, 300, 200),
            "Bibliotecario fantasma": Enemigo("Bibliotecario fantasma", 70, 35, 8, 90, 70)
        }

class Juego:
    def __init__(self):
        self.interfaz = InterfazUsuario()
        self.sistema_combate = SistemaCombate(self.interfaz)
        self.gestor_exploracion = GestorExploracion(self.interfaz)
        self.jugador = None
        self.laberinto = None
    
    def inicializar(self):
        GameUtils.limpiar_pantalla()
        print("🏰 ¡BIENVENIDO AL LABERINTO DEL TIEMPO! 🏰")
        print("\nUn lugar misterioso donde el tiempo fluye de manera extraña...")
        print("Debes explorar, luchar y sobrevivir para encontrar la salida.")
        
        nombre = input("\n¿Cuál es tu nombre, valiente aventurero? ").strip()
        if not nombre:
            nombre = "Aventurero"
        
        self.jugador = Jugador(nombre)
        self.laberinto = Laberinto()
        
        print(f"\n¡Bienvenido, {nombre}! Tu aventura comienza ahora...")
        time.sleep(2)
    
    def verificar_victoria(self):
        if (self.jugador.ubicacion == "dragon_lair" and 
            self.laberinto.ubicaciones["dragon_lair"]["visitado"]):
            print("\n🎉 ¡FELICIDADES! ¡HAS COMPLETADO EL LABERINTO DEL TIEMPO!")
            print("Has derrotado al dragón y encontrado el tesoro legendario.")
            print(f"Nivel final: {self.jugador.nivel}")
            print(f"Oro total: {self.jugador.oro}")
            return True
        return False
    
    def procesar_menu_principal(self):
        print(f"\n🌍 Estás en: {self.jugador.ubicacion.replace('_', ' ').title()}")
        
        print("\n¿Qué quieres hacer?")
        print("1. Ver estado")
        print("2. Ver inventario") 
        print("3. Usar item")
        print("4. Moverse")
        print("5. Ver mapa")
        print("6. Salir del juego")
        
        eleccion = input("\nElige una opción (1-6): ").strip()
        return self._ejecutar_accion(eleccion)
    
    def _ejecutar_accion(self, eleccion):
        if eleccion == "1":
            GameUtils.pausa()
            
        elif eleccion == "2":
            self.interfaz.mostrar_inventario(self.jugador)
            GameUtils.pausa()
            
        elif eleccion == "3":
            self.interfaz.mostrar_inventario(self.jugador)
            if self.jugador.inventario:
                item = input("¿Qué item quieres usar? ").strip()
                self.jugador.usar_item(item)
            GameUtils.pausa()
            
        elif eleccion == "4":
            return self._manejar_movimiento()
            
        elif eleccion == "5":
            self.interfaz.mostrar_mapa(self.jugador, self.laberinto)
            GameUtils.pausa()
            
        elif eleccion == "6":
            print("¡Gracias por jugar! ¡Hasta la próxima aventura!")
            return "salir"
            
        else:
            print("❌ Opción no válida.")
            GameUtils.pausa()
        
        return "continuar"
    
    def _manejar_movimiento(self):
        ubicacion_actual = self.laberinto.ubicaciones[self.jugador.ubicacion]
        
        print("\n🚪 Direcciones disponibles:")
        for direccion, destino in ubicacion_actual["conexiones"].items():
            print(f"  {direccion.title()} -> {destino.replace('_', ' ').title()}")
        
        direccion = input("\n¿A dónde quieres ir? ").strip().lower()
        if direccion in ubicacion_actual["conexiones"]:
            self.jugador.ubicacion = ubicacion_actual["conexiones"][direccion]
            print(f"Te diriges hacia {self.jugador.ubicacion.replace('_', ' ').title()}...")
            time.sleep(1)
            return "mover"
        else:
            print("❌ Dirección no válida.")
            GameUtils.pausa()
            return "continuar"
    
    def ejecutar(self):
        self.inicializar()
        
        while self.jugador.vida > 0:
            GameUtils.limpiar_pantalla()
            self.interfaz.mostrar_estado(self.jugador)
            
            if self.verificar_victoria():
                break
            
            # Explorar ubicación actual
            if not self.gestor_exploracion.explorar_ubicacion(
                self.jugador, self.laberinto, self.sistema_combate):
                continue
            
            # Procesar menú principal
            accion = self.procesar_menu_principal()
            if accion == "salir":
                break
        
        # Game Over
        if self.jugador.vida <= 0:
            print("\n💀 GAME OVER")
            print("Tu aventura ha llegado a su fin...")
            print(f"Alcanzaste el nivel {self.jugador.nivel}")

# Función principal mantenida para compatibilidad

def juego_principal():
    """Función de compatibilidad - usa la nueva arquitectura"""
    juego = Juego()
    juego.ejecutar()

if __name__ == "__main__":
    # Puedes usar cualquiera de las dos formas:
    juego_principal()  # Forma original
    # O directamente: Juego().ejecutar()