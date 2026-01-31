"""
Script de verificación - Detecta problemas antes de ejecutar el monitor
Ejecuta: python verificar_instalacion.py
"""

import os
import sys

def verificar():
    print("="*70)
    print("🔍 VERIFICACIÓN DE INSTALACIÓN - MONITOR DE WHATSAPP")
    print("="*70)
    print()
    
    problemas = []
    advertencias = []
    
    # 1. Verificar estructura de carpetas
    print("📁 1. Verificando estructura de carpetas...")
    carpetas_necesarias = ['monitor', 'config', 'data']
    for carpeta in carpetas_necesarias:
        if os.path.exists(carpeta):
            print(f"   ✓ Carpeta '{carpeta}' existe")
        else:
            print(f"   ❌ Carpeta '{carpeta}' NO existe")
            problemas.append(f"Falta la carpeta '{carpeta}'")
    print()
    
    # 2. Verificar archivos necesarios
    print("📄 2. Verificando archivos necesarios...")
    archivos = {
        'monitor/whatsapp_monitor.py': 'Monitor principal',
        'monitor/__init__.py': 'Inicializador de monitor',
        'config/whatsapp_config.py': 'Configuración',
        'run_monitor.py': 'Script de ejecución',
        'data/autopartes_inventario.db': 'Base de datos'
    }
    
    for archivo, descripcion in archivos.items():
        if os.path.exists(archivo):
            print(f"   ✓ {descripcion}: {archivo}")
        else:
            if archivo == 'data/autopartes_inventario.db':
                print(f"   ⚠️  {descripcion}: {archivo} (se creará automáticamente)")
                advertencias.append(f"Base de datos no existe (no crítico)")
            elif archivo.endswith('__init__.py'):
                print(f"   ⚠️  {descripcion}: {archivo} (se creará)")
                advertencias.append(f"Falta {archivo} (no crítico)")
            else:
                print(f"   ❌ {descripcion}: {archivo} NO EXISTE")
                problemas.append(f"Falta el archivo '{archivo}'")
    print()
    
    # 3. Verificar Python y versión
    print("🐍 3. Verificando Python...")
    print(f"   ✓ Versión de Python: {sys.version.split()[0]}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✓ Versión compatible (3.7+)")
    else:
        print(f"   ❌ Versión no compatible (necesitas 3.7+)")
        problemas.append("Python debe ser versión 3.7 o superior")
    print()
    
    # 4. Verificar dependencias
    print("📦 4. Verificando dependencias de Python...")
    dependencias = {
        'selenium': 'Selenium',
        'webdriver_manager': 'WebDriver Manager'
    }
    
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"   ✓ {nombre} instalado")
        except ImportError:
            print(f"   ❌ {nombre} NO instalado")
            problemas.append(f"Falta instalar {nombre}: pip install {modulo}")
    print()
    
    # 5. Verificar Chrome
    print("🌐 5. Verificando navegador Chrome...")
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/local/bin/chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    chrome_encontrado = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✓ Chrome encontrado: {path}")
            chrome_encontrado = True
            break
    
    if not chrome_encontrado:
        print(f"   ⚠️  Chrome no detectado en rutas comunes")
        advertencias.append("Chrome no detectado (puede estar en otra ubicación)")
    print()
    
    # 6. Probar imports
    print("🔧 6. Probando imports del código...")
    
    # Agregar carpetas al path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'monitor'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
    
    try:
        import whatsapp_config
        print(f"   ✓ whatsapp_config.py importado correctamente")
        print(f"      - Chats: {len(whatsapp_config.CHATS_MONITOREADOS)}")
        print(f"      - Tu nombre: {whatsapp_config.MI_NOMBRE_WHATSAPP}")
    except Exception as e:
        print(f"   ❌ Error importando whatsapp_config.py: {e}")
        problemas.append(f"Error en whatsapp_config.py: {e}")
    
    try:
        from whatsapp_monitor import WhatsAppInventoryMonitor
        print(f"   ✓ whatsapp_monitor.py importado correctamente")
    except Exception as e:
        print(f"   ❌ Error importando whatsapp_monitor.py: {e}")
        problemas.append(f"Error en whatsapp_monitor.py: {e}")
    print()
    
    # Resumen
    print("="*70)
    print("📊 RESUMEN")
    print("="*70)
    
    if not problemas and not advertencias:
        print("\n✅ TODO ESTÁ CORRECTO")
        print("\nPuedes ejecutar el monitor con:")
        print("   python run_monitor.py")
        
    elif problemas:
        print(f"\n❌ SE ENCONTRARON {len(problemas)} PROBLEMA(S) CRÍTICO(S):")
        for i, problema in enumerate(problemas, 1):
            print(f"   {i}. {problema}")
        
        if advertencias:
            print(f"\n⚠️  Y {len(advertencias)} ADVERTENCIA(S):")
            for i, advertencia in enumerate(advertencias, 1):
                print(f"   {i}. {advertencia}")
        
        print("\n🔧 SOLUCIONES:")
        print("\n1. Instalar dependencias faltantes:")
        print("   pip install selenium webdriver-manager")
        
        print("\n2. Crear archivos __init__.py vacíos:")
        print("   - En la carpeta 'monitor'")
        print("   - En la carpeta 'config'")
        
        print("\n3. Verificar que todos los archivos estén en su lugar")
        
    else:
        print(f"\n⚠️  SE ENCONTRARON {len(advertencias)} ADVERTENCIA(S):")
        for i, advertencia in enumerate(advertencias, 1):
            print(f"   {i}. {advertencia}")
        
        print("\n💡 Las advertencias no son críticas, pero revísalas")
        print("\nPuedes intentar ejecutar el monitor con:")
        print("   python run_monitor.py")
    
    print("\n" + "="*70)
    input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    try:
        verificar()
    except Exception as e:
        print(f"\n❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para cerrar...")
