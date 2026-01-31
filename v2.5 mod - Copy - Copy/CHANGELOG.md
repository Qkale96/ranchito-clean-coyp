# Changelog - Sistema de Inventario de Autopartes

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [2.0.0] - 2025-11-13

### ✨ Mejoras y Correcciones

#### Correcciones de Errores
- **Corregido**: Manejo de fechas nulas en la visualización de detalles de piezas
- **Corregido**: Eliminados imports no utilizados (`json`, `os` - movido a donde se necesita)
- **Corregido**: Validación mejorada de campos numéricos (precio)
- **Corregido**: Manejo de valores None en campos opcionales de la base de datos
- **Mejorado**: Ruta de base de datos ahora usa rutas absolutas para mayor robustez

#### Estructura del Proyecto
- **Agregado**: Estructura de carpetas profesional:
  - `src/` - Código fuente
  - `data/` - Base de datos y archivos de datos
  - `config/` - Archivos de configuración
  - `tests/` - Pruebas unitarias
  - `docs/` - Documentación
- **Agregado**: `requirements.txt` con todas las dependencias
- **Agregado**: `.gitignore` para control de versiones
- **Agregado**: `README.md` con documentación completa
- **Agregado**: `INSTALACION.md` con guía paso a paso
- **Agregado**: `CHANGELOG.md` (este archivo)
- **Agregado**: `docs/ESTRUCTURA.md` con descripción de la estructura
- **Agregado**: `run.py` - Script de inicio simplificado
- **Agregado**: `config/config.py` - Configuración centralizada
- **Agregado**: Estructura básica de tests

#### Mejoras de Código
- **Mejorado**: Validación de entrada de datos más robusta
- **Mejorado**: Manejo de errores mejorado en operaciones de base de datos
- **Mejorado**: Código más mantenible con mejor organización

### 📝 Documentación
- Documentación completa en README.md
- Guía de instalación detallada
- Documentación de estructura del proyecto
- Comentarios mejorados en el código

### 🔧 Configuración
- Archivo de configuración centralizado
- Rutas de base de datos mejoradas
- Estructura preparada para futuras mejoras

---

## [1.0.0] - Versión Inicial

### Características Iniciales
- Sistema básico de inventario de autopartes
- Gestión de piezas y vehículos
- Generación de códigos QR
- Almacenamiento de imágenes
- Dashboard con estadísticas
- Búsqueda y filtrado

---

## Formato del Changelog

- **Agregado**: Para nuevas funcionalidades
- **Cambiado**: Para cambios en funcionalidades existentes
- **Deprecado**: Para funcionalidades que serán removidas
- **Removido**: Para funcionalidades removidas
- **Corregido**: Para correcciones de bugs
- **Seguridad**: Para vulnerabilidades de seguridad

