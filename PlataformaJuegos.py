# Plataforma de Juegos - Game Platform
# Sistema modular de juegos en Python

import random
import os

class JuegoBase:
    """Clase base para todos los juegos"""
    
    def __init__(self, nombre):
        self.nombre = nombre
    
    def mostrar_titulo(self):
        """Muestra el título del juego"""
        print(f"\n🎮 {self.nombre} 🎮")
        print("=" * (len(self.nombre) + 6))
    
    def jugar(self):
        """Método que debe ser implementado por cada juego"""
        raise NotImplementedError("Cada juego debe implementar el método jugar()")


class PiedraPapelTijeras(JuegoBase):
    """Juego de Piedra, Papel, Tijeras"""
    
    def __init__(self):
        super().__init__("Piedra, Papel, Tijeras")
        self.opciones = ["piedra", "papel", "tijeras"]
        self.puntos_jugador = 0
        self.puntos_computadora = 0
    
    def obtener_jugada_computadora(self):
        """Genera jugada aleatoria de la computadora"""
        return random.choice(self.opciones)
    
    def determinar_ganador(self, jugador, computadora):
        """Determina el ganador de una ronda"""
        if jugador == computadora:
            return "empate"
        elif (jugador == "piedra" and computadora == "tijeras") or \
             (jugador == "papel" and computadora == "piedra") or \
             (jugador == "tijeras" and computadora == "papel"):
            return "jugador"
        else:
            return "computadora"
    
    def mostrar_resultado_ronda(self, jugador, computadora, resultado):
        """Muestra el resultado de una ronda"""
        emojis = {"piedra": "🪨", "papel": "📄", "tijeras": "✂️"}
        
        print(f"\nTú: {emojis[jugador]} {jugador.title()}")
        print(f"Computadora: {emojis[computadora]} {computadora.title()}")
        
        if resultado == "empate":
            print("🤝 ¡Empate!")
        elif resultado == "jugador":
            print("✅ ¡Ganaste esta ronda!")
            self.puntos_jugador += 1
        else:
            print("❌ Gana la computadora esta ronda")
            self.puntos_computadora += 1
    
    def mostrar_puntuacion(self):
        """Muestra la puntuación actual"""
        print(f"\n📊 Puntuación:")
        print(f"Tú: {self.puntos_jugador} | Computadora: {self.puntos_computadora}")
    
    def jugar(self):
        """Juego principal de Piedra, Papel, Tijeras"""
        self.mostrar_titulo()
        print("🎯 ¡Vamos a jugar! Escribe 'salir' para terminar.")
        print("Opciones: piedra, papel, tijeras")
        
        while True:
            print("\n" + "-" * 30)
            jugada = input("Tu jugada: ").lower().strip()
            
            if jugada == "salir":
                break
            
            if jugada not in self.opciones:
                print("❌ Opción no válida. Usa: piedra, papel, tijeras")
                continue
            
            jugada_pc = self.obtener_jugada_computadora()
            resultado = self.determinar_ganador(jugada, jugada_pc)
            
            self.mostrar_resultado_ronda(jugada, jugada_pc, resultado)
            self.mostrar_puntuacion()
        
        # Resultado final
        print(f"\n🏆 Resultado Final:")
        if self.puntos_jugador > self.puntos_computadora:
            print("🎉 ¡Felicidades! ¡Ganaste el juego!")
        elif self.puntos_computadora > self.puntos_jugador:
            print("😅 La computadora ganó esta vez. ¡Inténtalo de nuevo!")
        else:
            print("🤝 ¡Empate total! Buen juego.")


class AdivinanzaNumeros(JuegoBase):
    """Juego de adivinanza de números"""
    
    def __init__(self):
        super().__init__("Adivinanza de Números")
        self.numero_secreto = 0
        self.intentos = 0
        self.max_intentos = 7
    
    def generar_numero_secreto(self, min_num=1, max_num=100):
        """Genera un número secreto aleatorio"""
        self.numero_secreto = random.randint(min_num, max_num)
        self.intentos = 0
    
    def dar_pista(self, intento):
        """Da una pista sobre el número"""
        diferencia = abs(self.numero_secreto - intento)
        
        if diferencia == 0:
            return "✅ ¡Correcto!"
        elif diferencia <= 5:
            return "🔥 ¡Muy caliente!"
        elif diferencia <= 15:
            return "♨️ Caliente"
        elif diferencia <= 25:
            return "🌡️ Tibio"
        else:
            direccion = "⬆️ más alto" if intento < self.numero_secreto else "⬇️ más bajo"
            return f"🧊 Frío - intenta {direccion}"
    
    def jugar(self):
        """Juego principal de adivinanza"""
        self.mostrar_titulo()
        print("🎯 Adivina el número secreto entre 1 y 100")
        print(f"⏱️ Tienes {self.max_intentos} intentos")
        
        self.generar_numero_secreto()
        
        while self.intentos < self.max_intentos:
            try:
                print(f"\nIntento {self.intentos + 1}/{self.max_intentos}")
                intento = int(input("¿Cuál es tu número? "))
                
                if intento < 1 or intento > 100:
                    print("❌ El número debe estar entre 1 y 100")
                    continue
                
                self.intentos += 1
                pista = self.dar_pista(intento)
                print(pista)
                
                if intento == self.numero_secreto:
                    print(f"🎉 ¡Excelente! Lo lograste en {self.intentos} intentos")
                    return
                
            except ValueError:
                print("❌ Por favor, ingresa un número válido")
        
        print(f"\n💔 Se acabaron los intentos. El número era: {self.numero_secreto}")
        print("¡Mejor suerte la próxima vez!")


