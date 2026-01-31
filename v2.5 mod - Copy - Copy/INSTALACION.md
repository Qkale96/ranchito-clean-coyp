# Guía de Instalación - Sistema de Inventario de Autopartes

## Requisitos del Sistema

- **Python**: Versión 3.7 o superior
- **Sistema Operativo**: Windows, Linux o macOS
- **Espacio en disco**: Mínimo 100 MB (para la aplicación y base de datos)

## Instalación Paso a Paso

### 1. Verificar Python

Abre una terminal o PowerShell y verifica que Python esté instalado:

```bash
python --version
```

Deberías ver algo como: `Python 3.9.x` o superior.

Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/)

### 2. Navegar al Directorio del Proyecto

```bash
cd "C:\Users\donal\Desktop\proyecto inventario ranchito\v2"
```

### 3. Crear Entorno Virtual (Recomendado)

Un entorno virtual aísla las dependencias del proyecto:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Cuando el entorno virtual esté activo, verás `(venv)` al inicio de la línea de comandos.

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- Pillow (para procesamiento de imágenes)
- qrcode (para generar códigos QR)

### 5. Ejecutar la Aplicación

**Opción 1: Usando el script de inicio (Recomendado)**
```bash
python run.py
```

**Opción 2: Ejecutar directamente**
```bash
python src/inventario_autopartes.py
```

## Solución de Problemas

### Error: "No module named 'tkinter'"

**Solución**: Tkinter viene con Python, pero en algunos sistemas Linux puede necesitar instalarse por separado:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### Error: "No module named 'PIL'"

**Solución**: Instala Pillow:
```bash
pip install Pillow
```

### Error: "No module named 'qrcode'"

**Solución**: Instala qrcode:
```bash
pip install qrcode[pil]
```

### La base de datos no se crea

**Solución**: Asegúrate de que la carpeta `data/` existe y tienes permisos de escritura. La aplicación la creará automáticamente si no existe.

### Error al abrir imágenes

**Solución**: Verifica que las imágenes estén en formatos soportados: JPG, JPEG, PNG, GIF, BMP

## Primera Ejecución

1. Al ejecutar la aplicación por primera vez, se creará automáticamente la base de datos en `data/autopartes_inventario.db`
2. La interfaz se abrirá con tres pestañas: Dashboard, Inventario y Vehículos
3. Comienza agregando un vehículo donador o una pieza directamente

## Actualización

Para actualizar las dependencias:

```bash
pip install --upgrade -r requirements.txt
```

## Desinstalación

1. Desactiva el entorno virtual (si lo usas):
   ```bash
   deactivate
   ```

2. Elimina la carpeta del entorno virtual:
   ```bash
   rmdir /s venv  # Windows
   rm -rf venv    # Linux/Mac
   ```

3. Opcional: Elimina la base de datos si deseas empezar de cero:
   ```bash
   del data\autopartes_inventario.db  # Windows
   rm data/autopartes_inventario.db   # Linux/Mac
   ```

## Soporte

Si encuentras problemas durante la instalación, verifica:
1. Que Python esté correctamente instalado
2. Que todas las dependencias se hayan instalado correctamente
3. Que tengas permisos de escritura en el directorio del proyecto

Para más ayuda, consulta el README.md o abre un issue en el repositorio.

