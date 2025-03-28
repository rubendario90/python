def calculadora():
    print("🔢 Bienvenido a la Calculadora. Escribe 'q' en la operación para salir.")
    
    while True:
        try:
            num1 = float(input("Digite su primer número: "))
            num2 = float(input("Digite su segundo número: "))
        except ValueError:
            print("❌ Error: Ingresa un número válido.")
            continue

        operacion = input("Elige operación (+, -, *, /) o 'q' para salir: ")

        if operacion == "+":
            print("✅ Resultado: ", num1 + num2)
        elif operacion == "-":
            print("✅ Resultado: ", num1 - num2)
        elif operacion == "*":
            print("✅ Resultado: ", num1 * num2)
        elif operacion == "/":
            if num2 == 0:
                print("❌ Error: No se puede dividir por cero.")
            else:
                print("✅ Resultado: ", num1 / num2)
        elif operacion == "q":
            print("👋 Saliendo de la calculadora. ¡Adiós!")
            break
        else:
            print("❌ Operación no válida. Inténtalo de nuevo.")

calculadora()
            
