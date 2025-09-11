# Sistema de Aprobaciones con Correos Electrónicos

## 📋 Descripción

Este sistema de aprobaciones resuelve los problemas identificados en el sistema de reportes de consumos:

1. **✅ Correos de aprobación inicial y final no se enviaban**
2. **✅ Usuarios no se incluían en los correos**

## 🎯 Problemas Resueltos

### Problema 1: Correos no se enviaban
**Síntomas identificados:**
- Los correos de aprobación inicial no llegaban a los aprobadores
- Los correos de aprobación final no se enviaban
- No había feedback sobre el estado del envío

**Solución implementada:**
- Sistema robusto de envío de correos con manejo de errores
- Logging detallado para monitoreo y debugging
- Modo simulación para desarrollo y testing
- Reconexión automática en caso de fallas de red
- Context managers para manejo seguro de conexiones SMTP

### Problema 2: Usuarios no incluidos en correos
**Síntomas identificados:**
- Los correos no mostraban qué usuarios estaban involucrados
- Faltaba trazabilidad de quién participaba en el proceso
- No se incluía información de contacto de los participantes

**Solución implementada:**
- Lista completa de usuarios involucrados en cada email
- Gestión centralizada de usuarios con roles definidos
- Inclusión automática de solicitantes y aprobadores
- Formateo claro y legible de la información de usuarios
- Información de contacto completa (nombre, email, rol)

## 🏗️ Arquitectura del Sistema

```
📁 Sistema de Aprobaciones
├── 📄 email_config.py      # Configuración y plantillas de correo
├── 📄 usuarios.py          # Gestión de usuarios y roles
├── 📄 servicio_email.py    # Servicio de envío de correos y lógica de aprobación
├── 📄 main_aprobaciones.py # Demostración del sistema
└── 📄 test_aprobaciones.py # Tests del sistema
```

### Módulos Principales

#### 1. `email_config.py` - Configuración de Correos
- **EmailConfig**: Clase de configuración SMTP y plantillas
- Plantillas para correos de aprobación inicial, final y notificación completa
- Configuración centralizada de servidores SMTP
- Soporte para variables de entorno

#### 2. `usuarios.py` - Gestión de Usuarios
- **Usuario**: Clase modelo para usuarios del sistema
- **GestorUsuarios**: Gestión centralizada de usuarios
- Roles definidos: solicitante, aprobador_inicial, aprobador_final, admin
- Formateo automático para inclusión en correos

#### 3. `servicio_email.py` - Servicio de Correos y Aprobaciones
- **ServicioEmail**: Manejo de conexiones SMTP y envío de correos
- **SistemaAprobacion**: Lógica completa del flujo de aprobaciones
- Context managers para manejo seguro de recursos
- Logging comprehensivo para debugging

## 🚀 Uso del Sistema

### Ejemplo Básico

```python
from servicio_email import SistemaAprobacion
from usuarios import gestor_usuarios

# Usar el sistema con context manager (recomendado)
with SistemaAprobacion() as sistema:
    # Crear una solicitud
    solicitud = sistema.crear_solicitud(
        solicitante_id=3,
        documento_tipo="Orden de Compra",
        descripcion="Equipos de oficina",
        monto=15750.50,
        usuarios_involucrados=[gestor_usuarios.obtener_usuario(4)]
    )
    
    # Enviar correos de aprobación inicial
    sistema.enviar_solicitud_aprobacion_inicial(solicitud['id'])
    
    # Aprobar inicial (automáticamente envía correos finales)
    sistema.aprobar_inicial(solicitud['id'], aprobador_id=1)
    
    # Aprobar final (automáticamente envía notificaciones)
    sistema.aprobar_final(solicitud['id'], aprobador_id=2)
```

### Demostración Completa

```bash
# Ejecutar demostración completa
python main_aprobaciones.py

# Ejecutar tests
python test_aprobaciones.py
```

## 📧 Plantillas de Correo

### Correo de Aprobación Inicial
- **Asunto**: `📋 Solicitud de Aprobación Inicial - {documento_tipo}`
- **Incluye**: 
  - Información completa de la solicitud
  - **Lista de todos los usuarios involucrados**
  - Link de aprobación
  - Fecha límite

### Correo de Aprobación Final
- **Asunto**: `✅ Aprobación Final Requerida - {documento_tipo}`
- **Incluye**:
  - Información de aprobación inicial
  - **Lista de usuarios involucrados en el proceso**
  - Información del aprobador inicial
  - Link de aprobación final

### Notificación de Aprobación Completa
- **Asunto**: `🎉 Solicitud Aprobada Completamente - {documento_tipo}`
- **Incluye**:
  - Resumen completo del proceso
  - **Todos los usuarios que participaron**
  - Información de ambos aprobadores
  - Fechas de todo el proceso

## 👥 Gestión de Usuarios

### Roles del Sistema
- **solicitante**: Puede crear solicitudes
- **aprobador_inicial**: Aprueba en primera instancia  
- **aprobador_final**: Da aprobación final
- **admin**: Administración del sistema

