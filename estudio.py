import json
import os
import random
import time
from datetime import datetime, timedelta

class PatronProgramacion:
    def __init__(self, nombre, categoria, descripcion, codigo_ejemplo, casos_uso, dificultad):
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.codigo_ejemplo = codigo_ejemplo
        self.casos_uso = casos_uso
        self.dificultad = dificultad  # 1-5
        self.veces_estudiado = 0
        self.veces_correcto = 0
        self.ultima_revision = None
        self.proxima_revision = datetime.now()

class SistemaEstudio:
    def __init__(self):
        self.patrones = []
        self.progreso_usuario = {
            'nivel': 'Principiante',
            'patrones_dominados': 0,
            'sesiones_completadas': 0,
            'puntos_totales': 0,
            'racha_dias': 0,
            'ultima_sesion': None
        }
        self.cargar_patrones_base()
        self.cargar_progreso()
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self):
        print("🧠" + "="*60 + "🧠")
        print("        🎯 SISTEMA DE PATRONES DE PROGRAMACIÓN 🎯")
        print("         💡 Construye tu Biblioteca Mental 💡")
        print("🧠" + "="*60 + "🧠")
    
    def cargar_patrones_base(self):
        """Carga la biblioteca base de patrones"""
        patrones_base = [
            # PATRONES BÁSICOS
            PatronProgramacion(
                "Validación de Entrada",
                "Básico",
                "Patrón para validar entrada del usuario hasta que sea correcta",
                '''def validar_entrada(mensaje, tipo=int, validador=None):
    while True:
        try:
            valor = tipo(input(mensaje))
            if validador is None or validador(valor):
                return valor
            print("❌ Valor no válido")
        except ValueError:
            print("❌ Formato incorrecto")

# Uso:
edad = validar_entrada("Edad: ", int, lambda x: 0 < x < 150)''',
                ["Formularios", "Juegos", "CLI", "Configuración"],
                1
            ),
            
            PatronProgramacion(
                "Game Loop",
                "Básico", 
                "Bucle principal para juegos y aplicaciones interactivas",
                '''def game_loop():
    running = True
    while running:
        # 1. Manejar eventos/entrada
        events = handle_input()
        
        # 2. Actualizar lógica
        update_game_state(events)
        
        # 3. Renderizar
        render_screen()
        
        # 4. Controlar framerate
        time.sleep(1/60)  # 60 FPS
        
        # 5. Verificar condiciones de salida
        running = not should_quit()''',
                ["Juegos", "Simuladores", "Apps en tiempo real"],
                2
            ),
            
            PatronProgramacion(
                "Factory Method",
                "Creacional",
                "Crea objetos sin especificar la clase exacta",
                '''class CreadorEnemigo:
    @staticmethod
    def crear(tipo, nivel=1):
        enemigos = {
            'goblin': lambda: Goblin(nivel),
            'dragon': lambda: Dragon(nivel),
            'troll': lambda: Troll(nivel)
        }
        if tipo in enemigos:
            return enemigos[tipo]()
        raise ValueError(f"Tipo {tipo} no existe")

# Uso:
enemigo = CreadorEnemigo.crear('dragon', 5)''',
                ["Juegos", "APIs", "Sistemas modulares"],
                2
            ),
            
            PatronProgramacion(
                "Observer",
                "Comportamiento",
                "Notifica cambios automáticamente a múltiples objetos",
                '''class EventSystem:
    def __init__(self):
        self.listeners = {}
    
    def suscribir(self, evento, callback):
        if evento not in self.listeners:
            self.listeners[evento] = []
        self.listeners[evento].append(callback)
    
    def notificar(self, evento, data=None):
        if evento in self.listeners:
            for callback in self.listeners[evento]:
                callback(data)

# Uso:
events = EventSystem()
events.suscribir('jugador_muerte', lambda d: print("Game Over"))
events.notificar('jugador_muerte', {'score': 100})''',
                ["Interfaces gráficas", "Juegos", "Sistemas reactivos"],
                3
            ),
            
            PatronProgramacion(
                "Strategy",
                "Comportamiento", 
                "Intercambia algoritmos dinámicamente",
                '''class EstrategiaOrdenamiento:
    def ordenar(self, datos): raise NotImplementedError

class BubbleSort(EstrategiaOrdenamiento):
    def ordenar(self, datos):
        # Implementación bubble sort
        return sorted(datos)  # Simplificado

class QuickSort(EstrategiaOrdenamiento):  
    def ordenar(self, datos):
        # Implementación quicksort
        return sorted(datos)  # Simplificado

class Ordenador:
    def __init__(self, estrategia):
        self.estrategia = estrategia
    
    def ordenar(self, datos):
        return self.estrategia.ordenar(datos)''',
                ["Algoritmos", "IA de juegos", "Procesamiento de datos"],
                3
            ),
            
            PatronProgramacion(
                "Singleton",
                "Creacional",
                "Garantiza una sola instancia de una clase",
                '''class ConfigManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config = {}
            ConfigManager._initialized = True
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value

# Uso: Siempre la misma instancia
config1 = ConfigManager()
config2 = ConfigManager()
print(config1 is config2)  # True''',
                ["Configuración", "Logging", "Conexiones DB"],
                3
            ),
            
            PatronProgramacion(
                "Template Method",
                "Comportamiento",
                "Define el esqueleto de algoritmo, subclases implementan pasos",
                '''class AlgoritmoIA:
    def ejecutar_turno(self):
        self.analizar_situacion()
        accion = self.decidir_accion()
        self.ejecutar_accion(accion)
        self.evaluar_resultado()
    
    def analizar_situacion(self):
        # Común para todas las IA
        pass
    
    def decidir_accion(self): raise NotImplementedError
    def ejecutar_accion(self, accion): raise NotImplementedError
    def evaluar_resultado(self): pass

class IAAgresiva(AlgoritmoIA):
    def decidir_accion(self):
        return "atacar"
    
    def ejecutar_accion(self, accion):
        print(f"¡Ejecutando {accion} agresivamente!")''',
                ["IA de juegos", "Algoritmos", "Procesamiento por pasos"],
                4
            ),
            
            PatronProgramacion(
                "Command",
                "Comportamiento",
                "Encapsula acciones como objetos para deshacer/rehacer",
                '''class Command:
    def ejecutar(self): raise NotImplementedError
    def deshacer(self): raise NotImplementedError

class MoverJugador(Command):
    def __init__(self, jugador, dx, dy):
        self.jugador = jugador
        self.dx, self.dy = dx, dy
        self.pos_anterior = None
    
    def ejecutar(self):
        self.pos_anterior = (self.jugador.x, self.jugador.y)
        self.jugador.x += self.dx
        self.jugador.y += self.dy
    
    def deshacer(self):
        self.jugador.x, self.jugador.y = self.pos_anterior

class HistorialComandos:
    def __init__(self):
        self.comandos = []
    
    def ejecutar(self, comando):
        comando.ejecutar()
        self.comandos.append(comando)
    
    def deshacer(self):
        if self.comandos:
            self.comandos.pop().deshacer()''',
                ["Editores", "Juegos con undo", "Transacciones"],
                4
            ),
            
            PatronProgramacion(
                "State Machine",
                "Comportamiento",
                "Maneja diferentes estados y transiciones",
                '''class Estado:
    def manejar(self, contexto): raise NotImplementedError

class EstadoMenu(Estado):
    def manejar(self, juego):
        opcion = input("1.Jugar 2.Opciones 3.Salir: ")
        if opcion == "1":
            juego.cambiar_estado(EstadoJugando())
        elif opcion == "3":
            juego.cambiar_estado(EstadoSaliendo())

class EstadoJugando(Estado):
    def manejar(self, juego):
        # Lógica del juego
        if juego.jugador.vida <= 0:
            juego.cambiar_estado(EstadoGameOver())

class Juego:
    def __init__(self):
        self.estado = EstadoMenu()
    
    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
    
    def actualizar(self):
        self.estado.manejar(self)''',
                ["Juegos", "Interfaces", "Protocolos de red"],
                4
            ),
            
            PatronProgramacion(
                "Repository",
                "Arquitectural",
                "Abstrae el acceso a datos",
                '''class Repository:
    def crear(self, item): raise NotImplementedError
    def obtener(self, id): raise NotImplementedError  
    def actualizar(self, id, data): raise NotImplementedError
    def eliminar(self, id): raise NotImplementedError
    def listar(self): raise NotImplementedError

class UsuarioRepository(Repository):
    def __init__(self):
        self.usuarios = {}  # En memoria, podría ser DB
    
    def crear(self, usuario):
        id = len(self.usuarios) + 1
        self.usuarios[id] = usuario
        return id
    
    def obtener(self, id):
        return self.usuarios.get(id)
    
    # ... resto de métodos

# Uso:
repo = UsuarioRepository()
id = repo.crear({"nombre": "Juan", "email": "juan@test.com"})
usuario = repo.obtener(id)''',
                ["APIs", "Aplicaciones web", "Sistemas empresariales"],
                3
            )
        ]
        
        self.patrones = patrones_base
    
    def cargar_progreso(self):
        """Carga progreso desde archivo"""
        try:
            if os.path.exists('progreso_patrones.json'):
                with open('progreso_patrones.json', 'r') as f:
                    data = json.load(f)
                    self.progreso_usuario.update(data)
        except:
            pass  # Usar valores por defecto
    
    def guardar_progreso(self):
        """Guarda progreso en archivo"""
        try:
            with open('progreso_patrones.json', 'w') as f:
                json.dump(self.progreso_usuario, f, indent=2, default=str)
        except:
            pass
    
    def calcular_nivel(self):
        """Calcula nivel basado en patrones dominados"""
        dominados = self.progreso_usuario['patrones_dominados']
        if dominados < 3:
            return "Principiante"
        elif dominados < 6:
            return "Intermedio"
        elif dominados < 10:
            return "Avanzado"
        else:
            return "Experto"
    
    def mostrar_dashboard(self):
        self.limpiar_pantalla()
        self.mostrar_titulo()
        
        nivel = self.calcular_nivel()
        print(f"\n👤 PERFIL DEL ESTUDIANTE:")
        print(f"   🎯 Nivel: {nivel}")
        print(f"   🏆 Patrones Dominados: {self.progreso_usuario['patrones_dominados']}/{len(self.patrones)}")
        print(f"   📚 Sesiones Completadas: {self.progreso_usuario['sesiones_completadas']}")
        print(f"   ⭐ Puntos Totales: {self.progreso_usuario['puntos_totales']}")
        print(f"   🔥 Racha de Días: {self.progreso_usuario['racha_dias']}")
        
        # Estadísticas por categoría
        categorias = {}
        for patron in self.patrones:
            cat = patron.categoria
            if cat not in categorias:
                categorias[cat] = {'total': 0, 'dominados': 0}
            categorias[cat]['total'] += 1
            if patron.veces_correcto >= 3:  # Considerado dominado
                categorias[cat]['dominados'] += 1
        
        print(f"\n📊 PROGRESO POR CATEGORÍA:")
        for cat, stats in categorias.items():
            porcentaje = (stats['dominados'] / stats['total']) * 100
            barra = "█" * (stats['dominados'] * 2) + "░" * ((stats['total'] - stats['dominados']) * 2)
            print(f"   {cat:15} [{barra[:20]:20}] {porcentaje:5.1f}%")
    
    def seleccionar_patron_estudio(self):
        """Selecciona patrón usando repetición espaciada"""
        ahora = datetime.now()
        
        # Filtrar patrones que necesitan revisión
        necesitan_revision = [p for p in self.patrones if p.proxima_revision <= ahora]
        
        if not necesitan_revision:
            # Si ninguno necesita revisión, tomar los menos estudiados
            necesitan_revision = sorted(self.patrones, key=lambda p: p.veces_estudiado)[:3]
        
        # Priorizar por dificultad apropiada al nivel
        nivel = self.calcular_nivel()
        if nivel == "Principiante":
            necesitan_revision = [p for p in necesitan_revision if p.dificultad <= 2]
        elif nivel == "Intermedio":
            necesitan_revision = [p for p in necesitan_revision if p.dificultad <= 3]
        
        if not necesitan_revision:
            necesitan_revision = self.patrones[:3]  # Fallback
        
        return random.choice(necesitan_revision)
    
    def estudiar_patron(self, patron):
        """Sesión de estudio de un patrón"""
        self.limpiar_pantalla()
        print("📖" + "="*60 + "📖")
        print(f"        ESTUDIANDO: {patron.nombre}")
        print(f"        Categoría: {patron.categoria} | Dificultad: {'⭐' * patron.dificultad}")
        print("📖" + "="*60 + "📖")
        
        print(f"\n💡 DESCRIPCIÓN:")
        print(f"   {patron.descripcion}")
        
        print(f"\n🔧 CÓDIGO EJEMPLO:")
        print("-" * 50)
        print(patron.codigo_ejemplo)
        print("-" * 50)
        
        print(f"\n🎯 CASOS DE USO:")
        for i, caso in enumerate(patron.casos_uso, 1):
            print(f"   {i}. {caso}")
        
        input(f"\n📚 Presiona Enter cuando hayas estudiado el patrón...")
        
        # Quiz básico
        return self.quiz_patron(patron)
    
    def quiz_patron(self, patron):
        """Quiz sobre el patrón estudiado"""
        self.limpiar_pantalla()
        print("❓" + "="*60 + "❓")
        print(f"        QUIZ: {patron.nombre}")
        print("❓" + "="*60 + "❓")
        
        preguntas = self.generar_preguntas(patron)
        correctas = 0
        
        for i, pregunta in enumerate(preguntas, 1):
            print(f"\n🤔 Pregunta {i}/{len(preguntas)}:")
            print(f"   {pregunta['pregunta']}")
            
            for j, opcion in enumerate(pregunta['opciones'], 1):
                print(f"   {j}. {opcion}")
            
            try:
                respuesta = int(input(f"\nTu respuesta (1-{len(pregunta['opciones'])}): "))
                if 1 <= respuesta <= len(pregunta['opciones']):
                    if respuesta == pregunta['correcta']:
                        print("✅ ¡Correcto!")
                        correctas += 1
                    else:
                        print(f"❌ Incorrecto. La respuesta era: {pregunta['correcta']}")
                        print(f"💡 Explicación: {pregunta['explicacion']}")
                else:
                    print("❌ Opción no válida")
            except ValueError:
                print("❌ Respuesta inválida")
            
            time.sleep(2)
        
        porcentaje = (correctas / len(preguntas)) * 100
        
        print(f"\n🎯 RESULTADO:")
        print(f"   Correctas: {correctas}/{len(preguntas)} ({porcentaje:.1f}%)")
        
        # Actualizar estadísticas del patrón
        patron.veces_estudiado += 1
        if porcentaje >= 70:
            patron.veces_correcto += 1
            puntos = patron.dificultad * 10
            self.progreso_usuario['puntos_totales'] += puntos
            print(f"   🎉 ¡Ganaste {puntos} puntos!")
        
        # Programar próxima revisión (repetición espaciada)
        if porcentaje >= 80:
            dias_siguiente = min(patron.veces_correcto * 2, 30)
        else:
            dias_siguiente = 1
        
        patron.proxima_revision = datetime.now() + timedelta(days=dias_siguiente)
        patron.ultima_revision = datetime.now()
        
        input(f"\n⏎ Presiona Enter para continuar...")
        return porcentaje >= 70
    
    def generar_preguntas(self, patron):
        """Genera preguntas basadas en el patrón"""
        # Base de preguntas por patrón (simplificado)
        preguntas_base = {
            "Validación de Entrada": [
                {
                    "pregunta": "¿Cuál es el propósito principal de la validación de entrada?",
                    "opciones": ["Hacer código más largo", "Evitar errores y datos inválidos", "Complicar la aplicación"],
                    "correcta": 2,
                    "explicacion": "La validación previene errores y garantiza datos correctos"
                }
            ],
            "Factory Method": [
                {
                    "pregunta": "¿Qué ventaja ofrece el patrón Factory?",
                    "opciones": ["Código más rápido", "Desacopla creación de objetos", "Menos memoria"],
                    "correcta": 2,
                    "explicacion": "Factory desacopla la lógica de creación del código cliente"
                }
            ]
        }
        
        # Pregunta genérica si no hay específica
        preguntas_genericas = [
            {
                "pregunta": f"¿En qué categoría se clasifica el patrón {patron.nombre}?",
                "opciones": ["Creacional", "Estructural", "Comportamiento", "Básico"],
                "correcta": ["Creacional", "Estructural", "Comportamiento", "Básico"].index(patron.categoria) + 1,
                "explicacion": f"El patrón {patron.nombre} pertenece a la categoría {patron.categoria}"
            },
            {
                "pregunta": f"¿Cuál es un caso de uso típico del patrón {patron.nombre}?",
                "opciones": patron.casos_uso[:3] + ["Ninguna de las anteriores"],
                "correcta": 1,
                "explicacion": f"{patron.casos_uso[0]} es un caso de uso típico"
            }
        ]
        
        return preguntas_base.get(patron.nombre, preguntas_genericas)
    
    def sesion_estudio_rapida(self):
        """Sesión rápida de 15 minutos"""
        print("⚡ SESIÓN RÁPIDA INICIADA (15 minutos)")
        print("🎯 Estudiaremos 3 patrones en modo intensivo\n")
        
        patrones_sesion = []
        for _ in range(3):
            patron = self.seleccionar_patron_estudio()
            if patron not in patrones_sesion:
                patrones_sesion.append(patron)
        
        exitos = 0
        for i, patron in enumerate(patrones_sesion, 1):
            print(f"📚 Patrón {i}/3")
            if self.estudiar_patron(patron):
                exitos += 1
        
        self.progreso_usuario['sesiones_completadas'] += 1
        
        print(f"\n🎉 SESIÓN COMPLETADA!")
        print(f"   ✅ Patrones dominados en esta sesión: {exitos}/3")
        
        # Actualizar racha
        hoy = datetime.now().date()
        if self.progreso_usuario['ultima_sesion']:
            ultima = datetime.fromisoformat(self.progreso_usuario['ultima_sesion']).date()
            if hoy == ultima + timedelta(days=1):
                self.progreso_usuario['racha_dias'] += 1
            elif hoy != ultima:
                self.progreso_usuario['racha_dias'] = 1
        else:
            self.progreso_usuario['racha_dias'] = 1
        
        self.progreso_usuario['ultima_sesion'] = hoy.isoformat()
        
        # Actualizar patrones dominados
        self.progreso_usuario['patrones_dominados'] = sum(
            1 for p in self.patrones if p.veces_correcto >= 3
        )
        
        self.guardar_progreso()
    
    def explorar_biblioteca(self):
        """Navega por todos los patrones disponibles"""
        while True:
            self.limpiar_pantalla()
            print("📚" + "="*60 + "📚")
            print("               BIBLIOTECA DE PATRONES")
            print("📚" + "="*60 + "📚")
            
            # Agrupar por categoría
            por_categoria = {}
            for patron in self.patrones:
                if patron.categoria not in por_categoria:
                    por_categoria[patron.categoria] = []
                por_categoria[patron.categoria].append(patron)
            
            print(f"\n📖 CATÁLOGO COMPLETO ({len(self.patrones)} patrones):")
            
            opciones = []
            contador = 1
            for categoria, patrones in por_categoria.items():
                print(f"\n🏷️  {categoria.upper()}:")
                for patron in patrones:
                    dominio = "✅" if patron.veces_correcto >= 3 else "🔄" if patron.veces_estudiado > 0 else "❓"
                    dificultad = "⭐" * patron.dificultad
                    print(f"   {contador:2d}. {dominio} {patron.nombre:25} {dificultad}")
                    opciones.append(patron)
                    contador += 1
            
            print(f"\n{contador}. 🔙 Volver al menú principal")
            
            try:
                eleccion = int(input(f"\n🎯 Selecciona patrón (1-{contador}): "))
                if 1 <= eleccion < contador:
                    self.estudiar_patron(opciones[eleccion - 1])
                elif eleccion == contador:
                    break
                else:
                    print("❌ Opción no válida")
                    time.sleep(1)
            except ValueError:
                print("❌ Ingresa un número válido")
                time.sleep(1)
    
    def menu_principal(self):
        """Menú principal del sistema"""
        while True:
            self.mostrar_dashboard()
            
            print(f"\n🎮 OPCIONES DE ESTUDIO:")
            print(f"   1. ⚡ Sesión Rápida (15 min)")
            print(f"   2. 📚 Explorar Biblioteca")
            print(f"   3. 🎯 Estudiar Patrón Específico")
            print(f"   4. 📊 Ver Estadísticas Detalladas")
            print(f"   5. 🔄 Resetear Progreso")
            print(f"   6. ❌ Salir")
            
            try:
                opcion = int(input(f"\n🎮 Elige una opción (1-6): "))
                
                if opcion == 1:
                    self.sesion_estudio_rapida()
                elif opcion == 2:
                    self.explorar_biblioteca()
                elif opcion == 3:
                    patron = self.seleccionar_patron_estudio()
                    self.estudiar_patron(patron)
                elif opcion == 4:
                    self.ver_estadisticas_detalladas()
                elif opcion == 5:
                    self.resetear_progreso()
                elif opcion == 6:
                    print("\n🎓 ¡Sigue practicando! Los patrones son poder.")
                    self.guardar_progreso()
                    break
                else:
                    print("❌ Opción no válida")
                    time.sleep(1)
            
            except ValueError:
                print("❌ Ingresa un número válido")
                time.sleep(1)
    
    def ver_estadisticas_detalladas(self):
        """Muestra estadísticas completas"""
        self.limpiar_pantalla()
        print("📊" + "="*60 + "📊")
        print("               ESTADÍSTICAS DETALLADAS")
        print("📊" + "="*60 + "📊")
        
        # Patrón más/menos estudiado
        mas_estudiado = max(self.patrones, key=lambda p: p.veces_estudiado)
        menos_estudiado = min(self.patrones, key=lambda p: p.veces_estudiado)
        
        print(f"\n🏆 PATRÓN MÁS ESTUDIADO:")
        print(f"   {mas_estudiado.nombre} ({mas_estudiado.veces_estudiado} veces)")
        
        print(f"\n📝 PATRÓN MENOS ESTUDIADO:")
        print(f"   {menos_estudiado.nombre} ({menos_estudiado.veces_estudiado} veces)")
        
        # Próximas revisiones
        print(f"\n⏰ PRÓXIMAS REVISIONES:")
        proximas = sorted(self.patrones, key=lambda p: p.proxima_revision)[:5]
        for patron in proximas:
            dias = (patron.proxima_revision - datetime.now()).days
            if dias <= 0:
                print(f"   🔥 {patron.nombre} - ¡HOY!")
            else:
                print(f"   📅 {patron.nombre} - En {dias} días")
        
        input(f"\n⏎ Presiona Enter para continuar...")
    
    def resetear_progreso(self):
        """Resetea todo el progreso"""
        confirmacion = input("\n⚠️  ¿Seguro que quieres resetear TODO el progreso? (escribe 'CONFIRMAR'): ")
        if confirmacion == "CONFIRMAR":
            self.progreso_usuario = {
                'nivel': 'Principiante',
                'patrones_dominados': 0,
                'sesiones_completadas': 0,
                'puntos_totales': 0,
                'racha_dias': 0,
                'ultima_sesion': None
            }
            for patron in self.patrones:
                patron.veces_estudiado = 0
                patron.veces_correcto = 0
                patron.proxima_revision = datetime.now()
            
            print("🔄 Progreso reseteado completamente")
            self.guardar_progreso()
        else:
            print("❌ Reseteo cancelado")
        time.sleep(2)

if __name__ == "__main__":
    sistema = SistemaEstudio()
    sistema.menu_principal()
