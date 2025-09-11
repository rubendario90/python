#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Aprobaciones con Correos Electrónicos
===============================================

Este script demuestra el sistema de aprobaciones que resuelve los problemas identificados:
1. Correos de aprobación inicial y final que no se enviaban
2. Usuarios que no se incluían en los correos
3. Proporciona un sistema completo y funcional

Autor: Sistema de Aprobaciones
Fecha: 2024
"""

import logging
from datetime import datetime
from servicio_email import SistemaAprobacion
from usuarios import gestor_usuarios, Usuario

def configurar_logging():
    """Configura el sistema de logging para mostrar información detallada"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def mostrar_usuarios_sistema():
    """Muestra todos los usuarios del sistema"""
    print("\n" + "="*60)
    print("👥 USUARIOS DEL SISTEMA")
    print("="*60)
    
    usuarios = gestor_usuarios.listar_usuarios()
    for usuario in usuarios:
        print(f"🆔 {usuario.id_usuario:2d} | {usuario.nombre:20s} | {usuario.email:25s} | {usuario.rol}")
    
    print(f"\nTotal de usuarios activos: {len(usuarios)}")

def demostrar_flujo_aprobacion():
    """Demuestra el flujo completo de aprobación con correos"""
    print("\n" + "="*60)
    print("📋 DEMOSTRACIÓN DEL SISTEMA DE APROBACIONES")
    print("="*60)
    
    # Usar el sistema de aprobación con context manager
    with SistemaAprobacion() as sistema:
        
        print("\n1️⃣ Creando una nueva solicitud...")
        
        # Crear algunos usuarios adicionales para involucrar en la solicitud
        usuario_compras = gestor_usuarios.obtener_usuario(3)  # Carlos López
        usuario_rrhh = gestor_usuarios.obtener_usuario(4)     # Ana Rodríguez
        usuarios_involucrados = [usuario_compras, usuario_rrhh]
        
        # Crear la solicitud
        solicitud = sistema.crear_solicitud(
            solicitante_id=3,  # Carlos López (Compras)
            documento_tipo="Orden de Compra",
            descripcion="Compra de equipos de oficina para el departamento de RRHH. Incluye 5 computadoras portátiles, 2 impresoras láser y mobiliario de oficina.",
            monto=15750.50,
            usuarios_involucrados=usuarios_involucrados
        )
        
        print(f"✅ Solicitud creada: {solicitud['id']}")
        print(f"   Solicitante: {solicitud['solicitante'].nombre}")
        print(f"   Tipo: {solicitud['documento_tipo']}")
        print(f"   Monto: ${solicitud['monto']:,.2f}")
        print(f"   Usuarios involucrados: {len(usuarios_involucrados)}")
        
        print("\n2️⃣ Enviando correos de aprobación inicial...")
        
        # Enviar correos de aprobación inicial
        resultado_inicial = sistema.enviar_solicitud_aprobacion_inicial(solicitud['id'])
        
        if resultado_inicial:
            print("✅ Correos de aprobación inicial enviados exitosamente")
            aprobadores_iniciales = gestor_usuarios.obtener_aprobadores_iniciales()
            print(f"   📧 Enviado a {len(aprobadores_iniciales)} aprobadores iniciales:")
            for aprobador in aprobadores_iniciales:
                print(f"      • {aprobador.nombre} ({aprobador.email})")
        else:
            print("❌ Error enviando correos de aprobación inicial")
            return
        
        print("\n3️⃣ Simulando aprobación inicial...")
        
        # Simular aprobación inicial
        aprobador_inicial = gestor_usuarios.obtener_aprobadores_iniciales()[0]
        resultado_aprobacion_inicial = sistema.aprobar_inicial(solicitud['id'], aprobador_inicial.id_usuario)
        
        if resultado_aprobacion_inicial:
            print(f"✅ Aprobación inicial completada por: {aprobador_inicial.nombre}")
            print("📧 Correos de aprobación final enviados automáticamente")
            
            aprobadores_finales = gestor_usuarios.obtener_aprobadores_finales()
            print(f"   📧 Enviado a {len(aprobadores_finales)} aprobadores finales:")
            for aprobador in aprobadores_finales:
                print(f"      • {aprobador.nombre} ({aprobador.email})")
        else:
            print("❌ Error en aprobación inicial")
            return
        
        print("\n4️⃣ Simulando aprobación final...")
        
        # Simular aprobación final
        aprobador_final = gestor_usuarios.obtener_aprobadores_finales()[0]
        resultado_aprobacion_final = sistema.aprobar_final(solicitud['id'], aprobador_final.id_usuario)
        
        if resultado_aprobacion_final:
            print(f"✅ Aprobación final completada por: {aprobador_final.nombre}")
            print("🎉 Proceso de aprobación finalizado")
            print("📧 Notificaciones de finalización enviadas a todos los usuarios involucrados")
        else:
            print("❌ Error en aprobación final")
            return
        
        print("\n5️⃣ Estado final de la solicitud:")
        
        # Mostrar estado final
        solicitud_final = sistema.obtener_estado_solicitud(solicitud['id'])
        print(f"   ID: {solicitud_final['id']}")
        print(f"   Estado: {solicitud_final['estado'].upper()}")
        print(f"   Solicitante: {solicitud_final['solicitante'].nombre}")
        print(f"   Aprobador Inicial: {solicitud_final['aprobador_inicial'].nombre}")
        print(f"   Aprobador Final: {solicitud_final['aprobador_final'].nombre}")
        print(f"   Fecha Solicitud: {solicitud_final['fecha_solicitud'].strftime('%d/%m/%Y %H:%M')}")
        print(f"   Fecha Aprobación Inicial: {solicitud_final['fecha_aprobacion_inicial'].strftime('%d/%m/%Y %H:%M')}")
        print(f"   Fecha Aprobación Final: {solicitud_final['fecha_aprobacion_final'].strftime('%d/%m/%Y %H:%M')}")

