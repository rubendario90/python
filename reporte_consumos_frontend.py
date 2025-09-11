#!/usr/bin/env python3
"""
Reporte de Consumo - Frontend de Reportes
Genera reportes de consumo de las calculadoras
"""

import sys
import os
from consumption_reporter import ConsumptionReporter


def main():
    """Main function for consumption report generation."""
    
    print("📊 FRONTEND DE REPORTES DE CONSUMO")
    print("=" * 40)
    
    # Initialize reporter
    reporter = ConsumptionReporter()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "report":
            # Generate full report
            print(reporter.generate_report())
            
        elif command == "stats":
            # Show summary statistics
            stats = reporter.get_summary_stats()
            print("📈 ESTADÍSTICAS RESUMIDAS")
            print("-" * 25)
            print(f"Total de operaciones: {stats['total_operations']}")
            print(f"Total de errores: {stats['total_errors']}")
            print(f"Total de sesiones: {stats['total_sessions']}")
            print(f"Tasa de éxito: {stats['success_rate']:.1f}%")
            if stats['most_used_operation']:
                print(f"Operación más usada: {stats['most_used_operation']}")
                
        elif command == "clear":
            # Clear consumption data
            if os.path.exists(reporter.data_file):
                os.remove(reporter.data_file)
                print("✅ Datos de consumo limpiados.")
            else:
                print("ℹ️ No hay datos de consumo para limpiar.")
                
        elif command == "help":
            show_help()
            
        else:
            print(f"❌ Comando desconocido: {command}")
            show_help()
            sys.exit(1)
    else:
        # Interactive menu
        while True:
            print("\n🎯 MENÚ DE REPORTES")
            print("1. Ver reporte completo")
            print("2. Ver estadísticas resumidas")
            print("3. Limpiar datos de consumo")
            print("4. Salir")
            
            opcion = input("\nElige una opción: ").strip()
            
            if opcion == "1":
                print("\n" + reporter.generate_report())
                
            elif opcion == "2":
                stats = reporter.get_summary_stats()
                print("\n📈 ESTADÍSTICAS RESUMIDAS")
                print("-" * 25)
                print(f"Total de operaciones: {stats['total_operations']}")
                print(f"Total de errores: {stats['total_errors']}")
                print(f"Total de sesiones: {stats['total_sessions']}")
                print(f"Tasa de éxito: {stats['success_rate']:.1f}%")
                if stats['most_used_operation']:
                    print(f"Operación más usada: {stats['most_used_operation']}")
                    
            elif opcion == "3":
                confirmacion = input("¿Estás seguro de que quieres limpiar todos los datos? (s/N): ")
                if confirmacion.lower() == 's':
                    if os.path.exists(reporter.data_file):
                        os.remove(reporter.data_file)
                        print("✅ Datos de consumo limpiados.")
                        # Reload reporter with fresh data
                        reporter = ConsumptionReporter()
                    else:
                        print("ℹ️ No hay datos de consumo para limpiar.")
                else:
                    print("❌ Operación cancelada.")
                    
            elif opcion == "4":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida.")


def show_help():
    """Show help information."""
    print("\n📚 AYUDA - Reporte de Consumos Frontend")
    print("=" * 45)
    print("Uso: python reporte_consumos_frontend.py [comando]")
    print("\nComandos disponibles:")
    print("  report    - Generar reporte completo de consumo")
    print("  stats     - Mostrar estadísticas resumidas") 
    print("  clear     - Limpiar todos los datos de consumo")
    print("  help      - Mostrar esta ayuda")
    print("\nSin argumentos: Ejecutar menú interactivo")
    print("\nEjemplos:")
    print("  python reporte_consumos_frontend.py report")
    print("  python reporte_consumos_frontend.py stats")


if __name__ == "__main__":
    main()