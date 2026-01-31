"""
Configuración del Sistema de Inventario de Autopartes
"""

# Configuración de la base de datos
DATABASE_PATH = 'data/autopartes_inventario.db'

# Configuración de la aplicación
APP_TITLE = "Sistema de Inventario de Autopartes"
APP_SIZE = "1400x800"
APP_BG_COLOR = '#f0f0f0'

# Categorías de piezas
CATEGORIES = [
    'Motor',
    'Suspension',
    'Transmision',
    'Electrico',
    'Carroceria',
    'Interior',
    'Frenos',
    'Direccion',
    'Escape',
    'Refrigeracion',
    'Otro'
]

# Condiciones de piezas
CONDITIONS = [
    'Nueva',
    'Usada - Excelente',
    'Usada - Buena',
    'Usada - Regular',
    'Refaccionada'
]

# Estantes disponibles
SHELVES = ['A', 'B', 'C', 'D']

# Niveles disponibles
LEVELS = [1, 2, 3]

# Formato de fecha
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Configuración de QR
QR_VERSION = 1
QR_BOX_SIZE = 10
QR_BORDER = 2

# Configuración de imágenes
MAX_IMAGE_SIZE = (180, 180)
FULL_IMAGE_ZOOM_MAX = 5.0
FULL_IMAGE_ZOOM_MIN = 0.1

