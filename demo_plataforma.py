#!/usr/bin/env python3
# Demo de la Plataforma de Juegos
# Muestra las funcionalidades principales de forma automática

from PlataformaJuegos import PiedraPapelTijeras, AdivinanzaNumeros, CalculadoraJuego
import time

def demo_piedra_papel_tijeras():
    """Demostración del juego Piedra, Papel, Tijeras"""
    print("\n🪨📄✂️ DEMO: Piedra, Papel, Tijeras")
    print("=" * 40)
    
    juego = PiedraPapelTijeras()
    
    # Simular algunas jugadas
    jugadas_demo = [
        ("piedra", "tijeras"),
        ("papel", "piedra"),
        ("tijeras", "papel"),
        ("piedra", "piedra")
    ]
    
    for jugador, computadora in jugadas_demo:
        resultado = juego.determinar_ganador(jugador, computadora)
        juego.mostrar_resultado_ronda(jugador, computadora, resultado)
        time.sleep(1)
    
    juego.mostrar_puntuacion()
    
def demo_adivinanza():
    """Demostración del juego de adivinanza"""
    print("\n🎲 DEMO: Adivinanza de Números")
    print("=" * 40)
    
    juego = AdivinanzaNumeros()
    juego.mostrar_titulo()
    
    # Simular una partida
    juego.generar_numero_secreto(1, 100)
    numero_secreto = juego.numero_secreto
    
    print(f"💡 Para esta demo, el número secreto es: {numero_secreto}")
    print("🎯 Simulando intentos...")
    
    intentos_demo = [25, 50, 75, numero_secreto - 10, numero_secreto]
    
    for intento in intentos_demo:
        if juego.intentos >= juego.max_intentos:
            break
            
        juego.intentos += 1
        pista = juego.dar_pista(intento)
        print(f"Intento {juego.intentos}: {intento} → {pista}")
        
        if intento == numero_secreto:
            print(f"🎉 ¡Adivinado en {juego.intentos} intentos!")
            break
        
        time.sleep(0.5)

def demo_calculadora():
    """Demostración de la calculadora"""
    print("\n🔢 DEMO: Calculadora")
    print("=" * 40)
    
    calc = CalculadoraJuego()
    calc.mostrar_titulo()
    
    # Simular operaciones
    operaciones_demo = [
        (calc.sumar, 15, 25, "+"),
        (calc.restar, 50, 20, "-"),
        (calc.multiplicar, 6, 7, "×"),
        (calc.dividir, 100, 4, "÷"),
        (calc.dividir, 10, 0, "÷")  # División por cero
    ]
    
    for operacion, a, b, simbolo in operaciones_demo:
        resultado = operacion(a, b)
        if isinstance(resultado, str) and "❌" in resultado:
            print(f"{a} {simbolo} {b} = {resultado}")
        else:
            print(f"✅ {a} {simbolo} {b} = {resultado}")
        time.sleep(0.5)

def main():
    """Ejecutar todas las demostraciones"""
    print("🎮 DEMOSTRACIÓN DE LA PLATAFORMA DE JUEGOS 🎮")
    print("=" * 60)
    print("🚀 Mostrando funcionalidades de todos los juegos...")
    
    try:
        demo_piedra_papel_tijeras()
        demo_adivinanza()
        demo_calculadora()
        
        print("\n" + "=" * 60)
        print("🎉 ¡Demo completada!")
        print("💡 Para usar la plataforma interactiva, ejecuta:")
        print("   python3 PlataformaJuegos.py")
        
    except Exception as e:
        print(f"\n❌ Error en la demostración: {e}")

if __name__ == "__main__":
    main()