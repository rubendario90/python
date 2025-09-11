from consumption_reporter import ConsumptionReporter

def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b == 0:
        return "❌ No se puede dividir por cero"
    return a / b

# Initialize consumption reporter
reporter = ConsumptionReporter()

while True:
    print("\n📌 Menú Calculadora")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Ver reporte de consumo")
    print("6. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "6":
        print("👋 Saliendo...")
        reporter.track_operation("salir", success=True)
        break
    
    if opcion == "5":
        print("\n" + reporter.generate_report())
        continue

    try:
        num1 = float(input("Ingrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))
    except ValueError:
        print("❌ Error: Ingresa números válidos.")
        reporter.track_error("entrada_invalida")
        continue

    if opcion == "1":
        resultado = sumar(num1, num2)
        print("✅ Resultado:", resultado)
        reporter.track_operation("suma", num1, num2, resultado, success=True)
    elif opcion == "2":
        resultado = restar(num1, num2)
        print("✅ Resultado:", resultado)
        reporter.track_operation("resta", num1, num2, resultado, success=True)
    elif opcion == "3":
        resultado = multiplicar(num1, num2)
        print("✅ Resultado:", resultado)
        reporter.track_operation("multiplicacion", num1, num2, resultado, success=True)
    elif opcion == "4":
        resultado = dividir(num1, num2)
        if isinstance(resultado, str):  # Error message
            print(resultado)
            reporter.track_error("division_por_cero")
        else:
            print("✅ Resultado:", resultado)
            reporter.track_operation("division", num1, num2, resultado, success=True)
    else:
        print("❌ Opción no válida.")
        reporter.track_error("operacion_invalida")
