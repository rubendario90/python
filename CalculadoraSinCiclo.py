#calculadora de python sin ciclo while
def calculadora():
    print("🔢 Bienvenido a la Calculadora. Escribe 'q' en la operación para salir.")

    num1 = float(input("Digite su primer número: "))
    num2 = float(input("Digite su segundo número: "))
    operacion = input("Elige operación (+, -, *, /) o 'q' para salir: ")

    if operacion == "q":
        print("👋 Saliendo de la calculadora. ¡Adiós!")
        return  # Se usa return en lugar de break

    if operacion == "+":
        print("✅ Resultado:", num1 + num2)
    elif operacion == "-":
        print("✅ Resultado:", num1 - num2)
    elif operacion == "*":
        print("✅ Resultado:", num1 * num2)
    elif operacion == "/":
        if num2 == 0:
            print("❌ Error: No se puede dividir por cero.")
        else:
            print("✅ Resultado:", num1 / num2)
    else:
        print("❌ Operación no válida. Inténtalo de nuevo.")

calculadora()