class CalculadoraJuego(JuegoBase):
    """Integración de la calculadora como parte de la plataforma"""
    
    def __init__(self):
        super().__init__("Calculadora")
    
    def sumar(self, a, b):
        return a + b
    
    def restar(self, a, b):
        return a - b
    
    def multiplicar(self, a, b):
        return a * b
    
    def dividir(self, a, b):
        if b == 0:
            return "❌ No se puede dividir por cero"
        return a / b
    
    def jugar(self):
        """Calculadora integrada en la plataforma"""
        self.mostrar_titulo()
        print("🔢 Calculadora - Escribe 'salir' para volver al menú principal")
        
        while True:
            print("\n📌 Operaciones disponibles:")
            print("1. Sumar (+)")
            print("2. Restar (-)")
            print("3. Multiplicar (*)")
            print("4. Dividir (/)")
            print("5. Salir")
            
            opcion = input("Elige una opción (1-5): ").strip()
            
            if opcion == "5" or opcion.lower() == "salir":
                break
            
            if opcion not in ["1", "2", "3", "4"]:
                print("❌ Opción no válida")
                continue
            
            try:
                num1 = float(input("Primer número: "))
                num2 = float(input("Segundo número: "))
                
                if opcion == "1":
                    resultado = self.sumar(num1, num2)
                    print(f"✅ {num1} + {num2} = {resultado}")
                elif opcion == "2":
                    resultado = self.restar(num1, num2)
                    print(f"✅ {num1} - {num2} = {resultado}")
                elif opcion == "3":
                    resultado = self.multiplicar(num1, num2)
                    print(f"✅ {num1} × {num2} = {resultado}")
                elif opcion == "4":
                    resultado = self.dividir(num1, num2)
                    if isinstance(resultado, str):
                        print(resultado)
                    else:
                        print(f"✅ {num1} ÷ {num2} = {resultado}")
                        
            except ValueError:
                print("❌ Error: Ingresa números válidos")


class PlataformaJuegos:
    """Plataforma principal que gestiona todos los juegos"""
    
    def __init__(self):
        self.juegos = {
            "1": PiedraPapelTijeras(),
            "2": AdivinanzaNumeros(),
            "3": CalculadoraJuego()
        }
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la plataforma"""
        print("\n" + "=" * 50)
        print("🎮 PLATAFORMA DE JUEGOS EN PYTHON 🎮")
        print("=" * 50)
        print("\n🎯 Selecciona un juego:")
        print("1. 🪨📄✂️  Piedra, Papel, Tijeras")
        print("2. 🎲     Adivinanza de Números")
        print("3. 🔢     Calculadora")
        print("4. 🚪     Salir")
        print("\n" + "-" * 50)
    
    def ejecutar(self):
        """Ejecuta la plataforma principal"""
        print("🎉 ¡Bienvenido a la Plataforma de Juegos!")
        
        while True:
            self.mostrar_menu_principal()
            opcion = input("Elige una opción (1-4): ").strip()
            
            if opcion == "4":
                print("\n👋 ¡Gracias por jugar! ¡Hasta luego!")
                break
            
            if opcion in self.juegos:
                try:
                    self.juegos[opcion].jugar()
                    input("\n⏎ Presiona Enter para volver al menú principal...")
                except KeyboardInterrupt:
                    print("\n\n⚠️ Juego interrumpido. Volviendo al menú principal...")
            else:
                print("❌ Opción no válida. Selecciona 1, 2, 3 o 4.")
                input("⏎ Presiona Enter para continuar...")


def main():
    """Función principal"""
    try:
        plataforma = PlataformaJuegos()
        plataforma.ejecutar()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Adiós! Gracias por usar la plataforma de juegos.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, reporta este error.")


if __name__ == "__main__":
    main()