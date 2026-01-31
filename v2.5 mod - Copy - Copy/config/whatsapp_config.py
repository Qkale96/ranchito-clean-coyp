"""
Archivo de configuración para el Monitor de WhatsApp
Guardar como: config/whatsapp_config.py

VERSION CORREGIDA - Configuración mejorada
"""

# ============================================
# CONFIGURACIÓN DE CHATS A MONITOREAR
# ============================================
# IMPORTANTE: Los nombres deben ser EXACTOS como aparecen en WhatsApp Web
# Incluir mayúsculas, espacios y emojis tal cual aparecen

CHATS_MONITOREADOS = [
    "YONKEROS Y YARDEROS 646",  # Chat 1
    "Yonkeros y yarderos",       # Chat 2
    "Prueba partes"              # Chat de prueba
]

# ============================================
# TU NOMBRE EN WHATSAPP
# ============================================
# Como aparece en tu perfil de WhatsApp (para enviarte notificaciones)
# CAMBIA ESTO por tu nombre real:

MI_NOMBRE_WHATSAPP = "Paul Huerta"

# ============================================
# INTERVALO DE REVISIÓN
# ============================================
# Tiempo en segundos entre cada revisión de mensajes

INTERVALO_MONITOREO = 15  # Revisar cada 15 segundos

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================
# Ruta relativa desde la raíz del proyecto

RUTA_BASE_DATOS = "data/autopartes_inventario.db"

# ============================================
# MARCAS ADICIONALES DE AUTOS
# ============================================
# Agregar más marcas si es necesario (se suman a las predefinidas)

MARCAS_ADICIONALES = [
    'geo', 'plymouth', 'amg', 'brabus', 'shelby',
    'ram', 'rivian', 'lucid', 'polestar', 'genesis'
]

# ============================================
# PALABRAS CLAVE QUE INDICAN BÚSQUEDA
# ============================================
# Si el mensaje contiene alguna de estas palabras + marca de auto,
# se considera una búsqueda de partes

PALABRAS_CLAVE_BUSQUEDA = [
    # Búsqueda directa
    'busco', 'necesito', 'requiero', 'ocupo', 'quiero',
    
    # Preguntas
    'tiene', 'tienes', 'hay', 'tienen', 'habrá',
    
    # Venta/Compra
    'vende', 'vendes', 'venden', 'compro', 'comprar',
    
    # Precio/Disponibilidad
    'precio', 'cuanto', 'cuesta', 'vale', 'costo',
    'disponible', 'stock', 'inventario', 'existencia',
    
    # Partes
    'pieza', 'parte', 'refaccion', 'refacción', 'repuesto',
    'componente', 'accesorio',
    
    # Interés
    'interesa', 'cotiza', 'cotizar', 'cotizacion', 'cotización',
    'informacion', 'información', 'info'
]

# ============================================
# NOMBRES COMUNES DE PARTES
# ============================================
# Partes que se buscan frecuentemente

PARTES_COMUNES = [
    # Motor
    'motor', 'cabeza', 'bloque', 'piston', 'pistón', 'biela',
    'cigueñal', 'arbol de levas', 'árbol de levas', 'cadena de tiempo',
    
    # Transmisión
    'transmision', 'transmisión', 'caja', 'clutch', 'embrague',
    'diferencial', 'cardán', 'cardan', 'semieje', 'flecha',
    
    # Suspensión
    'suspension', 'suspensión', 'amortiguador', 'muelle', 'resorte',
    'brazo', 'rotula', 'rótula', 'terminal', 'barra estabilizadora',
    
    # Frenos
    'freno', 'disco', 'tambor', 'pastilla', 'balata',
    'caliper', 'cilindro maestro', 'booster',
    
    # Dirección
    'direccion', 'dirección', 'cremallera', 'caja de direccion',
    'caja de dirección', 'bomba de direccion', 'bomba de dirección',
    'volante', 'columna',
    
    # Eléctrico
    'alternador', 'marcha', 'motor de arranque', 'bateria', 'batería',
    'foco', 'faro', 'cuarto', 'calavera', 'switch', 'sensor',
    'modulo', 'módulo', 'computadora', 'bcm', 'ecm', 'relay',
    
    # Refrigeración
    'radiador', 'ventilador', 'electroventilador', 'termostato',
    'bomba de agua', 'manguera', 'deposito', 'depósito',
    
    # Aire Acondicionado
    'compresor', 'condensador', 'evaporador', 'expansion', 'expansión',
    
    # Carrocería
    'cofre', 'capo', 'capó', 'salpicadera', 'defensa', 'fascia',
    'parachoques', 'puerta', 'aleron', 'alerón', 'toldo',
    'guardafango', 'cuarto', 'parabrisas', 'medallón', 'medallon',
    
    # Cristales
    'parabrisas', 'vidrio', 'cristal', 'ventana',
    
    # Espejos
    'espejo', 'retrovisor',
    
    # Interior
    'asiento', 'butaca', 'tablero', 'consola', 'tapiz',
    'vestidura', 'volante', 'aire acondicionado', 'radio',
    'estereo', 'estéreo', 'bocina', 'parlante',
    
    # Escape
    'escape', 'multiple', 'múltiple', 'catalizador', 'convertidor',
    'silenciador', 'mofle', 'resonador'
]

# ============================================
# CONFIGURACIÓN DE NOTIFICACIONES
# ============================================

# Máximo de partes a mostrar en la notificación
MAX_PARTES_NOTIFICACION = 10

# Enviar notificación incluso si no hay partes disponibles
NOTIFICAR_SIN_PARTES = False

# ============================================
# CONFIGURACIÓN DE SELENIUM
# ============================================

# Modo headless (sin ventana del navegador visible)
# True = no se ve el navegador, False = se ve el navegador
HEADLESS_MODE = False

# Tiempo máximo de espera para elementos (segundos)
TIMEOUT_SELENIUM = 60

# ============================================
# CONFIGURACIÓN DE LOGGING
# ============================================

# Mostrar mensajes de debug en consola
MOSTRAR_MENSAJES_DEBUG = True

# Guardar log en archivo
GUARDAR_LOG_ARCHIVO = True

# Ruta del archivo de log
RUTA_LOG = "logs/whatsapp_monitor.log"

# ============================================
# CONFIGURACIÓN AVANZADA
# ============================================

# Número máximo de mensajes a revisar por ciclo
MAX_MENSAJES_POR_CICLO = 30

# Tiempo de espera después de abrir un chat (segundos)
TIEMPO_ESPERA_CHAT = 2

# Tiempo de espera después de hacer scroll (segundos)
TIEMPO_ESPERA_SCROLL = 1.5
