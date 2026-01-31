"""
Archivo de configuración para el Monitor de WhatsApp
Guardar como: config/whatsapp_config.py
"""

# CONFIGURACIÓN DE CHATS A MONITOREAR
# Nota: Los nombres deben ser EXACTOS como aparecen en WhatsApp Web
CHATS_MONITOREADOS = [
    "YONKEROS Y YARDEROS 646",  # ← CAMBIA ESTO: Reemplazar con nombre exacto del chat 1
    "Yonkeros y yarderos",       # ← CAMBIA ESTO: Reemplazar con nombre exacto del chat 2
    "Prueba partes"        # ← CAMBIA ESTO: Reemplazar con nombre exacto del chat 3
]

# TU NOMBRE EN WHATSAPP
# Como aparece en tu perfil de WhatsApp (para enviarte notificaciones)
MI_NOMBRE_WHATSAPP = "Paul Huerta"  # ← CAMBIA ESTO: Reemplazar con tu nombre

# INTERVALO DE REVISIÓN (en segundos)
INTERVALO_MONITOREO = 15  # Revisar cada 30 segundos

# CONFIGURACIÓN DE BASE DE DATOS
# Ruta relativa desde la raíz del proyecto
RUTA_BASE_DATOS = "data/autopartes_inventario.db"

# MARCAS ADICIONALES (opcional)
# Agregar más marcas si es necesario
MARCAS_ADICIONALES = [
    'pontiac', 'saturn', 'hummer', 'oldsmobile', 'mercury',
    'datsun', 'daihatsu', 'lada', 'tata', 'mahindra'
]

# PALABRAS CLAVE QUE INDICAN BÚSQUEDA DE PARTES
# Si el mensaje contiene alguna de estas palabras + marca de auto, se considera búsqueda
PALABRAS_CLAVE_BUSQUEDA = [
    'busco', 'necesito', 'tiene', 'tienes', 'hay', 'vende', 'vendes',
    'precio', 'cuanto', 'cuesta', 'disponible', 'stock', 'inventario',
    'pieza', 'parte', 'refaccion', 'repuesto'
]

# MÁXIMO DE PARTES A MOSTRAR EN NOTIFICACIÓN
MAX_PARTES_NOTIFICACION = 10

# CONFIGURACIÓN DE SELENIUM
HEADLESS_MODE = False  # True = sin interfaz gráfica, False = con navegador visible
TIMEOUT_SELENIUM = 60  # Segundos para esperar carga de elementos

# LOGGING
MOSTRAR_MENSAJES_DEBUG = True  # True = mostrar más información en consola
GUARDAR_LOG_ARCHIVO = True  # True = guardar registro en archivo
RUTA_LOG = "logs/whatsapp_monitor.log"