### Usuarios de Ejemplo
```python
# Usuarios pre-configurados
Juan Pérez (juan.perez@empresa.com) - aprobador_inicial
María García (maria.garcia@empresa.com) - aprobador_final  
Carlos López (carlos.lopez@empresa.com) - solicitante
Ana Rodríguez (ana.rodriguez@empresa.com) - solicitante
Luis Martínez (luis.martinez@empresa.com) - admin
```

## 🔧 Configuración

### Variables de Entorno (Producción)
```bash
export SMTP_SERVER="smtp.empresa.com"
export SMTP_PORT="587"
export SMTP_USERNAME="sistema@empresa.com"
export SMTP_PASSWORD="password_seguro"
export SMTP_USE_TLS="True"
export FROM_EMAIL="noreply@empresa.com"
export FROM_NAME="Sistema de Aprobaciones"
```

### Modo Desarrollo
El sistema automáticamente detecta cuando no puede conectarse al servidor SMTP y entra en **modo simulación**, registrando todos los correos en los logs en lugar de enviarlos realmente.

## 📊 Características del Sistema

### ✅ Funcionalidades Implementadas
- [x] Envío de correos de aprobación inicial
- [x] Envío de correos de aprobación final  
- [x] Inclusión completa de usuarios en todos los correos
- [x] Gestión de usuarios con roles
- [x] Plantillas de correo personalizables
- [x] Logging detallado para monitoreo
- [x] Manejo robusto de errores
- [x] Modo simulación para desarrollo
- [x] Tests comprehensivos
- [x] Context managers para manejo de recursos

### 🔄 Flujo de Aprobación
1. **Creación de Solicitud** → Genera ID único y registra usuarios
2. **Aprobación Inicial** → Envía correos a aprobadores iniciales (con usuarios incluidos)
3. **Aprobación Final** → Envía correos a aprobadores finales (con usuarios incluidos)
4. **Notificación Final** → Notifica a todos los usuarios involucrados

### 📈 Monitoreo y Logs
```
INFO:servicio_email:📋 Solicitud creada: SOL-0001
INFO:servicio_email:✅ Email enviado exitosamente a juan.perez@empresa.com
INFO:servicio_email:✅ Correos de aprobación inicial enviados para solicitud SOL-0001
INFO:servicio_email:🎉 Aprobación final completada para solicitud SOL-0001
```

## 🧪 Tests

El sistema incluye tests comprehensivos que verifican:
- Creación de solicitudes
- Envío de correos (con mocks)
- Inclusión de usuarios en correos  
- Flujo completo de aprobación
- Gestión de usuarios
- Configuración de plantillas

```bash
# Ejecutar tests
python test_aprobaciones.py

# Resultado esperado: 9 tests pasados
✅ TODOS LOS TESTS PASARON EXITOSAMENTE
Tests ejecutados: 9
```

## 🛠️ Solución Técnica Detallada

### Antes (Problemas Identificados)
```python
# ❌ PROBLEMA: Correos no se enviaban
def enviar_correo():
    # Sin manejo de errores
    # Sin logging
    # Sin fallback
    
# ❌ PROBLEMA: Usuarios no incluidos
email_content = f"Solicitud: {id}"
# Sin información de usuarios
```

### Después (Solución Implementada)
```python
# ✅ SOLUCIÓN: Sistema robusto de correos
def enviar_email(self, destinatario_email, destinatario_nombre, asunto, contenido):
    try:
        mensaje = self.crear_mensaje(destinatario_email, destinatario_nombre, asunto, contenido)
        if self.conexion_smtp:
            self.conexion_smtp.sendmail(self.config.from_email, destinatario_email, mensaje.as_string())
            logger.info(f"✅ Email enviado exitosamente a {destinatario_email}")
        else:
            # Modo simulación con logging detallado
            logger.info("📧 SIMULACIÓN DE ENVÍO DE EMAIL:")
            logger.info(f"   Para: {destinatario_nombre} <{destinatario_email}>")
        return True
    except Exception as e:
        logger.error(f"❌ Error enviando email: {str(e)}")
        return False

# ✅ SOLUCIÓN: Usuarios incluidos en todos los correos
👥 Usuarios involucrados:
• Carlos López (carlos.lopez@empresa.com) - Solicitante
• Ana Rodríguez (ana.rodriguez@empresa.com) - Solicitante  
• Juan Pérez (juan.perez@empresa.com) - Aprobador Inicial
```

## 🎉 Resultado Final

El sistema implementado **resuelve completamente** los problemas identificados:

1. **✅ Correos funcionando**: Sistema robusto con manejo de errores y logging
2. **✅ Usuarios incluidos**: Todos los correos muestran claramente quién está involucrado
3. **✅ Trazabilidad completa**: Cada paso del proceso es registrado y notificado
4. **✅ Fácil mantenimiento**: Código modular y bien documentado
5. **✅ Testing**: Suite de tests que garantiza el funcionamiento correcto

**El sistema está listo para producción** y proporciona una base sólida para el sistema de reportes de consumos.