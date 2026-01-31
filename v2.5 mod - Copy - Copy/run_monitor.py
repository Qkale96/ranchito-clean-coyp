#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar el monitor de WhatsApp
Ejecuta: python run_monitor.py
"""

import sys
import os

# Agregar directorios al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'monitor'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from whatsapp_monitor import WhatsAppInventoryMonitor
import whatsapp_config as config

def main():
    print("="*60)
    print("🚀 INICIANDO MONITOR DE WHATSAPP")
    print("="*60)
    print(f"📂 Base de datos: {config.RUTA_BASE_DATOS}")
    print(f"💬 Chats a monitorear:")
    for i, chat in enumerate(config.CHATS_MONITOREADOS, 1):
        print(f"   {i}. {chat}")
    print(f"👤 Enviar notificaciones a: {config.MI_NOMBRE_WHATSAPP}")
    print(f"⏱️  Intervalo de revisión: {config.INTERVALO_MONITOREO} segundos")
    print("="*60 + "\n")
    
    # Crear monitor
    monitor = WhatsAppInventoryMonitor(db_path=config.RUTA_BASE_DATOS)
    monitor.chats_monitoreados = config.CHATS_MONITOREADOS
    monitor.mi_nombre = config.MI_NOMBRE_WHATSAPP
    
    # Agregar marcas adicionales si existen
    if hasattr(config, 'MARCAS_ADICIONALES'):
        monitor.marcas_autos.extend(config.MARCAS_ADICIONALES)
        print(f"✅ Marcas adicionales agregadas: {len(config.MARCAS_ADICIONALES)}")
    
    # Iniciar monitoreo
    try:
        monitor.iniciar_monitoreo(intervalo=config.INTERVALO_MONITOREO)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("💡 Presiona Enter para cerrar...")
        input()

if __name__ == "__main__":
    main()