# Sistema de Inventario de Autopartes

Sistema de gestión de inventario para autopartes con interfaz gráfica desarrollado en Python usando Tkinter.

## 📋 Características

- **Gestión de Piezas**: Registro completo de autopartes con información detallada
- **Gestión de Vehículos Donadores**: Registro de vehículos de los que provienen las piezas
- **Sistema de Ubicación**: Organización por estantes y niveles (A-D, 1-3)
- **Códigos QR**: Generación de códigos QR para identificación rápida
- **Gestión de Imágenes**: Almacenamiento y visualización de múltiples fotos por pieza
- **Dashboard**: Estadísticas en tiempo real del inventario
- **Búsqueda y Filtrado**: Búsqueda avanzada por múltiples criterios
- **Base de Datos SQLite**: Almacenamiento local y confiable

## 🚀 Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. Clonar o descargar el repositorio:
```bash
cd "proyecto inventario ranchito/v2"
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

3. Activar el entorno virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Ejecutar la Aplicación

```bash
python src/inventario_autopartes.py
```

### Funcionalidades Principales

#### Dashboard
- Visualización de estadísticas generales
- Accesos rápidos a funciones principales

#### Inventario
- Ver todas las piezas registradas
- Buscar piezas por nombre, marca, modelo, año, stock number o ubicación
- Filtrar por categoría
- Agregar nuevas piezas
- Ver detalles completos de cada pieza
- Eliminar piezas
- Generar códigos QR

#### Vehículos
- Registrar vehículos donadores
- Ver piezas asociadas a cada vehículo
- Eliminar vehículos

### Agregar una Nueva Pieza

1. Ir a la pestaña "Inventario"
2. Clic en "+ Agregar Pieza"
3. Completar los campos obligatorios:
   - Nombre de la Pieza
   - Marca del Auto
   - Modelo
   - Año
4. Opcionalmente agregar:
   - Número de Parte
   - Fabricante
   - Precio
   - Fotos
   - Notas
5. Seleccionar ubicación (Estante y Nivel)
6. Clic en "Guardar Pieza"

### Categorías Disponibles

- Motor
- Suspensión
- Transmisión
- Eléctrico
- Carrocería
- Interior
- Frenos
- Dirección
- Escape
- Refrigeración
- Otro

## 📁 Estructura del Proyecto

```
v2/
├── src/                    # Código fuente
│   └── inventario_autopartes.py
├── data/                   # Base de datos
│   └── autopartes_inventario.db
├── config/                 # Archivos de configuración
├── tests/                  # Pruebas unitarias
├── docs/                   # Documentación adicional
├── requirements.txt        # Dependencias del proyecto
├── .gitignore             # Archivos a ignorar en Git
└── README.md              # Este archivo
```

## 🗄️ Base de Datos

El sistema utiliza SQLite para almacenar la información. La base de datos se crea automáticamente en la carpeta `data/` al ejecutar la aplicación por primera vez.

### Tablas

- **vehiculos**: Información de vehículos donadores
- **piezas**: Información de autopartes
- **imagenes**: Imágenes asociadas a las piezas (almacenadas en base64)

## 🛠️ Desarrollo

### Mejoras Futuras

- [ ] Exportar inventario a Excel/CSV
- [ ] Sistema de reportes
- [ ] Historial de movimientos
- [ ] Sistema de usuarios y permisos
- [ ] Backup automático de base de datos
- [ ] Búsqueda avanzada con múltiples filtros
- [ ] Edición de piezas existentes
- [ ] Impresión de etiquetas con QR

### Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 👤 Autor

Desarrollado para el proyecto de inventario de autopartes.

## 📞 Soporte

Para reportar problemas o sugerencias, por favor abre un issue en el repositorio.

---

**Versión:** 2.0  
**Última actualización:** 2025