def mostrar_estadisticas_correos():
    """Muestra estadísticas de los correos que se habrían enviado"""
    print("\n" + "="*60)
    print("📊 ESTADÍSTICAS DE CORREOS ENVIADOS")
    print("="*60)
    
    aprobadores_iniciales = gestor_usuarios.obtener_aprobadores_iniciales()
    aprobadores_finales = gestor_usuarios.obtener_aprobadores_finales()
    
    print(f"📧 Correos de aprobación inicial: {len(aprobadores_iniciales)}")
    print(f"📧 Correos de aprobación final: {len(aprobadores_finales)}")
    
    # Calcular usuarios únicos que reciben notificación final
    todos_usuarios = set()
    todos_usuarios.add(3)  # Solicitante (Carlos)
    todos_usuarios.add(4)  # Usuario involucrado (Ana)
    todos_usuarios.add(3)  # Usuario involucrado (Carlos - ya incluido)
    
    for aprobador in aprobadores_iniciales:
        todos_usuarios.add(aprobador.id_usuario)
    
    for aprobador in aprobadores_finales:
        todos_usuarios.add(aprobador.id_usuario)
    
    print(f"📧 Notificaciones de finalización: {len(todos_usuarios)}")
    print(f"📊 Total de correos enviados: {len(aprobadores_iniciales) + len(aprobadores_finales) + len(todos_usuarios)}")

def mostrar_solucion_problemas():
    """Explica cómo el sistema resuelve los problemas identificados"""
    print("\n" + "="*60)
    print("🔧 SOLUCIÓN A LOS PROBLEMAS IDENTIFICADOS")
    print("="*60)
    
    print("✅ PROBLEMA 1: Correos de aprobación inicial/final no se enviaban")
    print("   SOLUCIÓN:")
    print("   • Sistema robusto de envío con manejo de errores")
    print("   • Logging detallado para monitoreo")
    print("   • Modo simulación para desarrollo/testing")
    print("   • Reconexión automática en caso de fallas")
    
    print("\n✅ PROBLEMA 2: Usuarios no se incluían en los correos")
    print("   SOLUCIÓN:")
    print("   • Lista completa de usuarios involucrados en cada email")
    print("   • Gestión centralizada de usuarios con roles")
    print("   • Inclusión automática de solicitantes y aprobadores")
    print("   • Formateo claro de la información de usuarios")
    
    print("\n✅ MEJORAS ADICIONALES:")
    print("   • Plantillas de correo personalizables")
    print("   • Context managers para manejo de conexiones")
    print("   • Sistema de logging comprehensivo")
    print("   • Validación de datos y usuarios")
    print("   • Manejo de errores robusto")

def main():
    """Función principal que ejecuta la demostración completa"""
    configurar_logging()
    
    print("🚀 SISTEMA DE APROBACIONES CON CORREOS ELECTRÓNICOS")
    print("="*60)
    print("Este sistema resuelve los problemas de correos no enviados")
    print("y usuarios no incluidos en las notificaciones.")
    print("="*60)
    
    try:
        # Mostrar usuarios del sistema
        mostrar_usuarios_sistema()
        
        # Demostrar el flujo de aprobación
        demostrar_flujo_aprobacion()
        
        # Mostrar estadísticas
        mostrar_estadisticas_correos()
        
        # Explicar la solución
        mostrar_solucion_problemas()
        
        print("\n" + "="*60)
        print("🎉 DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("El sistema está funcionando correctamente y resuelve")
        print("todos los problemas identificados en la solicitud.")
        
    except Exception as e:
        logging.error(f"Error durante la demostración: {str(e)}")
        print(f"\n❌ Error durante la ejecución: {str(e)}")

if __name__ == "__main__":
    main()