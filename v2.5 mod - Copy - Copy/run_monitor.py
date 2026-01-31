#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar el monitor de WhatsApp
Ejecuta: python run_monitor.py

VERSION CORREGIDA - Con manejo de errores mejorado
"""

import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'monitor'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

def main():
    try:
        print("="*60)
        print("🚀 INICIANDO MONITOR DE WHATSAPP")
        print("="*60)
        
        # Intentar importar la configuración
        try:
            import whatsapp_config as config
            print("✓ Configuración cargada")
        except ImportError as e:
            print(f"\n❌ ERROR: No se pudo cargar whatsapp_config.py")
            print(f"   Detalle: {e}")
            print("\n💡 SOLUCIÓN:")
            print("   1. Verifica que el archivo 'config/whatsapp_config.py' exista")
            print("   2. Verifica que la carpeta 'config' tenga un archivo __init__.py")
            input("\nPresiona Enter para cerrar...")
            return
        
        # Intentar importar el monitor
        try:
            from whatsapp_monitor import WhatsAppInventoryMonitor
            print("✓ Monitor cargado")
        except ImportError as e:
            print(f"\n❌ ERROR: No se pudo cargar whatsapp_monitor.py")
            print(f"   Detalle: {e}")
            print("\n💡 SOLUCIÓN:")
            print("   1. Verifica que el archivo 'monitor/whatsapp_monitor.py' exista")
            print("   2. Verifica que la carpeta 'monitor' tenga un archivo __init__.py")
            input("\nPresiona Enter para cerrar...")
            return
        
        # Verificar base de datos
        db_path = config.RUTA_BASE_DATOS
        if not os.path.exists(db_path):
            print(f"\n⚠️  ADVERTENCIA: Base de datos no encontrada")
            print(f"   Ruta buscada: {os.path.abspath(db_path)}")
            print("\n💡 El monitor continuará, pero no podrá buscar partes")
            respuesta = input("\n¿Deseas continuar de todas formas? (s/n): ")
            if respuesta.lower() != 's':
                return
        else:
            print(f"✓ Base de datos encontrada: {db_path}")
        
        # Mostrar configuración
        print(f"\n📂 Base de datos: {config.RUTA_BASE_DATOS}")
        print(f"💬 Chats a monitorear:")
        for i, chat in enumerate(config.CHATS_MONITOREADOS, 1):
            print(f"   {i}. {chat}")
        print(f"👤 Enviar notificaciones a: {config.MI_NOMBRE_WHATSAPP}")
        print(f"⏱️  Intervalo de revisión: {config.INTERVALO_MONITOREO} segundos")
        print("="*60 + "\n")
        
        # Crear monitor
        print("🔧 Creando monitor...")
        monitor = WhatsAppInventoryMonitor(db_path=config.RUTA_BASE_DATOS)
        monitor.chats_monitoreados = config.CHATS_MONITOREADOS
        monitor.mi_nombre = config.MI_NOMBRE_WHATSAPP
        
        # Agregar marcas adicionales si existen
        if hasattr(config, 'MARCAS_ADICIONALES'):
            monitor.marcas_autos.extend(config.MARCAS_ADICIONALES)
            print(f"✓ Marcas adicionales agregadas: {len(config.MARCAS_ADICIONALES)}")
        
        print("\n" + "="*60)
        print("✓ Monitor configurado correctamente")
        print("="*60)
        
        # Iniciar monitoreo
        monitor.iniciar_monitoreo(intervalo=config.INTERVALO_MONITOREO)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor detenido por el usuario")
        print("✓ Cerrando...")
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print("\n📋 DETALLES DEL ERROR:")
        import traceback
        traceback.print_exc()
        
        print("\n\n💡 SOLUCIONES COMUNES:")
        print("1. Verifica que todos los archivos estén en su lugar:")
        print("   - monitor/whatsapp_monitor.py")
        print("   - config/whatsapp_config.py")
        print("   - data/autopartes_inventario.db")
        print("\n2. Instala las dependencias:")
        print("   pip install selenium webdriver-manager")
        print("\n3. Verifica que Chrome esté instalado")
        
        input("\n\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    main()
