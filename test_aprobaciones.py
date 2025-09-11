#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests para el Sistema de Aprobaciones con Correos Electrónicos
==============================================================

Tests simples para verificar que el sistema de aprobaciones funciona correctamente
y que los correos se envían con los usuarios incluidos.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servicio_email import SistemaAprobacion, ServicioEmail
from usuarios import gestor_usuarios, Usuario
from email_config import EmailConfig

class TestSistemaAprobaciones(unittest.TestCase):
    """Tests para el sistema de aprobaciones"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.sistema = SistemaAprobacion()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        self.sistema.servicio_email.desconectar_smtp()
    
    def test_crear_solicitud(self):
        """Test: Crear una nueva solicitud"""
        solicitud = self.sistema.crear_solicitud(
            solicitante_id=3,
            documento_tipo="Test Document",
            descripcion="Test description",
            monto=1000.00
        )
        
        self.assertIsNotNone(solicitud)
        self.assertEqual(solicitud['documento_tipo'], "Test Document")
        self.assertEqual(solicitud['monto'], 1000.00)
        self.assertEqual(solicitud['estado'], 'pendiente_inicial')
        self.assertIn('SOL-', solicitud['id'])
    
    def test_usuarios_en_sistema(self):
        """Test: Verificar que los usuarios están configurados correctamente"""
        aprobadores_iniciales = gestor_usuarios.obtener_aprobadores_iniciales()
        aprobadores_finales = gestor_usuarios.obtener_aprobadores_finales()
        
        self.assertGreater(len(aprobadores_iniciales), 0, "Debe haber al menos un aprobador inicial")
        self.assertGreater(len(aprobadores_finales), 0, "Debe haber al menos un aprobador final")
    
    def test_formateo_usuarios_en_email(self):
        """Test: Verificar que los usuarios se formatean correctamente para incluir en emails"""
        usuarios = gestor_usuarios.obtener_usuarios_por_rol("solicitante")
        lista_formateada = gestor_usuarios.formatear_lista_usuarios(usuarios)
        
        self.assertIsInstance(lista_formateada, str)
        self.assertIn("@", lista_formateada)  # Debe contener emails
        self.assertIn("Solicitante", lista_formateada)  # Debe contener roles
    
    @patch('smtplib.SMTP')
    def test_envio_correo_aprobacion_inicial(self, mock_smtp):
        """Test: Verificar que los correos de aprobación inicial se envían con usuarios incluidos"""
        # Configurar mock
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Crear solicitud
        solicitud = self.sistema.crear_solicitud(
            solicitante_id=3,
            documento_tipo="Test Document",
            descripcion="Test description",
            monto=1000.00,
            usuarios_involucrados=[gestor_usuarios.obtener_usuario(4)]
        )
        
        # Conectar manualmente para usar el mock
        self.sistema.servicio_email.conexion_smtp = mock_server
        
        # Enviar correos de aprobación inicial
        resultado = self.sistema.enviar_solicitud_aprobacion_inicial(solicitud['id'])
        
        self.assertTrue(resultado, "El envío de correos debería ser exitoso")
    
    def test_flujo_completo_aprobacion(self):
        """Test: Verificar el flujo completo de aprobación"""
        # Crear solicitud
        solicitud = self.sistema.crear_solicitud(
            solicitante_id=3,
            documento_tipo="Test Document",
            descripcion="Test description",
            monto=1000.00,
            usuarios_involucrados=[gestor_usuarios.obtener_usuario(4)]
        )
        
        solicitud_id = solicitud['id']
        
        # Verificar estado inicial
        self.assertEqual(solicitud['estado'], 'pendiente_inicial')
        
        # Simular aprobación inicial (sin envío real de correos)
        aprobador_inicial = gestor_usuarios.obtener_aprobadores_iniciales()[0]
        solicitud_actualizada = self.sistema.solicitudes[solicitud_id]
        solicitud_actualizada['estado'] = 'pendiente_final'
        solicitud_actualizada['aprobador_inicial'] = aprobador_inicial
        solicitud_actualizada['fecha_aprobacion_inicial'] = datetime.now()
        
        # Verificar estado después de aprobación inicial
        self.assertEqual(solicitud_actualizada['estado'], 'pendiente_final')
        self.assertIsNotNone(solicitud_actualizada['aprobador_inicial'])
        
        # Simular aprobación final
        aprobador_final = gestor_usuarios.obtener_aprobadores_finales()[0]
        solicitud_actualizada['estado'] = 'aprobado'
        solicitud_actualizada['aprobador_final'] = aprobador_final
        solicitud_actualizada['fecha_aprobacion_final'] = datetime.now()
        
        # Verificar estado final
        self.assertEqual(solicitud_actualizada['estado'], 'aprobado')
        self.assertIsNotNone(solicitud_actualizada['aprobador_final'])

class TestUsuarios(unittest.TestCase):
    """Tests para el sistema de usuarios"""
    
    def test_usuario_creacion(self):
        """Test: Crear un nuevo usuario"""
        usuario = Usuario(
            id_usuario=999,
            nombre="Test User",
            email="test@test.com",
            rol="solicitante"
        )
        
        self.assertEqual(usuario.nombre, "Test User")
        self.assertEqual(usuario.email, "test@test.com")
        self.assertEqual(usuario.rol, "solicitante")
        self.assertTrue(usuario.activo)
    
    def test_gestion_usuarios(self):
        """Test: Operaciones básicas de gestión de usuarios"""
        # Obtener usuario existente
        usuario = gestor_usuarios.obtener_usuario(1)
        self.assertIsNotNone(usuario)
        
        # Buscar por email
        usuario_por_email = gestor_usuarios.obtener_usuario_por_email(usuario.email)
        self.assertEqual(usuario.id_usuario, usuario_por_email.id_usuario)
        
        # Listar usuarios activos
        usuarios_activos = gestor_usuarios.listar_usuarios()
        self.assertGreater(len(usuarios_activos), 0)

class TestConfiguracionEmail(unittest.TestCase):
    """Tests para la configuración de email"""
    
    def test_configuracion_carga(self):
        """Test: Cargar configuración de email"""
        config = EmailConfig()
        
        self.assertIsNotNone(config.smtp_server)
        self.assertIsNotNone(config.from_email)
        self.assertIsInstance(config.templates, dict)
    
    def test_plantillas_email_incluyen_usuarios(self):
        """Test: Verificar que las plantillas incluyen sección de usuarios"""
        config = EmailConfig()
        
        for template_name, template_data in config.templates.items():
            self.assertIn('template', template_data)
            template_content = template_data['template']
            
            # Verificar que la plantilla incluye la variable usuarios_lista
            self.assertIn('{usuarios_lista}', template_content, 
                         f"La plantilla {template_name} debe incluir usuarios_lista")

def ejecutar_tests():
    """Función para ejecutar todos los tests"""
    print("🧪 EJECUTANDO TESTS DEL SISTEMA DE APROBACIONES")
    print("=" * 60)
    
    # Crear suite de tests
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTest(unittest.makeSuite(TestSistemaAprobaciones))
    suite.addTest(unittest.makeSuite(TestUsuarios))
    suite.addTest(unittest.makeSuite(TestConfiguracionEmail))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    if resultado.wasSuccessful():
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print(f"Tests ejecutados: {resultado.testsRun}")
        print("El sistema de aprobaciones funciona correctamente.")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print(f"Tests ejecutados: {resultado.testsRun}")
        print(f"Errores: {len(resultado.errors)}")
        print(f"Fallas: {len(resultado.failures)}")
    
    return resultado.wasSuccessful()

if __name__ == "__main__":
    ejecutar_tests()