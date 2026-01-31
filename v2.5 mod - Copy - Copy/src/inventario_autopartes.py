"""
Sistema de Inventario de Autopartes - Aplicación Desktop
Guarda el archivo como: inventario_autopartes.py
Ejecuta con: python inventario_autopartes.py

Requisitos:
pip install pillow qrcode
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import qrcode
import io
import base64

class AutoPartsInventory:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario de Autopartes")
        self.root.geometry("1400x800")
        self.setup_theme()
        
        # Inicializar base de datos
        self.init_database()
        
        # Variables
        self.current_images = []
        self.categories = ['Motor', 'Suspension', 'Transmision', 'Electrico', 'Carroceria', 
                          'Interior', 'Frenos', 'Direccion', 'Escape', 'Refrigeracion', 'Otro']
        self.conditions = ['Nueva', 'Usada - Excelente', 'Usada - Buena', 'Usada - Regular', 'Refaccionada']
        self.shelves = ['A', 'B', 'C', 'D']
        self.levels = [1, 2, 3]
        
        # Listas predefinidas para menús desplegables
        self.common_brands = ['Chevrolet', 'Ford', 'Nissan', 'Toyota', 'Volkswagen', 'Honda', 
                             'Mazda', 'Hyundai', 'Kia', 'Dodge', 'Chrysler', 'Jeep', 'BMW', 
                             'Mercedes-Benz', 'Audi', 'Volvo', 'Subaru', 'Mitsubishi', 'Suzuki',
                             'Peugeot', 'Renault', 'Fiat', 'Seat', 'Opel', 'Citroën']
        self.common_years = [str(year) for year in range(2024, 1980, -1)]  # 2024 a 1981
        self.common_part_names = ['Radiador', 'Alternador', 'Motor de Arranque', 'Compresor A/C', 
                                 'Bomba de Agua', 'Termostato', 'Filtro de Aceite', 'Filtro de Aire',
                                 'Batería', 'Faros Delanteros', 'Faros Traseros', 'Parabrisas',
                                 'Vidrios Laterales', 'Espejos Retrovisores', 'Parachoques Delantero',
                                 'Parachoques Trasero', 'Capó', 'Tapa de Cofre', 'Puertas', 'Guardafangos',
                                 'Amortiguadores', 'Muelles', 'Brazos de Control', 'Rótulas', 'Terminales',
                                 'Caja de Cambios', 'Embrague', 'Diferencial', 'Cardán', 'Semi-ejes',
                                 'Pastillas de Freno', 'Discos de Freno', 'Tambores', 'Cilindros de Freno',
                                 'Calipers', 'Líneas de Freno', 'Volante', 'Columnas de Dirección',
                                 'Cremallera', 'Bomba de Dirección', 'Silenciador', 'Catalizador',
                                 'Múltiple de Escape', 'Tubos de Escape', 'Asientos', 'Tablero',
                                 'Volante Interior', 'Consola Central', 'Alfombras', 'Cortinas',
                                 'Luces Interiores', 'Radio', 'Parlantes', 'Aire Acondicionado']
        self.common_manufacturers = ['ACDelco', 'Bosch', 'Denso', 'Delphi', 'Valeo', 'Mann-Filter',
                                    'Mahle', 'NGK', 'Champion', 'Motorcraft', 'Mopar', 'Genuine Parts',
                                    'Beck Arnley', 'Gates', 'Dayco', 'Continental', 'TRW', 'Monroe',
                                    'KYB', 'Bilstein', 'Brembo', 'Akebono', 'Wagner', 'Raybestos']
        
        # Crear interfaz
        self.create_widgets()
        self.load_dashboard()
    
    def init_database(self):
        """Inicializa la base de datos SQLite"""
        import os
        # Obtener el directorio base del proyecto (dos niveles arriba de src/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        db_path = os.path.join(data_dir, 'autopartes_inventario.db')
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Tabla de vehiculos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id TEXT PRIMARY KEY,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio TEXT NOT NULL,
                vin TEXT NOT NULL,
                color TEXT,
                motor TEXT,
                notas TEXT,
                fecha_ingreso TEXT
            )
        ''')
        
        # Tabla de piezas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS piezas (
                id TEXT PRIMARY KEY,
                stock_number TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio TEXT NOT NULL,
                numero_parte TEXT,
                categoria TEXT NOT NULL,
                fabricante TEXT,
                condicion TEXT NOT NULL,
                precio REAL,
                estante TEXT NOT NULL,
                nivel INTEGER NOT NULL,
                ubicacion TEXT NOT NULL,
                vehiculo_id TEXT,
                notas TEXT,
                fecha_ingreso TEXT,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
            )
        ''')
        
        # Tabla de imagenes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS imagenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pieza_id TEXT NOT NULL,
                imagen_data TEXT NOT NULL,
                orden INTEGER,
                FOREIGN KEY (pieza_id) REFERENCES piezas (id)
            )
        ''')
        
        self.conn.commit()
    
    def setup_theme(self):
        """Configura el tema oscuro de la aplicacion"""
        self.theme = {
            'bg': '#f0f0f0',
            'surface': '#ffffff',
            'surface_alt': '#f8fafc',
            'card': '#ffffff',
            'text': '#1f2937',
            'text_muted': '#6b7280',
            'accent': '#3b82f6',
            'accent_hover': '#2563eb',
            'accent_alt': '#10b981',
            'accent_alt_hover': '#059669',
            'warning': '#f59e0b',
            'purple': '#8b5cf6',
            'danger': '#ef4444',
            'danger_hover': '#dc2626',
            'border': '#d1d5db',
            'input_bg': '#ffffff',
            'header_bg': '#2563eb',
            'selection_text': '#ffffff'
        }
        
        self.root.configure(bg=self.theme['bg'])
        self.root.option_add("*Font", ("Arial", 10))
        self.root.option_add("*Background", self.theme['surface'])
        self.root.option_add("*Foreground", self.theme['text'])
        self.root.option_add("*Label.background", self.theme['surface'])
        self.root.option_add("*Label.foreground", self.theme['text'])
        self.root.option_add("*Frame.background", self.theme['surface'])
        self.root.option_add("*LabelFrame.background", self.theme['surface'])
        self.root.option_add("*LabelFrame.foreground", self.theme['text'])
        self.root.option_add("*Entry.background", self.theme['input_bg'])
        self.root.option_add("*Entry.foreground", self.theme['text'])
        self.root.option_add("*Entry.insertBackground", self.theme['text'])
        self.root.option_add("*Text.background", self.theme['input_bg'])
        self.root.option_add("*Text.foreground", self.theme['text'])
        self.root.option_add("*Text.insertBackground", self.theme['text'])
        self.root.option_add("*TCombobox*Listbox.background", self.theme['surface'])
        self.root.option_add("*TCombobox*Listbox.foreground", self.theme['text'])
        
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except tk.TclError:
            pass
        
        self.style.configure('TFrame', background=self.theme['surface'])
        self.style.configure('TLabel', background=self.theme['surface'], foreground=self.theme['text'])
        self.style.configure('TLabelFrame', background=self.theme['surface'], foreground=self.theme['text'])
        self.style.configure('TNotebook', background=self.theme['bg'], borderwidth=0)
        self.style.configure('TNotebook.Tab', background=self.theme['surface_alt'], foreground=self.theme['text_muted'])
        self.style.map('TNotebook.Tab', background=[('selected', self.theme['surface'])],
                       foreground=[('selected', self.theme['text'])])
        base_tree_layout = self.style.layout('Treeview')
        self.style.layout('DarkTreeview', base_tree_layout)
        self.style.configure('DarkTreeview',
                             background=self.theme['surface'],
                             foreground=self.theme['text'],
                             fieldbackground=self.theme['surface'],
                             bordercolor=self.theme['border'],
                             rowheight=26)
        self.style.map('DarkTreeview',
                       background=[('selected', self.theme['accent'])],
                       foreground=[('selected', self.theme['selection_text'])])
        self.style.configure('DarkTreeview.Heading',
                             background=self.theme['surface_alt'],
                             foreground=self.theme['text'])
        self.style.configure('DarkCombobox.TCombobox',
                             fieldbackground=self.theme['input_bg'],
                             background=self.theme['surface'],
                             foreground=self.theme['text'],
                             insertcolor=self.theme['text'])
        self.style.map('DarkCombobox.TCombobox',
                       fieldbackground=[('readonly', self.theme['surface'])])
        self.style.configure('TScrollbar', background=self.theme['surface_alt'], troughcolor=self.theme['bg'])
    
    def create_widgets(self):
        """Crea la interfaz principal"""
        # Header
        header = tk.Frame(self.root, bg=self.theme['header_bg'], height=80)
        header.pack(fill='x')
        
        title_font = tkfont.Font(family="Arial", size=20, weight="bold")
        title = tk.Label(header, text="Sistema de Inventario de Autopartes", 
                        font=title_font, bg=self.theme['header_bg'], fg=self.theme['text'])
        title.pack(pady=20)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabs
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.inventory_frame = ttk.Frame(self.notebook)
        self.vehicles_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        self.notebook.add(self.inventory_frame, text='Inventario')
        self.notebook.add(self.vehicles_frame, text='Vehiculos')
        
        # Crear contenido de cada tab
        self.create_dashboard_tab()
        self.create_inventory_tab()
        self.create_vehicles_tab()
    
    def get_unique_values_from_db(self, column, table='piezas'):
        """Obtiene valores únicos de una columna en la base de datos"""
        try:
            self.cursor.execute(f'SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL AND {column} != "" ORDER BY {column}')
            return [row[0] for row in self.cursor.fetchall()]
        except:
            return []
    
    def create_autocomplete_combobox(self, parent, textvariable, values, width=28):
        """Crea un Combobox con autocompletado que permite escribir"""
        # Asegurar que values sea una lista válida
        if not values:
            original_values = []
        else:
            original_values = [str(v) for v in values if v is not None]
        
        if not original_values:
            original_values = ['']
        
        combo = ttk.Combobox(parent, textvariable=textvariable, values=original_values, width=width,
                             style='DarkCombobox.TCombobox')
        
        def autocomplete(event):
            """Filtra las opciones mientras el usuario escribe"""
            try:
                # Ignorar teclas de navegación y control
                if event.keysym in ['Up', 'Down', 'Return', 'Tab', 'Escape', 'Shift_L', 'Shift_R', 
                                   'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Left', 'Right']:
                    return
                
                # Usar after para actualizar después de que se procese la tecla
                def update_values():
                    try:
                        current_value = textvariable.get()
                        if current_value:
                            # Filtrar valores que empiecen con lo que el usuario escribió
                            filtered = [v for v in original_values if str(v).lower().startswith(current_value.lower())]
                            if filtered:
                                combo['values'] = filtered
                            else:
                                combo['values'] = original_values
                        else:
                            # Si está vacío, mostrar todos los valores
                            combo['values'] = original_values
                    except:
                        try:
                            combo['values'] = original_values
                        except:
                            pass
                
                combo.after(10, update_values)
                
            except:
                pass
        
        def on_focus_in(event):
            """Restaurar todas las opciones cuando el campo recibe foco"""
            try:
                combo['values'] = original_values
            except:
                pass
        
        def on_focus_out(event):
            """Asegurar que los valores estén restaurados al perder foco"""
            try:
                combo['values'] = original_values
            except:
                pass
        
        # Bindings de eventos
        combo.bind('<KeyRelease>', autocomplete)
        combo.bind('<FocusIn>', on_focus_in)
        combo.bind('<FocusOut>', on_focus_out)
        
        return combo
    
    def create_dashboard_tab(self):
        """Crea el dashboard con estadisticas"""
        # Frame de estadisticas
        stats_frame = tk.Frame(self.dashboard_frame, bg=self.theme['surface'])
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Obtener estadisticas
        self.cursor.execute('SELECT COUNT(*) FROM piezas')
        total_piezas = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(DISTINCT categoria) FROM piezas')
        total_categorias = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM vehiculos')
        total_vehiculos = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT SUM(precio) FROM piezas')
        valor_total = self.cursor.fetchone()[0] or 0
        
        # Mostrar estadisticas
        stats = [
            ("Total Piezas", total_piezas, '#3b82f6'),
            ("Categorias", total_categorias, '#10b981'),
            ("Vehiculos", total_vehiculos, '#8b5cf6'),
            ("Valor Total", f"${valor_total:,.2f} MXN", '#f59e0b')
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief='raised', borderwidth=0, highlightthickness=0)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=label, font=('Arial', 12), bg=color, fg='white').pack(pady=(10,0))
            tk.Label(card, text=str(value), font=('Arial', 24, 'bold'), bg=color, fg='white').pack(pady=(0,10))
        
        # Botones de acciones rapidas
        actions_frame = tk.LabelFrame(self.dashboard_frame, text="Acciones Rapidas", font=('Arial', 14, 'bold'),
                                      bg=self.theme['surface'], fg=self.theme['text'])
        actions_frame.pack(fill='both', padx=20, pady=20, expand=True)
        
        btn_add_part = tk.Button(actions_frame, text="+ Agregar Nueva Pieza", 
                                font=('Arial', 14), bg=self.theme['accent'], fg=self.theme['text'],
                                activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                                command=self.add_part_window, height=3, relief='flat', bd=0)
        btn_add_part.pack(fill='x', padx=20, pady=10)
        
        btn_add_vehicle = tk.Button(actions_frame, text="Registrar Vehiculo", 
                                    font=('Arial', 14), bg=self.theme['accent_alt'], fg=self.theme['text'],
                                    activebackground=self.theme['accent_alt_hover'], activeforeground=self.theme['text'],
                                    command=self.add_vehicle_window, height=3, relief='flat', bd=0)
        btn_add_vehicle.pack(fill='x', padx=20, pady=10)
    
    def create_inventory_tab(self):
        """Crea la pestaña de inventario"""
        # Frame de busqueda
        search_frame = tk.Frame(self.inventory_frame, bg=self.theme['surface'])
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Buscar:", font=('Arial', 12), bg=self.theme['surface'],
                 fg=self.theme['text']).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_inventory())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=40,
                                bg=self.theme['input_bg'], fg=self.theme['text'],
                                insertbackground=self.theme['text'], relief='flat',
                                highlightthickness=1, highlightbackground=self.theme['border'])
        search_entry.pack(side='left', padx=5)
        
        tk.Label(search_frame, text="Categoria:", font=('Arial', 12), bg=self.theme['surface'],
                 fg=self.theme['text']).pack(side='left', padx=5)
        self.filter_category = tk.StringVar(value='Todas')
        category_combo = ttk.Combobox(search_frame, textvariable=self.filter_category, 
                                     values=['Todas'] + self.categories, state='readonly', width=20,
                                     style='DarkCombobox.TCombobox')
        category_combo.pack(side='left', padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_inventory())
        
        btn_add = tk.Button(search_frame, text="+ Agregar Pieza", bg=self.theme['accent'], fg=self.theme['text'],
                           font=('Arial', 11), command=self.add_part_window,
                           activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                           relief='flat', bd=0)
        btn_add.pack(side='right', padx=5)
        
        # Treeview para mostrar piezas
        tree_frame = tk.Frame(self.inventory_frame, bg=self.theme['surface'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side='bottom', fill='x')
        
        # Treeview
        columns = ('Stock', 'Nombre', 'Marca', 'Modelo', 'Año', 'Categoria', 'Ubicacion', 'Precio')
        self.parts_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                       yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                                       style='DarkTreeview')
        
        vsb.config(command=self.parts_tree.yview)
        hsb.config(command=self.parts_tree.xview)
        
        # Configurar columnas
        widths = [120, 150, 100, 100, 60, 100, 80, 80]
        for col, width in zip(columns, widths):
            self.parts_tree.heading(col, text=col)
            self.parts_tree.column(col, width=width)
        
        self.parts_tree.pack(fill='both', expand=True)
        self.parts_tree.bind('<Double-1>', lambda e: self.view_part_details())
        
        # Botones de accion
        btn_frame = tk.Frame(self.inventory_frame, bg=self.theme['surface'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Ver Detalles", command=self.view_part_details,
                 bg=self.theme['accent'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_part,
                 bg=self.theme['danger'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['danger_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Generar QR", command=self.generate_qr,
                 bg=self.theme['purple'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground='#7c3aed', activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        
        self.load_inventory()
    
    def create_vehicles_tab(self):
        """Crea la pestaña de vehiculos"""
        # Frame superior
        top_frame = tk.Frame(self.vehicles_frame, bg=self.theme['surface'])
        top_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(top_frame, text="Vehiculos Donadores", font=('Arial', 16, 'bold'),
                 bg=self.theme['surface'], fg=self.theme['text']).pack(side='left')
        tk.Button(top_frame, text="+ Agregar Vehiculo", bg=self.theme['accent_alt'], fg=self.theme['text'],
                 font=('Arial', 11), command=self.add_vehicle_window,
                 activebackground=self.theme['accent_alt_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='right')
        
        # Treeview para vehiculos
        tree_frame = tk.Frame(self.vehicles_frame, bg=self.theme['surface'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        
        columns = ('Marca', 'Modelo', 'Año', 'VIN', 'Color', 'Motor', 'Piezas')
        self.vehicles_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                         yscrollcommand=vsb.set, style='DarkTreeview')
        vsb.config(command=self.vehicles_tree.yview)
        
        widths = [100, 100, 60, 150, 80, 100, 60]
        for col, width in zip(columns, widths):
            self.vehicles_tree.heading(col, text=col)
            self.vehicles_tree.column(col, width=width)
        
        self.vehicles_tree.pack(fill='both', expand=True)
        
        # Botones
        btn_frame = tk.Frame(self.vehicles_frame, bg=self.theme['surface'])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="Ver Piezas", command=self.view_vehicle_parts,
                 bg=self.theme['accent'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_vehicle,
                 bg=self.theme['danger'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['danger_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        
        self.load_vehicles()
    
    def add_part_window(self):
        """Ventana para agregar nueva pieza"""
        window = tk.Toplevel(self.root)
        window.title("Agregar Nueva Pieza")
        window.geometry("800x700")
        window.grab_set()
        window.configure(bg=self.theme['bg'])
        
        # Canvas con scrollbar
        canvas = tk.Canvas(window, bg=self.theme['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Variables del formulario
        vars_dict = {
            'nombre': tk.StringVar(),
            'marca': tk.StringVar(),
            'modelo': tk.StringVar(),
            'anio': tk.StringVar(),
            'numero_parte': tk.StringVar(),
            'categoria': tk.StringVar(value='Motor'),
            'fabricante': tk.StringVar(),
            'condicion': tk.StringVar(value='Usada - Buena'),
            'precio': tk.StringVar(),
            'estante': tk.StringVar(value='A'),
            'nivel': tk.StringVar(value='1'),
            'vehiculo_id': tk.StringVar(),
            'notas': tk.StringVar()
        }
        
        self.current_images = []
        
        # Obtener valores únicos de la base de datos para autocompletado
        db_nombres = self.get_unique_values_from_db('nombre')
        db_marcas = self.get_unique_values_from_db('marca')
        db_modelos = self.get_unique_values_from_db('modelo')
        db_anios = self.get_unique_values_from_db('anio')
        db_fabricantes = self.get_unique_values_from_db('fabricante')
        db_numero_parte = self.get_unique_values_from_db('numero_parte')
        
        # Combinar valores de BD con listas predefinidas (BD primero, luego comunes)
        # Filtrar valores None y vacíos, y convertir a string
        def clean_values(values):
            unique_by_case = {}
            for value in values:
                if value is None:
                    continue
                value_str = str(value).strip()
                if not value_str:
                    continue
                key = value_str.lower()
                if key not in unique_by_case:
                    unique_by_case[key] = value_str
            return sorted(unique_by_case.values(), key=lambda x: x.lower())
        
        nombres_values = clean_values(db_nombres + self.common_part_names)
        marcas_values = clean_values(db_marcas + self.common_brands)
        modelos_values = clean_values(db_modelos) if db_modelos else []
        anios_values = sorted(set([str(v) for v in (db_anios + self.common_years) if v is not None and str(v).strip()]), reverse=True)
        fabricantes_values = clean_values(db_fabricantes + self.common_manufacturers)
        numero_parte_values = clean_values(db_numero_parte) if db_numero_parte else []
        
        # Asegurar que todas las listas tengan al menos un valor vacío si están vacías
        if not nombres_values:
            nombres_values = ['']
        if not marcas_values:
            marcas_values = ['']
        if not modelos_values:
            modelos_values = ['']
        if not anios_values:
            anios_values = ['']
        if not fabricantes_values:
            fabricantes_values = ['']
        if not numero_parte_values:
            numero_parte_values = ['']
        
        # Precios comunes para menú desplegable
        precios_comunes = ['100', '150', '200', '250', '300', '350', '400', '450', '500', 
                          '600', '700', '800', '900', '1000', '1200', '1500', '2000', 
                          '2500', '3000', '3500', '4000', '5000', '6000', '7000', '8000', 
                          '10000', '12000', '15000', '20000']
        
        # Formulario
        row = 0
        fields = [
            ('Nombre de la Pieza:', 'nombre', 'autocomplete', nombres_values),
            ('Categoria:', 'categoria', 'combo', self.categories),
            ('Marca del Auto:', 'marca', 'autocomplete', marcas_values),
            ('Modelo:', 'modelo', 'autocomplete', modelos_values),
            ('Año:', 'anio', 'autocomplete', anios_values),
            ('Numero de Parte:', 'numero_parte', 'autocomplete', numero_parte_values),
            ('Fabricante:', 'fabricante', 'autocomplete', fabricantes_values),
            ('Condicion:', 'condicion', 'combo', self.conditions),
            ('Precio (MXN):', 'precio', 'autocomplete', precios_comunes),
            ('Estante:', 'estante', 'combo', self.shelves),
            ('Nivel:', 'nivel', 'combo', ['1', '2', '3']),
        ]
        
        for field in fields:
            label_text = field[0]
            var_name = field[1]
            field_type = field[2]
            
            tk.Label(scrollable_frame, text=label_text, font=('Arial', 10), bg=self.theme['surface'],
                     fg=self.theme['text']).grid(
                row=row, column=0, sticky='w', padx=10, pady=5)
            
            if field_type == 'autocomplete':
                combo = self.create_autocomplete_combobox(scrollable_frame, vars_dict[var_name], field[3])
                combo.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
            elif field_type == 'combo':
                combo = ttk.Combobox(scrollable_frame, textvariable=vars_dict[var_name],
                                    values=field[3], state='readonly', width=28,
                                    style='DarkCombobox.TCombobox')
                combo.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
            
            row += 1
        
        # Vehiculo donador
        tk.Label(scrollable_frame, text="Vehiculo Donador:", font=('Arial', 10),
                 bg=self.theme['surface'], fg=self.theme['text']).grid(
            row=row, column=0, sticky='w', padx=10, pady=5)
        
        self.cursor.execute('SELECT id, marca, modelo, anio, vin FROM vehiculos')
        vehicles = self.cursor.fetchall()
        vehicle_options = ['Sin asignar'] + [f"{v[1]} {v[2]} {v[3]} - {v[4]}" for v in vehicles]
        vehicle_ids = [''] + [v[0] for v in vehicles]
        
        vehicle_combo = ttk.Combobox(scrollable_frame, textvariable=vars_dict['vehiculo_id'],
                                    values=vehicle_options, state='readonly', width=28,
                                    style='DarkCombobox.TCombobox')
        vehicle_combo.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        
        def on_vehicle_select(event):
            idx = vehicle_combo.current()
            if idx > 0 and idx <= len(vehicles):
                vehicle = vehicles[idx - 1]
                vars_dict['vehiculo_id'].set(vehicle_ids[idx])
                # Auto-completar marca, modelo y año si están vacíos
                if not vars_dict['marca'].get():
                    vars_dict['marca'].set(vehicle[1])
                if not vars_dict['modelo'].get():
                    vars_dict['modelo'].set(vehicle[2])
                if not vars_dict['anio'].get():
                    vars_dict['anio'].set(vehicle[3])
            else:
                vars_dict['vehiculo_id'].set('')
        
        vehicle_combo.bind('<<ComboboxSelected>>', on_vehicle_select)
        row += 1
        
        # Notas
        tk.Label(scrollable_frame, text="Notas:", font=('Arial', 10),
                 bg=self.theme['surface'], fg=self.theme['text']).grid(
            row=row, column=0, sticky='nw', padx=10, pady=5)
        notes_text = tk.Text(scrollable_frame, height=3, width=30, relief='flat',
                             bg=self.theme['input_bg'], fg=self.theme['text'],
                             insertbackground=self.theme['text'], highlightthickness=1,
                             highlightbackground=self.theme['border'])
        notes_text.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        row += 1
        
        # Imagenes
        tk.Label(scrollable_frame, text="Fotos:", font=('Arial', 10),
                 bg=self.theme['surface'], fg=self.theme['text']).grid(
            row=row, column=0, sticky='nw', padx=10, pady=5)
        
        images_frame = tk.Frame(scrollable_frame, bg=self.theme['surface'])
        images_frame.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        
        def select_images():
            files = filedialog.askopenfilenames(
                title="Seleccionar imagenes",
                filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.gif *.bmp")]
            )
            for file in files:
                with open(file, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                    self.current_images.append(img_data)
            
            for widget in images_frame.winfo_children():
                widget.destroy()
            
            tk.Label(images_frame, text=f"{len(self.current_images)} imagen(es) seleccionada(s)",
                     bg=self.theme['surface'], fg=self.theme['text']).pack()
        
        tk.Button(images_frame, text="Seleccionar Imagenes", command=select_images,
                 bg=self.theme['accent'], fg=self.theme['text'], relief='flat', bd=0,
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text']).pack()
        row += 1
        
        # Botones
        btn_frame = tk.Frame(scrollable_frame, bg=self.theme['surface'])
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_part():
            # Validar campos requeridos
            if not all([vars_dict['nombre'].get(), vars_dict['marca'].get(), 
                       vars_dict['modelo'].get(), vars_dict['anio'].get()]):
                messagebox.showerror("Error", "Por favor completa todos los campos obligatorios")
                return
            
            # Validar precio
            try:
                precio = float(vars_dict['precio'].get() or 0)
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número válido")
                return
            
            # Generar stock number
            stock_number = f"AP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ubicacion = f"{vars_dict['estante'].get()}-{vars_dict['nivel'].get()}"
            
            # Convertir nivel a int para la base de datos
            try:
                nivel_int = int(vars_dict['nivel'].get())
            except:
                nivel_int = 1
            
            # Insertar pieza
            try:
                self.cursor.execute('''
                    INSERT INTO piezas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    stock_number, stock_number, vars_dict['nombre'].get(), vars_dict['marca'].get(),
                    vars_dict['modelo'].get(), vars_dict['anio'].get(), vars_dict['numero_parte'].get() or None,
                    vars_dict['categoria'].get(), vars_dict['fabricante'].get() or None, vars_dict['condicion'].get(),
                    precio, vars_dict['estante'].get(), nivel_int,
                    ubicacion, vars_dict['vehiculo_id'].get() or None, notes_text.get('1.0', 'end').strip() or None,
                    datetime.now().isoformat()
                ))
                
                # Insertar imagenes
                for i, img_data in enumerate(self.current_images):
                    self.cursor.execute('''
                        INSERT INTO imagenes (pieza_id, imagen_data, orden) VALUES (?, ?, ?)
                    ''', (stock_number, img_data, i))
                
                self.conn.commit()
                messagebox.showinfo("Exito", f"Pieza agregada con stock: {stock_number}")
                window.destroy()
                self.load_inventory()
                self.load_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        tk.Button(btn_frame, text="Cancelar", command=window.destroy,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11), width=15,
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Guardar Pieza", command=save_part,
                 bg=self.theme['accent'], fg=self.theme['text'], font=('Arial', 11), width=15,
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_vehicle_window(self):
        """Ventana para agregar vehiculo"""
        window = tk.Toplevel(self.root)
        window.title("Registrar Vehiculo Donador")
        window.geometry("500x450")
        window.grab_set()
        window.configure(bg=self.theme['bg'])
        
        # Variables
        vars_dict = {
            'marca': tk.StringVar(),
            'modelo': tk.StringVar(),
            'anio': tk.StringVar(),
            'vin': tk.StringVar(),
            'color': tk.StringVar(),
            'motor': tk.StringVar(),
            'notas': tk.StringVar()
        }
        
        # Formulario
        fields = [
            ('Marca:', 'marca'),
            ('Modelo:', 'modelo'),
            ('Año:', 'anio'),
            ('VIN / Numero de Serie:', 'vin'),
            ('Color:', 'color'),
            ('Motor:', 'motor')
        ]
        
        for i, (label_text, var_name) in enumerate(fields):
            tk.Label(window, text=label_text, font=('Arial', 10),
                     bg=self.theme['surface'], fg=self.theme['text']).grid(
                row=i, column=0, sticky='w', padx=20, pady=10)
            entry = tk.Entry(window, textvariable=vars_dict[var_name], width=30,
                             bg=self.theme['input_bg'], fg=self.theme['text'],
                             insertbackground=self.theme['text'], relief='flat',
                             highlightthickness=1, highlightbackground=self.theme['border'])
            entry.grid(row=i, column=1, padx=20, pady=10)
        
        # Notas
        tk.Label(window, text="Notas:", font=('Arial', 10),
                 bg=self.theme['surface'], fg=self.theme['text']).grid(
            row=len(fields), column=0, sticky='nw', padx=20, pady=10)
        notes_text = tk.Text(window, height=3, width=30, bg=self.theme['input_bg'],
                             fg=self.theme['text'], insertbackground=self.theme['text'],
                             relief='flat', highlightthickness=1, highlightbackground=self.theme['border'])
        notes_text.grid(row=len(fields), column=1, padx=20, pady=10)
        
        # Botones
        btn_frame = tk.Frame(window, bg=self.theme['surface'])
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        def save_vehicle():
            if not all([vars_dict['marca'].get(), vars_dict['modelo'].get(), 
                       vars_dict['anio'].get(), vars_dict['vin'].get()]):
                messagebox.showerror("Error", "Por favor completa todos los campos obligatorios")
                return
            
            vehicle_id = f"VEH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            try:
                self.cursor.execute('''
                    INSERT INTO vehiculos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vehicle_id, vars_dict['marca'].get(), vars_dict['modelo'].get(),
                    vars_dict['anio'].get(), vars_dict['vin'].get(), vars_dict['color'].get() or None,
                    vars_dict['motor'].get() or None, notes_text.get('1.0', 'end').strip() or None,
                    datetime.now().isoformat()
                ))
                
                self.conn.commit()
                messagebox.showinfo("Exito", "Vehiculo registrado correctamente")
                window.destroy()
                self.load_vehicles()
                self.load_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        tk.Button(btn_frame, text="Cancelar", command=window.destroy,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11), width=15,
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Guardar Vehiculo", command=save_vehicle,
                 bg=self.theme['accent_alt'], fg=self.theme['text'], font=('Arial', 11), width=15,
                 activebackground=self.theme['accent_alt_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
    
    def load_inventory(self):
        """Carga el inventario en el treeview"""
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        self.cursor.execute('''
            SELECT stock_number, nombre, marca, modelo, anio, categoria, ubicacion, precio 
            FROM piezas ORDER BY fecha_ingreso DESC
        ''')
        
        for row in self.cursor.fetchall():
            self.parts_tree.insert('', 'end', values=row)
    
    def filter_inventory(self):
        """Filtra el inventario"""
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        search = self.search_var.get().lower()
        category = self.filter_category.get()
        
        query = '''
            SELECT stock_number, nombre, marca, modelo, anio, categoria, ubicacion, precio 
            FROM piezas WHERE 1=1
        '''
        params = []
        
        if search:
            query += ''' AND (LOWER(nombre) LIKE ? OR LOWER(marca) LIKE ? OR LOWER(modelo) LIKE ? 
                        OR LOWER(anio) LIKE ? OR LOWER(stock_number) LIKE ? OR LOWER(ubicacion) LIKE ?)'''
            params.extend([f'%{search}%'] * 6)
        
        if category != 'Todas':
            query += ' AND categoria = ?'
            params.append(category)
        
        query += ' ORDER BY fecha_ingreso DESC'
        
        self.cursor.execute(query, params)
        for row in self.cursor.fetchall():
            self.parts_tree.insert('', 'end', values=row)
    
    def load_vehicles(self):
        """Carga los vehiculos"""
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
        
        self.cursor.execute('SELECT id, marca, modelo, anio, vin, color, motor FROM vehiculos')
        
        for row in self.cursor.fetchall():
            vehicle_id = row[0]
            self.cursor.execute('SELECT COUNT(*) FROM piezas WHERE vehiculo_id = ?', (vehicle_id,))
            parts_count = self.cursor.fetchone()[0]
            
            self.vehicles_tree.insert('', 'end', values=row[1:] + (parts_count,), tags=(vehicle_id,))
    
    def load_dashboard(self):
        """Recarga el dashboard"""
        # Recrear el dashboard
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        self.create_dashboard_tab()
    
    def view_part_details(self):
        """Ver detalles de una pieza"""
        selection = self.parts_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una pieza")
            return
        
        stock_number = self.parts_tree.item(selection[0])['values'][0]
        
        # Obtener datos de la pieza
        self.cursor.execute('SELECT * FROM piezas WHERE stock_number = ?', (stock_number,))
        part = self.cursor.fetchone()
        
        if not part:
            return
        
        # Ventana de detalles
        window = tk.Toplevel(self.root)
        window.title(f"Detalles - {part[2]}")
        window.geometry("1000x600")
        window.configure(bg=self.theme['bg'])
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(window, bg=self.theme['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columna izquierda - Informacion
        left_frame = tk.Frame(main_frame, bg=self.theme['surface'])
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Informacion general
        info_frame = tk.LabelFrame(left_frame, text="Informacion General", font=('Arial', 12, 'bold'),
                                   bg=self.theme['surface'], fg=self.theme['text'])
        info_frame.pack(fill='x', pady=10)
        
        info_fields = [
            ('Stock:', part[1]),
            ('Nombre:', part[2]),
            ('Marca:', part[3]),
            ('Modelo:', part[4]),
            ('Año:', part[5]),
            ('Numero de Parte:', part[6] or 'N/A'),
            ('Categoria:', part[7]),
            ('Fabricante:', part[8] or 'N/A'),
            ('Condicion:', part[9]),
            ('Precio:', f"${part[10]} MXN" if part[10] else 'N/A'),
            ('Fecha de Ingreso:', datetime.fromisoformat(part[16]).strftime('%d/%m/%Y') if part[16] else 'N/A')
        ]
        
        for label, value in info_fields:
            row_frame = tk.Frame(info_frame, bg=self.theme['surface'])
            row_frame.pack(fill='x', padx=10, pady=2)
            tk.Label(row_frame, text=label, font=('Arial', 10, 'bold'), width=18, anchor='w',
                     bg=self.theme['surface'], fg=self.theme['text']).pack(side='left')
            tk.Label(row_frame, text=str(value), font=('Arial', 10),
                     bg=self.theme['surface'], fg=self.theme['text']).pack(side='left')
        
        # Ubicacion
        location_frame = tk.LabelFrame(left_frame, text="Ubicacion en Almacen", font=('Arial', 12, 'bold'),
                                       bg=self.theme['surface'], fg=self.theme['text'])
        location_frame.pack(fill='x', pady=10)
        
        tk.Label(location_frame, text=part[13], font=('Arial', 36, 'bold'), 
                fg=self.theme['accent'], bg=self.theme['surface']).pack(pady=10)
        tk.Label(location_frame, text=f"Estante {part[11]} - Nivel {part[12]}", 
                font=('Arial', 12), bg=self.theme['surface'], fg=self.theme['text']).pack(pady=5)
        
        # Vehiculo donador
        if part[14]:
            self.cursor.execute('SELECT marca, modelo, anio, vin FROM vehiculos WHERE id = ?', (part[14],))
            vehicle = self.cursor.fetchone()
            if vehicle:
                vehicle_frame = tk.LabelFrame(left_frame, text="Vehiculo Donador", font=('Arial', 12, 'bold'),
                                              bg=self.theme['surface'], fg=self.theme['text'])
                vehicle_frame.pack(fill='x', pady=10)
                
                tk.Label(vehicle_frame, text=f"{vehicle[0]} {vehicle[1]} {vehicle[2]}", 
                        font=('Arial', 11), bg=self.theme['surface'], fg=self.theme['text']).pack(padx=10, pady=5)
                tk.Label(vehicle_frame, text=f"VIN: {vehicle[3]}", 
                        font=('Arial', 10), bg=self.theme['surface'], fg=self.theme['text']).pack(padx=10, pady=5)
        
        # Notas
        if part[15]:
            notes_frame = tk.LabelFrame(left_frame, text="Notas", font=('Arial', 12, 'bold'),
                                        bg=self.theme['surface'], fg=self.theme['text'])
            notes_frame.pack(fill='both', expand=True, pady=10)
            
            notes_text = tk.Text(notes_frame, height=4, wrap='word', font=('Arial', 10),
                                 bg=self.theme['input_bg'], fg=self.theme['text'], relief='flat',
                                 insertbackground=self.theme['text'])
            notes_text.pack(fill='both', expand=True, padx=10, pady=10)
            notes_text.insert('1.0', part[15])
            notes_text.config(state='disabled')
        
        # Columna derecha - QR e imagenes
        right_frame = tk.Frame(main_frame, bg=self.theme['surface'])
        right_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        # Codigo QR
        qr_frame = tk.LabelFrame(right_frame, text="Codigo QR", font=('Arial', 12, 'bold'),
                                 bg=self.theme['surface'], fg=self.theme['text'])
        qr_frame.pack(fill='x', pady=10)
        
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(f"{part[1]}|{part[13]}|{part[2]}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        qr_img = qr_img.resize((200, 200))
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        qr_label = tk.Label(qr_frame, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack(pady=10)
        
        tk.Label(qr_frame, text=f"{part[1]}\n{part[13]}", 
                font=('Arial', 9), bg=self.theme['surface'], fg=self.theme['text']).pack(pady=5)
        
        btn_save_qr = tk.Button(qr_frame, text="Guardar QR", 
                               command=lambda: self.save_qr(part[1], qr_img),
                               bg=self.theme['purple'], fg=self.theme['text'],
                               activebackground='#7c3aed', activeforeground=self.theme['text'],
                               relief='flat', bd=0)
        btn_save_qr.pack(pady=5)
        
        # Imagenes
        images_frame = tk.LabelFrame(right_frame, text="Fotos de la Pieza", font=('Arial', 12, 'bold'),
                                     bg=self.theme['surface'], fg=self.theme['text'])
        images_frame.pack(fill='both', expand=True, pady=10)
        
        self.cursor.execute('SELECT imagen_data FROM imagenes WHERE pieza_id = ? ORDER BY orden', (part[0],))
        images = self.cursor.fetchall()
        
        if images:
            canvas = tk.Canvas(images_frame, height=250, bg=self.theme['surface'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(images_frame, orient="horizontal", command=canvas.xview)
            img_container = tk.Frame(canvas, bg=self.theme['surface'])
            
            canvas.create_window((0, 0), window=img_container, anchor="nw")
            canvas.configure(xscrollcommand=scrollbar.set)
            
            for i, (img_data,) in enumerate(images):
                try:
                    img_bytes = base64.b64decode(img_data)
                    img = Image.open(io.BytesIO(img_bytes))
                    img.thumbnail((180, 180))
                    photo = ImageTk.PhotoImage(img)
                    
                    img_label = tk.Label(img_container, image=photo, cursor="hand2",
                                         bg=self.theme['surface'])
                    img_label.image = photo
                    img_label.pack(side='left', padx=5)
                    img_label.bind('<Button-1>', lambda e, data=img_data: self.show_full_image(data))
                except:
                    pass
            
            img_container.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
            canvas.pack(fill='both', expand=True, padx=5, pady=5)
            scrollbar.pack(fill='x', padx=5)
        else:
            tk.Label(images_frame, text="Sin fotos", font=('Arial', 12), 
                    fg=self.theme['text_muted'], bg=self.theme['surface']).pack(expand=True)
        
        # Boton cerrar
        tk.Button(window, text="Cerrar", command=window.destroy,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(pady=10)
    
    def save_qr(self, stock_number, qr_img):
        """Guardar codigo QR"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            initialfile=f"QR_{stock_number}.png",
            filetypes=[("PNG", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            qr_img.save(filename)
            messagebox.showinfo("Exito", "Codigo QR guardado correctamente")
    
    def show_full_image(self, img_data):
        """Mostrar imagen en tamaño completo con zoom"""
        window = tk.Toplevel(self.root)
        window.title("Visor de Imagen")
        window.geometry("1000x700")
        window.configure(bg=self.theme['bg'])
        
        # Variables para zoom
        self.zoom_level = 1.0
        self.pan_start_x = 0
        self.pan_start_y = 0
        
        # Cargar imagen original
        img_bytes = base64.b64decode(img_data)
        self.original_image = Image.open(io.BytesIO(img_bytes))
        
        # Frame superior con controles
        controls_frame = tk.Frame(window, bg=self.theme['surface'], height=50)
        controls_frame.pack(fill='x', side='top')
        controls_frame.pack_propagate(False)
        
        # Canvas para la imagen
        canvas = tk.Canvas(window, bg=self.theme['bg'], highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Scrollbars
        h_scroll = ttk.Scrollbar(window, orient='horizontal', command=canvas.xview)
        v_scroll = ttk.Scrollbar(window, orient='vertical', command=canvas.yview)
        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        self.image_canvas = canvas
        
        def display_image():
            new_width = int(self.original_image.width * self.zoom_level)
            new_height = int(self.original_image.height * self.zoom_level)
            resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized)
            canvas.delete('all')
            canvas.create_image(0, 0, anchor='nw', image=self.photo)
            canvas.configure(scrollregion=(0, 0, new_width, new_height))
            zoom_label.config(text=f"Zoom: {int(self.zoom_level * 100)}%")
        
        def zoom_in():
            if self.zoom_level < 5.0:
                self.zoom_level *= 1.2
                display_image()
        
        def zoom_out():
            if self.zoom_level > 0.1:
                self.zoom_level *= 0.8
                display_image()
        
        def reset_zoom():
            self.zoom_level = 1.0
            display_image()
        
        def save_image():
            filename = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")]
            )
            if filename:
                with open(filename, 'wb') as f:
                    f.write(img_bytes)
                messagebox.showinfo("Exito", "Imagen guardada correctamente")
        
        # Botones de zoom
        tk.Button(controls_frame, text="Zoom +", command=zoom_in,
                 bg=self.theme['accent'], fg=self.theme['text'], font=('Arial', 11), padx=10,
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5, pady=10)
        tk.Button(controls_frame, text="Zoom -", command=zoom_out,
                 bg=self.theme['accent'], fg=self.theme['text'], font=('Arial', 11), padx=10,
                 activebackground=self.theme['accent_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5, pady=10)
        tk.Button(controls_frame, text="Restablecer", command=reset_zoom,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11), padx=10,
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5, pady=10)
        tk.Button(controls_frame, text="Guardar", command=save_image,
                 bg=self.theme['accent_alt'], fg=self.theme['text'], font=('Arial', 11), padx=10,
                 activebackground=self.theme['accent_alt_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5, pady=10)
        tk.Button(controls_frame, text="Cerrar", command=window.destroy,
                 bg=self.theme['danger'], fg=self.theme['text'], font=('Arial', 11), padx=10,
                 activebackground=self.theme['danger_hover'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='right', padx=10, pady=10)
        
        zoom_label = tk.Label(controls_frame, text=f"Zoom: 100%", 
                             bg=self.theme['surface'], fg=self.theme['text'], font=('Arial', 11))
        zoom_label.pack(side='left', padx=20)
        
        tk.Label(controls_frame, text="Usa scroll del mouse para zoom", 
                bg=self.theme['surface'], fg=self.theme['text_muted'], font=('Arial', 9)).pack(side='right', padx=10)
        
        # Mostrar imagen inicial
        display_image()
        
        # Bindings para zoom con rueda del mouse
        def mouse_wheel(event):
            if event.delta > 0 or event.num == 4:
                zoom_in()
            else:
                zoom_out()
        
        canvas.bind('<MouseWheel>', mouse_wheel)
        canvas.bind('<Button-4>', mouse_wheel)
        canvas.bind('<Button-5>', mouse_wheel)
    
    def generate_qr(self):
        """Generar y mostrar QR de pieza seleccionada"""
        selection = self.parts_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una pieza")
            return
        
        stock_number = self.parts_tree.item(selection[0])['values'][0]
        
        self.cursor.execute('SELECT stock_number, nombre, ubicacion FROM piezas WHERE stock_number = ?', 
                          (stock_number,))
        part = self.cursor.fetchone()
        
        if not part:
            return
        
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(f"{part[0]}|{part[2]}|{part[1]}")
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        window = tk.Toplevel(self.root)
        window.title(f"Codigo QR - {part[0]}")
        window.geometry("400x450")
        window.configure(bg=self.theme['bg'])
        
        qr_img_display = qr_img.resize((300, 300))
        photo = ImageTk.PhotoImage(qr_img_display)
        
        label = tk.Label(window, image=photo, bg=self.theme['bg'])
        label.image = photo
        label.pack(pady=20)
        
        tk.Label(window, text=f"Stock: {part[0]}", font=('Arial', 12, 'bold'),
                bg=self.theme['bg'], fg=self.theme['text']).pack()
        tk.Label(window, text=f"Ubicacion: {part[2]}", font=('Arial', 11),
                bg=self.theme['bg'], fg=self.theme['text']).pack()
        tk.Label(window, text=part[1], font=('Arial', 10),
                bg=self.theme['bg'], fg=self.theme['text_muted']).pack(pady=10)
        
        btn_frame = tk.Frame(window, bg=self.theme['bg'])
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Guardar QR", 
                 command=lambda: self.save_qr(part[0], qr_img),
                 bg=self.theme['purple'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground='#7c3aed', activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Cerrar", command=window.destroy,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(side='left', padx=5)
    
    def delete_part(self):
        """Eliminar pieza"""
        selection = self.parts_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una pieza")
            return
        
        stock_number = self.parts_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmar", "Estas seguro de eliminar esta pieza?"):
            try:
                self.cursor.execute('DELETE FROM imagenes WHERE pieza_id = ?', (stock_number,))
                self.cursor.execute('DELETE FROM piezas WHERE stock_number = ?', (stock_number,))
                self.conn.commit()
                messagebox.showinfo("Exito", "Pieza eliminada correctamente")
                self.load_inventory()
                self.load_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def view_vehicle_parts(self):
        """Ver piezas de un vehiculo"""
        selection = self.vehicles_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona un vehiculo")
            return
        
        vehicle_id = self.vehicles_tree.item(selection[0])['tags'][0]
        
        self.cursor.execute('SELECT marca, modelo, anio FROM vehiculos WHERE id = ?', (vehicle_id,))
        vehicle = self.cursor.fetchone()
        
        window = tk.Toplevel(self.root)
        window.title(f"Piezas de {vehicle[0]} {vehicle[1]} {vehicle[2]}")
        window.geometry("900x500")
        window.configure(bg=self.theme['bg'])
        
        tk.Label(window, text=f"Piezas extraidas de: {vehicle[0]} {vehicle[1]} {vehicle[2]}", 
                font=('Arial', 14, 'bold'), bg=self.theme['bg'], fg=self.theme['text']).pack(pady=10)
        
        # Treeview
        tree_frame = tk.Frame(window, bg=self.theme['surface'])
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side='right', fill='y')
        
        columns = ('Stock', 'Nombre', 'Categoria', 'Ubicacion', 'Precio')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=vsb.set,
                            style='DarkTreeview')
        vsb.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(fill='both', expand=True)
        
        self.cursor.execute('''
            SELECT stock_number, nombre, categoria, ubicacion, precio 
            FROM piezas WHERE vehiculo_id = ?
        ''', (vehicle_id,))
        
        for row in self.cursor.fetchall():
            tree.insert('', 'end', values=row)
        
        tk.Button(window, text="Cerrar", command=window.destroy,
                 bg=self.theme['surface_alt'], fg=self.theme['text'], font=('Arial', 11),
                 activebackground=self.theme['border'], activeforeground=self.theme['text'],
                 relief='flat', bd=0).pack(pady=10)
    
    def delete_vehicle(self):
        """Eliminar vehiculo"""
        selection = self.vehicles_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona un vehiculo")
            return
        
        vehicle_id = self.vehicles_tree.item(selection[0])['tags'][0]
        
        # Verificar si hay piezas asociadas
        self.cursor.execute('SELECT COUNT(*) FROM piezas WHERE vehiculo_id = ?', (vehicle_id,))
        parts_count = self.cursor.fetchone()[0]
        
        if parts_count > 0:
            if not messagebox.askyesno("Advertencia", 
                f"Este vehiculo tiene {parts_count} pieza(s) asociada(s).\n"
                "Deseas eliminarlo de todas formas?\n"
                "(Las piezas no se eliminaran, solo perderan la referencia al vehiculo)"):
                return
        
        if messagebox.askyesno("Confirmar", "Estas seguro de eliminar este vehiculo?"):
            try:
                self.cursor.execute('UPDATE piezas SET vehiculo_id = NULL WHERE vehiculo_id = ?', 
                                  (vehicle_id,))
                self.cursor.execute('DELETE FROM vehiculos WHERE id = ?', (vehicle_id,))
                self.conn.commit()
                messagebox.showinfo("Exito", "Vehiculo eliminado correctamente")
                self.load_vehicles()
                self.load_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def __del__(self):
        """Cerrar conexion a la base de datos"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPartsInventory(root)
    root.mainloop()