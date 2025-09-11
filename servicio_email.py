# Servicio de correo electrónico para aprobaciones
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import datetime, timedelta
from email_config import EmailConfig
from usuarios import gestor_usuarios

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServicioEmail:
    """Servicio para envío de correos electrónicos de aprobación"""
    
    def __init__(self, config=None):
        self.config = config or EmailConfig()
        self.conexion_smtp = None
    
    def conectar_smtp(self):
        """Establece conexión con el servidor SMTP"""
        try:
            logger.info(f"Conectando a servidor SMTP: {self.config.smtp_server}:{self.config.smtp_port}")
            self.conexion_smtp = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            
            if self.config.use_tls:
                self.conexion_smtp.starttls()
                logger.info("TLS habilitado")
            
            # En un entorno real, descomentar para autenticación
            # self.conexion_smtp.login(self.config.smtp_username, self.config.smtp_password)
            logger.info("Conexión SMTP establecida exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a SMTP: {str(e)}")
            # En lugar de fallar, simularemos el envío para propósitos de demostración
            logger.warning("Modo simulación activado - los correos se registrarán en logs")
            return False
    
    def desconectar_smtp(self):
        """Cierra la conexión SMTP"""
        if self.conexion_smtp:
            try:
                self.conexion_smtp.quit()
                logger.info("Conexión SMTP cerrada")
            except:
                pass
            finally:
                self.conexion_smtp = None
    
    def crear_mensaje(self, destinatario_email, destinatario_nombre, asunto, contenido):
        """Crea el mensaje de correo electrónico"""
        mensaje = MIMEMultipart()
        mensaje['From'] = formataddr((self.config.from_name, self.config.from_email))
        mensaje['To'] = formataddr((destinatario_nombre, destinatario_email))
        mensaje['Subject'] = asunto
        
        # Agregar el contenido del mensaje
        mensaje.attach(MIMEText(contenido, 'plain', 'utf-8'))
        
        return mensaje
    
    def enviar_email(self, destinatario_email, destinatario_nombre, asunto, contenido):
        """Envía un correo electrónico"""
        try:
            # Crear el mensaje
            mensaje = self.crear_mensaje(destinatario_email, destinatario_nombre, asunto, contenido)
            
            # Intentar enviar
            if self.conexion_smtp:
                texto_mensaje = mensaje.as_string()
                self.conexion_smtp.sendmail(
                    self.config.from_email,
                    destinatario_email,
                    texto_mensaje
                )
                logger.info(f"✅ Email enviado exitosamente a {destinatario_email}")
            else:
                # Modo simulación - registrar en logs
                logger.info("📧 SIMULACIÓN DE ENVÍO DE EMAIL:")
                logger.info(f"   Para: {destinatario_nombre} <{destinatario_email}>")
                logger.info(f"   Asunto: {asunto}")
                logger.info(f"   Contenido:\n{contenido}")
                logger.info("   Estado: ✅ ENVIADO (SIMULADO)")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email a {destinatario_email}: {str(e)}")
            return False
    
    def enviar_emails_multiples(self, lista_destinatarios, asunto, contenido):
        """Envía el mismo email a múltiples destinatarios"""
        resultados = []
        
        for destinatario in lista_destinatarios:
            if hasattr(destinatario, 'email') and hasattr(destinatario, 'nombre'):
                resultado = self.enviar_email(
                    destinatario.email,
                    destinatario.nombre,
                    asunto,
                    contenido
                )
                resultados.append({
                    'email': destinatario.email,
                    'nombre': destinatario.nombre,
                    'enviado': resultado
                })
            else:
                logger.warning(f"Destinatario inválido: {destinatario}")
                resultados.append({
                    'email': 'unknown',
                    'nombre': 'unknown',
                    'enviado': False
                })
        
        return resultados

