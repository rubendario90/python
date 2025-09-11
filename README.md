# Python - Sistema de Aprobaciones con Correos Electrónicos

## 📋 Descripción

Este repositorio contiene prácticas de código Python y un **Sistema de Aprobaciones con Correos Electrónicos** que resuelve problemas específicos de envío de correos y inclusión de usuarios en notificaciones.

## 🚀 Contenido del Repositorio

### Calculadoras Python (Prácticas originales)
- `CalculadoraConCiclo.py` - Calculadora con bucle infinito
- `CalculadoraConFunciones.py` - Calculadora usando funciones
- `CalculadoraSinCiclo.py` - Calculadora sin bucle while

### Sistema de Aprobaciones (Nuevo)
- `email_config.py` - Configuración y plantillas de correo
- `usuarios.py` - Gestión de usuarios y roles
- `servicio_email.py` - Servicio de envío y lógica de aprobación
- `main_aprobaciones.py` - Demostración del sistema
- `test_aprobaciones.py` - Tests del sistema
- `README_APROBACIONES.md` - Documentación completa

## 🎯 Problemas Resueltos

El Sistema de Aprobaciones fue desarrollado para resolver problemas específicos:

1. **✅ Correos de aprobación inicial y final no se enviaban**
2. **✅ Usuarios no se incluían en los correos de notificación**

## 🏃‍♂️ Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/rubendario90/python.git
cd python
```

### 2. Ejecutar la demostración
```bash
python main_aprobaciones.py
```

### 3. Ejecutar tests
```bash
python test_aprobaciones.py
```

## 📚 Documentación Completa

Para información detallada sobre el Sistema de Aprobaciones, consultar:
**[README_APROBACIONES.md](README_APROBACIONES.md)**

## 🛠️ Características Principales

- ✅ Sistema robusto de envío de correos con manejo de errores
- ✅ Inclusión completa de usuarios en todas las notificaciones
- ✅ Logging detallado para monitoreo y debugging
- ✅ Modo simulación para desarrollo
- ✅ Tests comprehensivos
- ✅ Configuración flexible via variables de entorno

## 📊 Flujo de Aprobación

1. **Creación** → Solicitud con usuarios involucrados
2. **Aprobación Inicial** → Correos a aprobadores (con lista de usuarios)
3. **Aprobación Final** → Correos finales (con lista de usuarios)  
4. **Notificación** → Todos los usuarios reciben confirmación final

## 🎉 Resultado

El sistema implementado resuelve completamente los problemas identificados y proporciona una base sólida para sistemas de aprobación empresariales.
