# Configuración de correo electrónico para el sistema de aprobaciones
import os

class EmailConfig:
    """Configuración para el servicio de correo electrónico"""
    
    def __init__(self):
        # Configuración SMTP - usar variables de entorno en producción
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', 'correo@empresa.com')
        self.smtp_password = os.getenv('SMTP_PASSWORD', 'password')
        self.use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() == 'true'
        
        # Configuración de correos
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@empresa.com')
        self.from_name = os.getenv('FROM_NAME', 'Sistema de Aprobaciones')
        
        # Plantillas de correo
        self.templates = {
            'initial_approval': {
                'subject': '📋 Solicitud de Aprobación Inicial - {documento_tipo}',
                'template': '''
Estimado/a {usuario_nombre},

Se ha recibido una nueva solicitud que requiere su aprobación inicial:

📄 Tipo de Documento: {documento_tipo}
🆔 ID de Solicitud: {solicitud_id}
👤 Solicitante: {solicitante_nombre} ({solicitante_email})
📅 Fecha de Solicitud: {fecha_solicitud}
💰 Monto/Valor: {monto}

📝 Descripción:
{descripcion}

👥 Usuarios involucrados:
{usuarios_lista}

🔗 Para revisar y aprobar la solicitud, ingrese al sistema:
{link_aprobacion}

⏰ Fecha límite para aprobación: {fecha_limite}

Saludos cordiales,
Sistema de Aprobaciones
                '''
            },
            'final_approval': {
                'subject': '✅ Aprobación Final Requerida - {documento_tipo}',
                'template': '''
Estimado/a {usuario_nombre},

La siguiente solicitud ha pasado la aprobación inicial y ahora requiere su aprobación final:

📄 Tipo de Documento: {documento_tipo}
🆔 ID de Solicitud: {solicitud_id}
👤 Solicitante: {solicitante_nombre} ({solicitante_email})
✅ Aprobado inicialmente por: {aprobador_inicial}
📅 Fecha de Aprobación Inicial: {fecha_aprobacion_inicial}
💰 Monto/Valor: {monto}

📝 Descripción:
{descripcion}

👥 Usuarios involucrados en el proceso:
{usuarios_lista}

🔗 Para revisar y dar aprobación final, ingrese al sistema:
{link_aprobacion}

⏰ Fecha límite para aprobación final: {fecha_limite}

Saludos cordiales,
Sistema de Aprobaciones
                '''
            },
            'approval_completed': {
                'subject': '🎉 Solicitud Aprobada Completamente - {documento_tipo}',
                'template': '''
Estimado/a {usuario_nombre},

Le informamos que la siguiente solicitud ha sido aprobada completamente:

📄 Tipo de Documento: {documento_tipo}
🆔 ID de Solicitud: {solicitud_id}
👤 Solicitante: {solicitante_nombre} ({solicitante_email})
✅ Aprobador Inicial: {aprobador_inicial}
✅ Aprobador Final: {aprobador_final}
📅 Fecha de Finalización: {fecha_finalizacion}
💰 Monto/Valor: {monto}

👥 Todos los usuarios involucrados:
{usuarios_lista}

El proceso de aprobación ha finalizado exitosamente.

Saludos cordiales,
Sistema de Aprobaciones
                '''
            }
        }
    
    def get_template(self, template_type):
        """Obtiene una plantilla de correo por tipo"""
        return self.templates.get(template_type, {})