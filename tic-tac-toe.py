import random
import os
import time

class JuegoDelGato:
    def __init__(self):
        self.tablero = [' ' for _ in range(9)]
        self.jugador_actual = 'X'
        self.modo_juego = None
        self.puntuacion = {'X': 0, 'O': 0, 'Empates': 0}
        self.nombres = {'X': 'Jugador 1', 'O': 'Jugador 2'}
        
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self):
        print("🎮" + "="*40 + "🎮")
        print("     🐱 JUEGO DEL GATO MEJORADO 🐱")
        print("🎮" + "="*40 + "🎮")
    
    def mostrar_tablero(self):
        print("\n   🎯 TABLERO ACTUAL:")
        print("   ┌───┬───┬───┐")
        print(f"   │ {self.tablero[0]} │ {self.tablero[1]} │ {self.tablero[2]} │")
        print("   ├───┼───┼───┤")
        print(f"   │ {self.tablero[3]} │ {self.tablero[4]} │ {self.tablero[5]} │")
        print("   ├───┼───┼───┤")
        print(f"   │ {self.tablero[6]} │ {self.tablero[7]} │ {self.tablero[8]} │")
        print("   └───┴───┴───┘")
        
        print("\n   📍 POSICIONES:")
        print("   ┌───┬───┬───┐")
        print("   │ 1 │ 2 │ 3 │")
        print("   ├───┼───┼───┤")
        print("   │ 4 │ 5 │ 6 │")
        print("   ├───┼───┼───┤")
        print("   │ 7 │ 8 │ 9 │")
        print("   └───┴───┴───┘")
    
    def mostrar_puntuacion(self):
        print("\n📊 PUNTUACIÓN:")
        print(f"   🎭 {self.nombres['X']} (X): {self.puntuacion['X']}")
        print(f"   🎭 {self.nombres['O']} (O): {self.puntuacion['O']}")
        print(f"   🤝 Empates: {self.puntuacion['Empates']}")
    
    def verificar_ganador(self):
        # Combinaciones ganadoras
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticales
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        
        for combo in combinaciones:
            if (self.tablero[combo[0]] == self.tablero[combo[1]] == 
                self.tablero[combo[2]] != ' '):
                return self.tablero[combo[0]]
        
        # Verificar empate
        if ' ' not in self.tablero:
            return 'Empate'
        
        return None
    
    def hacer_movimiento(self, posicion, simbolo):
        if self.tablero[posicion] == ' ':
            self.tablero[posicion] = simbolo
            return True
        return False
    
    def obtener_posiciones_vacias(self):
        return [i for i, casilla in enumerate(self.tablero) if casilla == ' ']
    
    def movimiento_ia_facil(self):
        """IA fácil - movimientos aleatorios"""
        posiciones_vacias = self.obtener_posiciones_vacias()
        return random.choice(posiciones_vacias)
    
    def movimiento_ia_medio(self):
        """IA medio - bloquea jugador y busca ganar"""
        # Primero: intentar ganar
        for pos in self.obtener_posiciones_vacias():
            tablero_temp = self.tablero.copy()
            tablero_temp[pos] = 'O'
            if self.verificar_ganador_temp(tablero_temp) == 'O':
                return pos
        
        # Segundo: bloquear al jugador
        for pos in self.obtener_posiciones_vacias():
            tablero_temp = self.tablero.copy()
            tablero_temp[pos] = 'X'
            if self.verificar_ganador_temp(tablero_temp) == 'X':
                return pos
        
        # Tercero: centro si está disponible
        if self.tablero[4] == ' ':
            return 4
        
        # Cuarto: esquinas
        esquinas = [0, 2, 6, 8]
        esquinas_vacias = [pos for pos in esquinas if self.tablero[pos] == ' ']
        if esquinas_vacias:
            return random.choice(esquinas_vacias)
        
        # Último: cualquier posición
        return random.choice(self.obtener_posiciones_vacias())
    
    def movimiento_ia_dificil(self):
        """IA difícil - algoritmo minimax simplificado"""
        return self.minimax(self.tablero, 'O')['posicion']
    
    def minimax(self, tablero, jugador):
        posiciones_vacias = [i for i, casilla in enumerate(tablero) if casilla == ' ']
        
        ganador = self.verificar_ganador_temp(tablero)
        if ganador == 'O':
            return {'puntaje': 1}
        elif ganador == 'X':
            return {'puntaje': -1}
        elif not posiciones_vacias:
            return {'puntaje': 0}
        
        movimientos = []
        
        for pos in posiciones_vacias:
            movimiento = {'posicion': pos}
            tablero[pos] = jugador
            
            if jugador == 'O':
                resultado = self.minimax(tablero, 'X')
                movimiento['puntaje'] = resultado['puntaje']
            else:
                resultado = self.minimax(tablero, 'O')
                movimiento['puntaje'] = resultado['puntaje']
            
            tablero[pos] = ' '
            movimientos.append(movimiento)
        
        if jugador == 'O':
            mejor_movimiento = max(movimientos, key=lambda x: x['puntaje'])
        else:
            mejor_movimiento = min(movimientos, key=lambda x: x['puntaje'])
        
        return mejor_movimiento
    
    def verificar_ganador_temp(self, tablero):
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        
        for combo in combinaciones:
            if (tablero[combo[0]] == tablero[combo[1]] == 
                tablero[combo[2]] != ' '):
                return tablero[combo[0]]
        
        if ' ' not in tablero:
            return 'Empate'
        
        return None
    
    def seleccionar_modo(self):
        self.limpiar_pantalla()
        self.mostrar_titulo()
        
        print("\n🎯 MODOS DE JUEGO:")
        print("   1. 👥 Dos Jugadores")
        print("   2. 🤖 Vs Computadora (Fácil)")
        print("   3. 🤖 Vs Computadora (Medio)")
        print("   4. 🤖 Vs Computadora (Difícil)")
        print("   5. 📊 Ver Estadísticas")
        print("   6. ❌ Salir")
        
        while True:
            try:
                opcion = int(input("\n🎮 Elige un modo (1-6): "))
                if 1 <= opcion <= 6:
                    if opcion == 1:
                        self.modo_juego = "dos_jugadores"
                        self.configurar_nombres()
                    elif opcion == 2:
                        self.modo_juego = "ia_facil"
                        self.nombres = {'X': 'Tú', 'O': 'Computadora (Fácil)'}
                    elif opcion == 3:
                        self.modo_juego = "ia_medio"
                        self.nombres = {'X': 'Tú', 'O': 'Computadora (Medio)'}
                    elif opcion == 4:
                        self.modo_juego = "ia_dificil"
                        self.nombres = {'X': 'Tú', 'O': 'Computadora (Difícil)'}
                    elif opcion == 5:
                        self.mostrar_estadisticas()
                        continue
                    elif opcion == 6:
                        return False
                    return True
                else:
                    print("❌ Por favor elige una opción válida (1-6)")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
    
    def configurar_nombres(self):
        print("\n👥 CONFIGURACIÓN DE JUGADORES:")
        nombre1 = input("🎭 Nombre del Jugador 1 (X): ").strip()
        nombre2 = input("🎭 Nombre del Jugador 2 (O): ").strip()
        
        self.nombres['X'] = nombre1 if nombre1 else "Jugador 1"
        self.nombres['O'] = nombre2 if nombre2 else "Jugador 2"
    
    def mostrar_estadisticas(self):
        self.limpiar_pantalla()
        self.mostrar_titulo()
        print("\n📈 ESTADÍSTICAS GENERALES:")
        total_partidas = self.puntuacion['X'] + self.puntuacion['O'] + self.puntuacion['Empates']
        
        if total_partidas > 0:
            print(f"   🎯 Total de partidas: {total_partidas}")
            print(f"   🏆 Victorias X: {self.puntuacion['X']} ({self.puntuacion['X']/total_partidas*100:.1f}%)")
            print(f"   🏆 Victorias O: {self.puntuacion['O']} ({self.puntuacion['O']/total_partidas*100:.1f}%)")
            print(f"   🤝 Empates: {self.puntuacion['Empates']} ({self.puntuacion['Empates']/total_partidas*100:.1f}%)")
        else:
            print("   📝 Aún no hay partidas registradas")
        
        input("\n⏎ Presiona Enter para continuar...")
    
    def jugar_partida(self):
        self.tablero = [' ' for _ in range(9)]
        self.jugador_actual = 'X'
        
        while True:
            self.limpiar_pantalla()
            self.mostrar_titulo()
            self.mostrar_puntuacion()
            self.mostrar_tablero()
            
            ganador = self.verificar_ganador()
            if ganador:
                self.mostrar_resultado(ganador)
                break
            
            print(f"\n🎯 Turno de: {self.nombres[self.jugador_actual]} ({self.jugador_actual})")
            
            if self.jugador_actual == 'X' or self.modo_juego == "dos_jugadores":
                # Turno del jugador humano
                self.turno_humano()
            else:
                # Turno de la IA
                self.turno_ia()
            
            # Cambiar jugador
            self.jugador_actual = 'O' if self.jugador_actual == 'X' else 'X'
    
    def turno_humano(self):
        while True:
            try:
                posicion = int(input("🎯 Elige una posición (1-9): ")) - 1
                if 0 <= posicion <= 8:
                    if self.hacer_movimiento(posicion, self.jugador_actual):
                        break
                    else:
                        print("❌ Esa posición ya está ocupada. Intenta otra.")
                else:
                    print("❌ Por favor elige un número entre 1 y 9")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
    
    def turno_ia(self):
        print("🤖 La computadora está pensando...")
        time.sleep(1)  # Pausa dramática
        
        if self.modo_juego == "ia_facil":
            posicion = self.movimiento_ia_facil()
        elif self.modo_juego == "ia_medio":
            posicion = self.movimiento_ia_medio()
        elif self.modo_juego == "ia_dificil":
            posicion = self.movimiento_ia_dificil()
        
        self.hacer_movimiento(posicion, self.jugador_actual)
        print(f"🤖 La computadora eligió la posición {posicion + 1}")
        time.sleep(1)
    
    def mostrar_resultado(self, ganador):
        print("\n" + "🎉" * 20)
        if ganador == 'Empate':
            print("🤝 ¡ES UN EMPATE! 🤝")
            self.puntuacion['Empates'] += 1
        else:
            print(f"🏆 ¡GANADOR: {self.nombres[ganador]}! 🏆")
            self.puntuacion[ganador] += 1
        print("🎉" * 20)
        
        # Mostrar tablero final
        self.mostrar_tablero()
    
    def preguntar_otra_partida(self):
        while True:
            respuesta = input("\n🎮 ¿Quieres jugar otra partida? (s/n): ").strip().lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif respuesta in ['n', 'no']:
                return False
            else:
                print("❌ Por favor responde 's' para sí o 'n' para no")
    
    def ejecutar(self):
        self.limpiar_pantalla()
        print("🎊 ¡Bienvenido al Juego del Gato Mejorado! 🎊")
        print("✨ Diviértete y demuestra tu estrategia ✨")
        time.sleep(2)
        
        while True:
            if not self.seleccionar_modo():
                break
            
            while True:
                self.jugar_partida()
                if not self.preguntar_otra_partida():
                    break
        
        self.limpiar_pantalla()
        self.mostrar_titulo()
        print("\n🎊 ¡GRACIAS POR JUGAR! 🎊")
        self.mostrar_estadisticas()
        print("👋 ¡Hasta la próxima!")

