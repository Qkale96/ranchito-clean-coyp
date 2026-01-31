# Estructura del Proyecto

## Descripción General

Este documento describe la estructura del proyecto Sistema de Inventario de Autopartes.

## Estructura de Directorios

```
v2/
├── src/                          # Código fuente principal
│   ├── __init__.py              # Inicialización del paquete
│   └── inventario_autopartes.py # Aplicación principal
│
├── data/                         # Datos de la aplicación
│   └── autopartes_inventario.db # Base de datos SQLite
│
├── config/                       # Archivos de configuración
│   └── config.py                # Configuración centralizada
│
├── tests/                        # Pruebas unitarias
│   ├── __init__.py
│   └── test_database.py         # Tests de base de datos
│
├── docs/                         # Documentación
│   ├── ESTRUCTURA.md            # Este archivo
│   └── (otros documentos)
│
├── requirements.txt              # Dependencias del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Documentación principal
```

## Descripción de Carpetas

### src/
Contiene el código fuente principal de la aplicación. El archivo `inventario_autopartes.py` es el punto de entrada de la aplicación.

### data/
Almacena los archivos de datos, principalmente la base de datos SQLite. Esta carpeta se crea automáticamente si no existe.

### config/
Contiene archivos de configuración. El archivo `config.py` centraliza todas las constantes y configuraciones del sistema.

### tests/
Contiene las pruebas unitarias y de integración del proyecto. Actualmente incluye una estructura básica para tests de base de datos.

### docs/
Documentación adicional del proyecto, incluyendo guías, diagramas y otros documentos de referencia.

## Flujo de Datos

1. **Interfaz de Usuario (Tkinter)**: El usuario interactúa con la aplicación a través de la interfaz gráfica.

2. **Lógica de Negocio**: La clase `AutoPartsInventory` maneja toda la lógica de la aplicación.

3. **Base de Datos (SQLite)**: Los datos se almacenan en una base de datos SQLite local.

4. **Archivos**: Las imágenes se almacenan como base64 en la base de datos.

## Convenciones de Código

- **Nombres de clases**: PascalCase (ej: `AutoPartsInventory`)
- **Nombres de funciones**: snake_case (ej: `add_part_window`)
- **Nombres de variables**: snake_case (ej: `stock_number`)
- **Constantes**: UPPER_SNAKE_CASE (ej: `DATABASE_PATH`)

## Próximos Pasos

- [ ] Separar la lógica de negocio de la interfaz
- [ ] Crear módulos separados para diferentes funcionalidades
- [ ] Implementar un sistema de logging
- [ ] Agregar más tests unitarios
- [ ] Crear documentación de API

