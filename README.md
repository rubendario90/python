# python
practicas de codigo de python

## Calculadoras Disponibles

Este repositorio contiene tres implementaciones de calculadora con seguimiento de consumo:

- **CalculadoraSinCiclo.py** - Calculadora sin bucle while
- **CalculadoraConCiclo.py** - Calculadora con bucle infinito  
- **CalculadoraConFunciones.py** - Calculadora con funciones y menú (incluye opción de reporte)

## Nuevo: Sistema de Reporte de Consumos

### Funcionalidades
- Seguimiento automático de operaciones realizadas
- Registro de errores y tipos de error
- Estadísticas de uso por tipo de operación
- Reportes detallados de consumo
- Persistencia de datos entre sesiones

### Uso del Frontend de Reportes

```bash
# Ver reporte completo
python reporte_consumos_frontend.py report

# Ver estadísticas resumidas
python reporte_consumos_frontend.py stats

# Menú interactivo
python reporte_consumos_frontend.py

# Limpiar datos de consumo
python reporte_consumos_frontend.py clear

# Ayuda
python reporte_consumos_frontend.py help
```

### Archivos del Sistema
- **consumption_reporter.py** - Clase principal para tracking de consumo
- **reporte_consumos_frontend.py** - Frontend para generar reportes
- **test_consumption_reporter.py** - Tests unitarios del sistema
