#!/usr/bin/env python3
# Script de prueba para la plataforma de juegos

from PlataformaJuegos import PiedraPapelTijeras, AdivinanzaNumeros, CalculadoraJuego

def test_piedra_papel_tijeras():
    """Prueba básica del juego Piedra, Papel, Tijeras"""
    print("🧪 Probando Piedra, Papel, Tijeras...")
    juego = PiedraPapelTijeras()
    
    # Probar determinación de ganador
    assert juego.determinar_ganador("piedra", "tijeras") == "jugador"
    assert juego.determinar_ganador("papel", "piedra") == "jugador"
    assert juego.determinar_ganador("tijeras", "papel") == "jugador"
    assert juego.determinar_ganador("piedra", "piedra") == "empate"
    assert juego.determinar_ganador("piedra", "papel") == "computadora"
    
    print("✅ Piedra, Papel, Tijeras - Lógica correcta")

def test_adivinanza_numeros():
    """Prueba básica del juego de adivinanza"""
    print("🧪 Probando Adivinanza de Números...")
    juego = AdivinanzaNumeros()
    
    # Generar número y probar pistas
    juego.generar_numero_secreto(1, 100)
    assert 1 <= juego.numero_secreto <= 100
    
    # Probar pista exacta
    pista = juego.dar_pista(juego.numero_secreto)
    assert "✅ ¡Correcto!" in pista
    
    print("✅ Adivinanza de Números - Lógica correcta")

def test_calculadora():
    """Prueba básica de la calculadora"""
    print("🧪 Probando Calculadora...")
    calc = CalculadoraJuego()
    
    # Probar operaciones básicas
    assert calc.sumar(5, 3) == 8
    assert calc.restar(10, 4) == 6
    assert calc.multiplicar(3, 4) == 12
    assert calc.dividir(10, 2) == 5
    assert "❌" in calc.dividir(10, 0)
    
    print("✅ Calculadora - Operaciones correctas")

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas de la Plataforma de Juegos...")
    print("=" * 50)
    
    try:
        test_piedra_papel_tijeras()
        test_adivinanza_numeros()
        test_calculadora()
        
        print("\n" + "=" * 50)
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("La plataforma de juegos está lista para usar.")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()