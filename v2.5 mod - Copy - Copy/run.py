#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de inicio para el Sistema de Inventario de Autopartes
Ejecuta: python run.py
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Asegurar que la carpeta data existe
os.makedirs('data', exist_ok=True)

# Importar y ejecutar la aplicación
from inventario_autopartes import AutoPartsInventory
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPartsInventory(root)
    root.mainloop()

