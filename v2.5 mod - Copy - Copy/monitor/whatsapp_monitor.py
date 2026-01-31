"""
Monitor de WhatsApp para Sistema de Inventario de Autopartes
Detecta menciones de autos y busca en el inventario

Instalación:
pip install selenium webdriver-manager

Requisitos:
- Tener WhatsApp Web abierto en el navegador
- Configurar los chats a monitorear
"""

import sqlite3
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os

class WhatsAppInventoryMonitor:
    def __init__(self, db_path='data/autopartes_inventario.db'):
        """Inicializar monitor"""
        # Ruta absoluta a la base de datos
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.base_dir, db_path)
        
        # Marcas de autos a detectar (expandida)
        self.marcas_autos = [
            'toyota', 'honda', 'nissan', 'ford', 'chevrolet', 'chevy', 'mazda',
            'volkswagen', 'vw', 'bmw', 'mercedes', 'benz', 'audi', 'hyundai',
            'kia', 'seat', 'jeep', 'dodge', 'ram', 'gmc', 'buick', 'cadillac',
            'chrysler', 'mitsubishi', 'subaru', 'suzuki', 'isuzu', 'peugeot',
            'renault', 'fiat', 'opel', 'citroen', 'volvo', 'saab', 'lexus',
            'infiniti', 'acura', 'lincoln', 'pontiac', 'mercury', 'oldsmobile',
            'saturn', 'hummer', 'mini', 'smart', 'porsche', 'ferrari', 'lamborghini',
            'alfa romeo', 'land rover', 'jaguar', 'maserati', 'bentley'
        ]
        
        # Chats a monitorear (configurar con nombres reales)
        self.chats_monitoreados = [
            "Grupo Ventas 1",
            "Cliente Juan",
            "Cliente Pedro"
        ]
        
        # Tu nombre para notificaciones (como aparece en WhatsApp)
        self.mi_nombre = "Yo"
        
        # Control de mensajes procesados
        self.mensajes_procesados = set()
        
        # Configurar Selenium
        self.driver = None
        
        print(f"Base de datos configurada en: {self.db_path}")
        if os.path.exists(self.db_path):
            print("Base de datos encontrada")
        else:
            print("ADVERTENCIA: Base de datos no encontrada en esa ruta")
    
    def conectar_whatsapp(self):
        """Conectar a WhatsApp Web"""
        print("\nIniciando WhatsApp Web...")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            print("Modo sin guardar sesion - deberás escanear QR cada vez")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            self.driver.get('https://web.whatsapp.com')
            self.driver.maximize_window()
            
            print("Por favor, escanea el codigo QR de WhatsApp Web")
            print("Esperando a que cargue WhatsApp...")
            
            # Esperar a que cargue la interfaz
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("WhatsApp Web conectado!")
            time.sleep(3)
            
        except Exception as e:
            print(f"Error al conectar: {e}")
            print("Asegurate de escanear el codigo QR")
            raise
    
    def extraer_info_auto(self, mensaje):
        """Extrae información del auto del mensaje"""
        mensaje_lower = mensaje.lower()
        
        info = {
            'marca': None,
            'modelo': None,
            'año': None,
            'texto_original': mensaje
        }
        
        # Buscar marca
        for marca in self.marcas_autos:
            if marca in mensaje_lower:
                info['marca'] = marca
                break
        
        if not info['marca']:
            return None
        
        # Buscar año (1980-2030)
        regex_año = r'\b(19[8-9]\d|20[0-3]\d)\b'
        años = re.findall(regex_año, mensaje)
        if años:
            info['año'] = años[0]
        
        # Extraer posible modelo (palabras después de la marca)
        palabras = mensaje.split()
        for i, palabra in enumerate(palabras):
            if palabra.lower() == info['marca'] or info['marca'] in palabra.lower():
                if i + 1 < len(palabras):
                    modelo_palabras = []
                    for j in range(i + 1, min(i + 3, len(palabras))):
                        if not re.match(r'^\d{4}$', palabras[j]):
                            modelo_palabras.append(palabras[j])
                        else:
                            break
                    if modelo_palabras:
                        info['modelo'] = ' '.join(modelo_palabras)
                break
        
        return info
    
    def buscar_en_inventario(self, marca, modelo=None, año=None):
        """Busca partes en el inventario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
                SELECT stock_number, nombre, marca, modelo, anio, 
                       categoria, ubicacion, precio, condicion
                FROM piezas 
                WHERE LOWER(marca) LIKE ?
            """
            params = [f'%{marca}%']
            
            if modelo:
                query += " AND LOWER(modelo) LIKE ?"
                params.append(f'%{modelo}%')
            
            if año:
                query += " AND anio = ?"
                params.append(año)
            
            query += " LIMIT 20"
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conn.close()
            
            return resultados
            
        except Exception as e:
            print(f"Error en base de datos: {e}")
            return []
    
    def crear_mensaje_notificacion(self, chat_nombre, info_auto, partes):
        """Crea el mensaje de notificación con emojis de WhatsApp"""
        # Usar emojis simples compatibles
        mensaje = "🚨 *ALERTA DE INVENTARIO* 🚨\n\n"
        mensaje += f"💬 *Chat:* {chat_nombre}\n"
        mensaje += f"🔍 *Busqueda:*\n"
        mensaje += f"   🚗 Marca: {info_auto['marca'].upper()}\n"
        
        if info_auto['modelo']:
            mensaje += f"   📋 Modelo: {info_auto['modelo']}\n"
        
        if info_auto['año']:
            mensaje += f"   📅 Ano: {info_auto['año']}\n"
        
        # Mensaje original sin caracteres especiales
        texto_limpio = info_auto['texto_original'].replace('\n', ' ')
        mensaje += f"\n💭 *Mensaje:* {texto_limpio}\n\n"
        
        if partes:
            mensaje += f"✅ *{len(partes)} PARTE(S) DISPONIBLE(S):*\n"
            mensaje += "━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for i, parte in enumerate(partes[:10], 1):
                stock, nombre, marca, modelo, año, cat, ubic, precio, cond = parte
                mensaje += f"*{i}. {nombre}*\n"
                mensaje += f"🏷️ Stock: {stock}\n"
                mensaje += f"🚙 Auto: {marca} {modelo} {año}\n"
                mensaje += f"📍 Ubicacion: {ubic}\n"
                mensaje += f"📦 Categoria: {cat}\n"
                if precio:
                    mensaje += f"💰 Precio: ${precio:.2f} MXN\n"
                mensaje += f"⭐ Estado: {cond}\n\n"
            
            if len(partes) > 10:
                mensaje += f"➕ ...y {len(partes) - 10} parte(s) mas\n"
        else:
            mensaje += "❌ *No se encontraron partes*\n"
        
        mensaje += "━━━━━━━━━━━━━━━━━━━━"
        return mensaje
    
    def enviar_notificacion(self, mensaje):
        """Envía notificación a ti mismo"""
        try:
            print("Enviando notificacion...")
            
            # Buscar chat contigo mismo
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            time.sleep(0.5)
            
            # Limpiar búsqueda anterior
            search_box.clear()
            time.sleep(0.3)
            search_box.send_keys(Keys.ESCAPE)
            time.sleep(0.3)
            search_box.clear()
            
            search_box.send_keys(self.mi_nombre)
            time.sleep(2)
            
            # Hacer clic en el primer resultado
            try:
                chat = self.driver.find_element(By.XPATH, f'//span[@title="{self.mi_nombre}"]')
                chat.click()
                time.sleep(1)
            except:
                print(f"No se encontro chat con nombre '{self.mi_nombre}'")
                print("Intenta enviar un mensaje a ti mismo primero en WhatsApp")
                return
            
            # Limpiar mensaje de caracteres especiales
            mensaje_limpio = ''.join(c if ord(c) < 128 else ' ' for c in mensaje)
            
            # Enviar mensaje usando ENTER en lugar de buscar el botón
            input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            input_box.click()
            time.sleep(0.5)
            
            input_box.send_keys(mensaje_limpio)
            time.sleep(0.5)
            
            # Enviar con ENTER (más confiable que buscar el botón)
            input_box.send_keys(Keys.ENTER)
            time.sleep(1)
            
            print("Notificacion enviada exitosamente")
            
        except Exception as e:
            print(f"Error al enviar notificacion: {e}")
            print("Intentando metodo alternativo...")
            
            # Método alternativo si falla el primero
            try:
                input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                input_box.click()
                time.sleep(0.3)
                
                # Limpiar y enviar
                mensaje_simple = ''.join(c if ord(c) < 128 else '' for c in mensaje)
                input_box.send_keys(mensaje_simple)
                time.sleep(0.3)
                input_box.send_keys(Keys.ENTER)
                
                print("Notificacion enviada (metodo alternativo)")
            except Exception as e2:
                print(f"Error en metodo alternativo: {e2}")
    
    def monitorear_chat(self, nombre_chat):
        """Monitorea un chat específico"""
        try:
            # Buscar el chat
            search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.click()
            time.sleep(0.5)
            
            # Limpiar búsqueda anterior
            search_box.clear()
            time.sleep(0.3)
            search_box.send_keys(Keys.ESCAPE)
            time.sleep(0.3)
            search_box.clear()
            
            # Nueva búsqueda
            search_box.send_keys(nombre_chat)
            time.sleep(2)
            
            # Abrir el chat
            try:
                chat = self.driver.find_element(By.XPATH, f'//span[@title="{nombre_chat}"]')
                chat.click()
                time.sleep(2)
            except:
                print(f"No se encontro el chat '{nombre_chat}'")
                print("Verifica que el nombre sea exacto (mayusculas, espacios, emojis)")
                
                # Limpiar búsqueda antes de salir
                try:
                    search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                    search_box.clear()
                    search_box.send_keys(Keys.ESCAPE)
                except:
                    pass
                return
            
            # Obtener mensajes
            mensajes = self.driver.find_elements(
                By.XPATH, 
                '//div[contains(@class, "message-in") or contains(@class, "message-out")]//span[contains(@class, "selectable-text")]'
            )
            
            mensajes_nuevos = 0
            for elemento_mensaje in mensajes[-20:]:
                try:
                    texto = elemento_mensaje.text
                    
                    if not texto or len(texto) < 5:
                        continue
                    
                    # Crear ID único para el mensaje
                    mensaje_id = f"{nombre_chat}:{texto[:50]}"
                    
                    # Evitar procesar el mismo mensaje dos veces
                    if mensaje_id in self.mensajes_procesados:
                        continue
                    
                    self.mensajes_procesados.add(mensaje_id)
                    mensajes_nuevos += 1
                    
                    # Analizar el mensaje
                    info_auto = self.extraer_info_auto(texto)
                    
                    if info_auto:
                        print(f"\n[CAR] Auto detectado en '{nombre_chat}':")
                        print(f"   >> Marca: {info_auto['marca']}")
                        if info_auto['modelo']:
                            print(f"   >> Modelo: {info_auto['modelo']}")
                        if info_auto['año']:
                            print(f"   >> Ano: {info_auto['año']}")
                        
                        # Buscar en inventario
                        partes = self.buscar_en_inventario(
                            info_auto['marca'],
                            info_auto['modelo'],
                            info_auto['año']
                        )
                        
                        print(f"   [#] Partes encontradas: {len(partes)}")
                        
                        # Enviar notificación si hay partes
                        if partes:
                            mensaje_notif = self.crear_mensaje_notificacion(
                                nombre_chat, info_auto, partes
                            )
                            self.enviar_notificacion(mensaje_notif)
                
                except Exception as e:
                    continue
            
            if mensajes_nuevos == 0:
                print(f"   Sin mensajes nuevos")
            
            # Limpiar el campo de búsqueda al finalizar
            try:
                search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.click()
                time.sleep(0.2)
                search_box.clear()
                search_box.send_keys(Keys.ESCAPE)
                time.sleep(0.2)
            except:
                pass
            
        except Exception as e:
            print(f"Error monitoreando '{nombre_chat}': {e}")
            
            # Intentar limpiar búsqueda incluso si hay error
            try:
                search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.clear()
                search_box.send_keys(Keys.ESCAPE)
            except:
                pass
    
    def iniciar_monitoreo(self, intervalo=30):
        """Inicia el monitoreo continuo"""
        print("\n" + "="*60)
        print("MONITOR DE WHATSAPP - INVENTARIO DE AUTOPARTES")
        print("="*60)
        print(f"Base de datos: {self.db_path}")
        print(f"Chats monitoreados: {', '.join(self.chats_monitoreados)}")
        print(f"Intervalo: {intervalo} segundos")
        print("="*60 + "\n")
        
        self.conectar_whatsapp()
        
        print("\nMonitoreo iniciado. Presiona Ctrl+C para detener.\n")
        
        try:
            ciclo = 0
            while True:
                ciclo += 1
                print(f"\n{'='*60}")
                print(f"Ciclo #{ciclo} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")
                
                for chat in self.chats_monitoreados:
                    print(f"\nRevisando '{chat}'...")
                    self.monitorear_chat(chat)
                
                print(f"\nEsperando {intervalo} segundos hasta el proximo ciclo...")
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\nDeteniendo monitor...")
            self.cerrar()
        except Exception as e:
            print(f"\nError critico: {e}")
            self.cerrar()
    
    def cerrar(self):
        """Cierra el navegador"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        print("Monitor cerrado")


if __name__ == "__main__":
    print("Este archivo debe ser importado desde run_monitor.py")
    print("Ejecuta: python run_monitor.py")