# Juego adicional: Adivinanza de Números
class JuegoAdivinanza:
    def __init__(self):
        self.rango_min = 1
        self.rango_max = 100
        self.numero_secreto = 0
        self.intentos = 0
        self.max_intentos = 7
        self.puntuacion = {'ganadas': 0, 'perdidas': 0}
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self):
        print("🔢" + "="*40 + "🔢")
        print("     🎯 ADIVINA EL NÚMERO 🎯")
        print("🔢" + "="*40 + "🔢")
    
    def configurar_dificultad(self):
        self.limpiar_pantalla()
        self.mostrar_titulo()
        
        print("\n🎯 SELECCIONA LA DIFICULTAD:")
        print("   1. 😊 Fácil (1-50, 8 intentos)")
        print("   2. 🤔 Medio (1-100, 7 intentos)")
        print("   3. 😰 Difícil (1-200, 6 intentos)")
        print("   4. 💀 Extremo (1-500, 5 intentos)")
        
        while True:
            try:
                opcion = int(input("\n🎮 Elige dificultad (1-4): "))
                if opcion == 1:
                    self.rango_max, self.max_intentos = 50, 8
                    print("😊 Dificultad: FÁCIL")
                elif opcion == 2:
                    self.rango_max, self.max_intentos = 100, 7
                    print("🤔 Dificultad: MEDIO")
                elif opcion == 3:
                    self.rango_max, self.max_intentos = 200, 6
                    print("😰 Dificultad: DIFÍCIL")
                elif opcion == 4:
                    self.rango_max, self.max_intentos = 500, 5
                    print("💀 Dificultad: EXTREMO")
                else:
                    print("❌ Opción no válida")
                    continue
                break
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        time.sleep(1)
    
    def jugar(self):
        self.configurar_dificultad()
        self.numero_secreto = random.randint(self.rango_min, self.rango_max)
        self.intentos = 0
        adivinanzas = []
        
        print(f"\n🎯 ¡Adivina el número entre {self.rango_min} y {self.rango_max}!")
        print(f"🎪 Tienes {self.max_intentos} intentos")
        
        while self.intentos < self.max_intentos:
            self.limpiar_pantalla()
            self.mostrar_titulo()
            
            print(f"\n🎯 Rango: {self.rango_min} - {self.rango_max}")
            print(f"🎪 Intentos restantes: {self.max_intentos - self.intentos}")
            
            if adivinanzas:
                print("\n📋 Tus intentos anteriores:")
                for i, (num, pista) in enumerate(adivinanzas, 1):
                    print(f"   {i}. {num} - {pista}")
            
            try:
                adivinanza = int(input(f"\n🔢 Ingresa tu número ({self.rango_min}-{self.rango_max}): "))
                
                if not (self.rango_min <= adivinanza <= self.rango_max):
                    print(f"❌ El número debe estar entre {self.rango_min} y {self.rango_max}")
                    input("⏎ Presiona Enter para continuar...")
                    continue
                
                self.intentos += 1
                
                if adivinanza == self.numero_secreto:
                    self.mostrar_victoria()
                    return True
                elif adivinanza < self.numero_secreto:
                    pista = "📈 Muy bajo"
                    adivinanzas.append((adivinanza, pista))
                else:
                    pista = "📉 Muy alto"
                    adivinanzas.append((adivinanza, pista))
                
                # Pistas adicionales
                diferencia = abs(adivinanza - self.numero_secreto)
                if diferencia <= 5:
                    pista += " - ¡MUY CERCA! 🔥"
                elif diferencia <= 15:
                    pista += " - Cerca 🎯"
                elif diferencia <= 30:
                    pista += " - Tibio 🌡️"
                else:
                    pista += " - Frío ❄️"
                
                adivinanzas[-1] = (adivinanza, pista)
                
            except ValueError:
                print("❌ Por favor ingresa un número válido")
                input("⏎ Presiona Enter para continuar...")
        
        self.mostrar_derrota()
        return False
    
    def mostrar_victoria(self):
        self.limpiar_pantalla()
        print("🎉" * 20)
        print("🏆 ¡FELICIDADES! ¡GANASTE! 🏆")
        print(f"🎯 El número era: {self.numero_secreto}")
        print(f"🎪 Lo lograste en {self.intentos} intento(s)")
        
        # Calcular puntuación
        puntos = (self.max_intentos - self.intentos + 1) * 10
        print(f"⭐ Puntuación: {puntos} puntos")
        print("🎉" * 20)
        
        self.puntuacion['ganadas'] += 1
    
    def mostrar_derrota(self):
        self.limpiar_pantalla()
        print("💀" * 20)
        print("😞 ¡Se acabaron los intentos!")
        print(f"🎯 El número era: {self.numero_secreto}")
        print("💪 ¡Inténtalo otra vez!")
        print("💀" * 20)
        
        self.puntuacion['perdidas'] += 1

# Menú principal para elegir juego
def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🎮" + "="*50 + "🎮")
        print("           🎊 MINI ARCADE DE JUEGOS 🎊")
        print("🎮" + "="*50 + "🎮")
        
        print("\n🎯 JUEGOS DISPONIBLES:")
        print("   1. 🐱 Gato (Tic-Tac-Toe)")
        print("   2. 🔢 Adivina el Número")
        print("   3. ❌ Salir")
        
        try:
            opcion = int(input("\n🎮 Elige un juego (1-3): "))
            
            if opcion == 1:
                juego_gato = JuegoDelGato()
                juego_gato.ejecutar()
            elif opcion == 2:
                juego_adivinanza = JuegoAdivinanza()
                while True:
                    juego_adivinanza.jugar()
                    if input("\n🎮 ¿Otra partida? (s/n): ").lower() not in ['s', 'si', 'sí']:
                        break
            elif opcion == 3:
                print("\n👋 ¡Gracias por jugar!")
                break
            else:
                print("❌ Opción no válida")
                input("⏎ Presiona Enter para continuar...")
        
        except ValueError:
            print("❌ Por favor ingresa un número válido")
            input("⏎ Presiona Enter para continuar...")

if __name__ == "__main__":
    menu_principal()