class SistemaAprobacion:
    """Sistema principal de aprobaciones con correos electrónicos"""
    
    def __init__(self):
        self.servicio_email = ServicioEmail()
        self.solicitudes = {}  # Almacenar solicitudes en memoria (en producción usar BD)
        self.contador_solicitudes = 1
    
    def __enter__(self):
        """Context manager - establecer conexión"""
        self.servicio_email.conectar_smtp()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager - cerrar conexión"""
        self.servicio_email.desconectar_smtp()
    
    def crear_solicitud(self, solicitante_id, documento_tipo, descripcion, monto, usuarios_involucrados=None):
        """Crea una nueva solicitud de aprobación"""
        solicitud_id = f"SOL-{self.contador_solicitudes:04d}"
        self.contador_solicitudes += 1
        
        solicitante = gestor_usuarios.obtener_usuario(solicitante_id)
        if not solicitante:
            raise ValueError(f"Solicitante con ID {solicitante_id} no encontrado")
        
        solicitud = {
            'id': solicitud_id,
            'solicitante': solicitante,
            'documento_tipo': documento_tipo,
            'descripcion': descripcion,
            'monto': monto,
            'usuarios_involucrados': usuarios_involucrados or [],
            'fecha_solicitud': datetime.now(),
            'estado': 'pendiente_inicial',
            'aprobador_inicial': None,
            'aprobador_final': None,
            'fecha_aprobacion_inicial': None,
            'fecha_aprobacion_final': None,
            'fecha_limite': datetime.now() + timedelta(days=7)
        }
        
        self.solicitudes[solicitud_id] = solicitud
        logger.info(f"📋 Solicitud creada: {solicitud_id}")
        return solicitud
    
    def enviar_solicitud_aprobacion_inicial(self, solicitud_id):
        """Envía correos para aprobación inicial"""
        solicitud = self.solicitudes.get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud {solicitud_id} no encontrada")
            return False
        
        # Obtener aprobadores iniciales
        aprobadores = gestor_usuarios.obtener_aprobadores_iniciales()
        if not aprobadores:
            logger.error("No hay aprobadores iniciales configurados")
            return False
        
        # Preparar datos para la plantilla
        template = self.servicio_email.config.get_template('initial_approval')
        usuarios_involucrados = solicitud['usuarios_involucrados'] + [solicitud['solicitante']]
        
        datos = {
            'documento_tipo': solicitud['documento_tipo'],
            'solicitud_id': solicitud['id'],
            'solicitante_nombre': solicitud['solicitante'].nombre,
            'solicitante_email': solicitud['solicitante'].email,
            'fecha_solicitud': solicitud['fecha_solicitud'].strftime('%d/%m/%Y %H:%M'),
            'monto': f"${solicitud['monto']:,.2f}",
            'descripcion': solicitud['descripcion'],
            'usuarios_lista': gestor_usuarios.formatear_lista_usuarios(usuarios_involucrados),
            'link_aprobacion': f"http://sistema.empresa.com/aprobar/{solicitud['id']}",
            'fecha_limite': solicitud['fecha_limite'].strftime('%d/%m/%Y')
        }
        
        # Enviar a cada aprobador inicial
        resultados = []
        for aprobador in aprobadores:
            datos['usuario_nombre'] = aprobador.nombre
            asunto = template['subject'].format(**datos)
            contenido = template['template'].format(**datos)
            
            resultado = self.servicio_email.enviar_email(
                aprobador.email,
                aprobador.nombre,
                asunto,
                contenido
            )
            resultados.append(resultado)
        
        if all(resultados):
            logger.info(f"✅ Correos de aprobación inicial enviados para solicitud {solicitud_id}")
            return True
        else:
            logger.error(f"❌ Error enviando algunos correos para solicitud {solicitud_id}")
            return False
    
    def aprobar_inicial(self, solicitud_id, aprobador_id):
        """Aprueba una solicitud en fase inicial"""
        solicitud = self.solicitudes.get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud {solicitud_id} no encontrada")
            return False
        
        aprobador = gestor_usuarios.obtener_usuario(aprobador_id)
        if not aprobador or aprobador.rol != 'aprobador_inicial':
            logger.error(f"Aprobador inicial {aprobador_id} no válido")
            return False
        
        solicitud['estado'] = 'pendiente_final'
        solicitud['aprobador_inicial'] = aprobador
        solicitud['fecha_aprobacion_inicial'] = datetime.now()
        
        logger.info(f"✅ Aprobación inicial completada para solicitud {solicitud_id}")
        
        # Enviar correos para aprobación final
        return self.enviar_solicitud_aprobacion_final(solicitud_id)
    
    def enviar_solicitud_aprobacion_final(self, solicitud_id):
        """Envía correos para aprobación final"""
        solicitud = self.solicitudes.get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud {solicitud_id} no encontrada")
            return False
        
        # Obtener aprobadores finales
        aprobadores = gestor_usuarios.obtener_aprobadores_finales()
        if not aprobadores:
            logger.error("No hay aprobadores finales configurados")
            return False
        
        # Preparar datos para la plantilla
        template = self.servicio_email.config.get_template('final_approval')
        usuarios_involucrados = solicitud['usuarios_involucrados'] + [solicitud['solicitante']]
        
        datos = {
            'documento_tipo': solicitud['documento_tipo'],
            'solicitud_id': solicitud['id'],
            'solicitante_nombre': solicitud['solicitante'].nombre,
            'solicitante_email': solicitud['solicitante'].email,
            'aprobador_inicial': solicitud['aprobador_inicial'].nombre,
            'fecha_aprobacion_inicial': solicitud['fecha_aprobacion_inicial'].strftime('%d/%m/%Y %H:%M'),
            'monto': f"${solicitud['monto']:,.2f}",
            'descripcion': solicitud['descripcion'],
            'usuarios_lista': gestor_usuarios.formatear_lista_usuarios(usuarios_involucrados),
            'link_aprobacion': f"http://sistema.empresa.com/aprobar-final/{solicitud['id']}",
            'fecha_limite': solicitud['fecha_limite'].strftime('%d/%m/%Y')
        }
        
        # Enviar a cada aprobador final
        resultados = []
        for aprobador in aprobadores:
            datos['usuario_nombre'] = aprobador.nombre
            asunto = template['subject'].format(**datos)
            contenido = template['template'].format(**datos)
            
            resultado = self.servicio_email.enviar_email(
                aprobador.email,
                aprobador.nombre,
                asunto,
                contenido
            )
            resultados.append(resultado)
        
        if all(resultados):
            logger.info(f"✅ Correos de aprobación final enviados para solicitud {solicitud_id}")
            return True
        else:
            logger.error(f"❌ Error enviando algunos correos para solicitud {solicitud_id}")
            return False
    
    def aprobar_final(self, solicitud_id, aprobador_id):
        """Aprueba una solicitud en fase final"""
        solicitud = self.solicitudes.get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud {solicitud_id} no encontrada")
            return False
        
        aprobador = gestor_usuarios.obtener_usuario(aprobador_id)
        if not aprobador or aprobador.rol != 'aprobador_final':
            logger.error(f"Aprobador final {aprobador_id} no válido")
            return False
        
        solicitud['estado'] = 'aprobado'
        solicitud['aprobador_final'] = aprobador
        solicitud['fecha_aprobacion_final'] = datetime.now()
        
        logger.info(f"🎉 Aprobación final completada para solicitud {solicitud_id}")
        
        # Enviar correo de notificación de finalización
        return self.enviar_notificacion_aprobacion_completa(solicitud_id)
    
    def enviar_notificacion_aprobacion_completa(self, solicitud_id):
        """Envía notificación cuando la aprobación está completa"""
        solicitud = self.solicitudes.get(solicitud_id)
        if not solicitud:
            logger.error(f"Solicitud {solicitud_id} no encontrada")
            return False
        
        # Preparar datos para la plantilla
        template = self.servicio_email.config.get_template('approval_completed')
        usuarios_involucrados = solicitud['usuarios_involucrados'] + [solicitud['solicitante']]
        
        # Agregar aprobadores a la lista de usuarios
        if solicitud['aprobador_inicial']:
            usuarios_involucrados.append(solicitud['aprobador_inicial'])
        if solicitud['aprobador_final']:
            usuarios_involucrados.append(solicitud['aprobador_final'])
        
        datos = {
            'documento_tipo': solicitud['documento_tipo'],
            'solicitud_id': solicitud['id'],
            'solicitante_nombre': solicitud['solicitante'].nombre,
            'solicitante_email': solicitud['solicitante'].email,
            'aprobador_inicial': solicitud['aprobador_inicial'].nombre,
            'aprobador_final': solicitud['aprobador_final'].nombre,
            'fecha_finalizacion': solicitud['fecha_aprobacion_final'].strftime('%d/%m/%Y %H:%M'),
            'monto': f"${solicitud['monto']:,.2f}",
            'usuarios_lista': gestor_usuarios.formatear_lista_usuarios(usuarios_involucrados)
        }
        
        # Enviar a todos los usuarios involucrados
        resultados = []
        for usuario in usuarios_involucrados:
            datos['usuario_nombre'] = usuario.nombre
            asunto = template['subject'].format(**datos)
            contenido = template['template'].format(**datos)
            
            resultado = self.servicio_email.enviar_email(
                usuario.email,
                usuario.nombre,
                asunto,
                contenido
            )
            resultados.append(resultado)
        
        if all(resultados):
            logger.info(f"✅ Notificaciones de aprobación completa enviadas para solicitud {solicitud_id}")
            return True
        else:
            logger.error(f"❌ Error enviando algunas notificaciones para solicitud {solicitud_id}")
            return False
    
    def obtener_estado_solicitud(self, solicitud_id):
        """Obtiene el estado actual de una solicitud"""
        return self.solicitudes.get(solicitud_id)
    
    def listar_solicitudes(self):
        """Lista todas las solicitudes"""
        return list(self.solicitudes.values())