# python
practicas de codigo de python

## 🎮 Plataforma de Juegos (Game Platform)

Una plataforma interactiva de juegos desarrollada en Python con múltiples juegos clásicos.

### 🚀 Cómo usar

```bash
# Ejecutar la plataforma interactiva
python3 PlataformaJuegos.py

# Ver demostración de funcionalidades
python3 demo_plataforma.py

# Ejecutar pruebas
python3 test_plataforma.py
```

### 🎯 Juegos Disponibles

1. **🪨📄✂️ Piedra, Papel, Tijeras**
   - Juego clásico contra la computadora
   - Sistema de puntuación
   - Feedback visual con emojis

2. **🎲 Adivinanza de Números**
   - Adivina un número entre 1 y 100
   - 7 intentos máximo
   - Sistema de pistas (frío/tibio/caliente)

3. **🔢 Calculadora**
   - Operaciones básicas (+, -, ×, ÷)
   - Manejo de errores (división por cero)
   - Integrada en la plataforma

### 🏗️ Arquitectura

- **Diseño modular** con clase base `JuegoBase`
- **Fácil extensión** para agregar nuevos juegos
- **Interfaz consistente** en español con emojis
- **Manejo de errores** robusto

### 📁 Archivos del Proyecto

- `PlataformaJuegos.py` - Plataforma principal y todos los juegos
- `demo_plataforma.py` - Demostración automática de funcionalidades
- `test_plataforma.py` - Pruebas unitarias básicas
- `CalculadoraConFunciones.py` - Calculadora original con funciones
- `CalculadoraConCiclo.py` - Calculadora con ciclo while
- `CalculadoraSinCiclo.py` - Calculadora sin ciclo
