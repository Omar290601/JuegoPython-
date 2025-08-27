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
