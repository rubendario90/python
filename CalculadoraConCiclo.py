#calculadora de python con bucle infinito
from consumption_reporter import ConsumptionReporter

def calculadora():
    print("🔢 Bienvenido a la Calculadora. Escribe 'q' en la operación para salir.")
    
    # Initialize consumption reporter
    reporter = ConsumptionReporter()
    
    while True:
        try:
            num1 = float(input("Digite su primer número: "))
            num2 = float(input("Digite su segundo número: "))
        except ValueError:
            print("❌ Error: Ingresa un número válido.")
            reporter.track_error("entrada_invalida")
            continue

        operacion = input("Elige operación (+, -, *, /) o 'q' para salir: ")

        if operacion == "+":
            resultado = num1 + num2
            print("✅ Resultado: ", resultado)
            reporter.track_operation("suma", num1, num2, resultado, success=True)
        elif operacion == "-":
            resultado = num1 - num2
            print("✅ Resultado: ", resultado)
            reporter.track_operation("resta", num1, num2, resultado, success=True)
        elif operacion == "*":
            resultado = num1 * num2
            print("✅ Resultado: ", resultado)
            reporter.track_operation("multiplicacion", num1, num2, resultado, success=True)
        elif operacion == "/":
            if num2 == 0:
                print("❌ Error: No se puede dividir por cero.")
                reporter.track_error("division_por_cero")
            else:
                resultado = num1 / num2
                print("✅ Resultado: ", resultado)
                reporter.track_operation("division", num1, num2, resultado, success=True)
        elif operacion == "q":
            print("👋 Saliendo de la calculadora. ¡Adiós!")
            reporter.track_operation("salir", success=True)
            break
        else:
            print("❌ Operación no válida. Inténtalo de nuevo.")
            reporter.track_error("operacion_invalida")

calculadora()
            
