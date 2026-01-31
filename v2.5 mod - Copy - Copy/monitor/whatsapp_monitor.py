"""
Monitor de WhatsApp para Sistema de Inventario de Autopartes
VERSION FINAL CORREGIDA - Todos los errores solucionados

Instalación:
pip install selenium webdriver-manager
"""

import sqlite3
import re
import time
import hashlib
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
        
        # Marcas de autos a detectar (expandida y más flexible)
        self.marcas_autos = [
            'toyota', 'honda', 'nissan', 'ford', 'chevrolet', 'chevy', 'mazda',
            'volkswagen', 'vw', 'bmw', 'mercedes', 'benz', 'audi', 'hyundai',
            'kia', 'seat', 'jeep', 'dodge', 'ram', 'gmc', 'buick', 'cadillac',
            'chrysler', 'mitsubishi', 'subaru', 'suzuki', 'isuzu', 'peugeot',
            'renault', 'fiat', 'opel', 'citroen', 'volvo', 'saab', 'lexus',
            'infiniti', 'acura', 'lincoln', 'pontiac', 'mercury', 'oldsmobile',
            'saturn', 'hummer', 'mini', 'smart', 'porsche', 'ferrari', 'lamborghini',
            'alfa romeo', 'land rover', 'jaguar', 'maserati', 'bentley',
            'datsun', 'daihatsu', 'lada', 'tata', 'mahindra'
        ]
        
        # Palabras clave que indican búsqueda de partes
        self.palabras_clave = [
            'busco', 'necesito', 'tiene', 'tienes', 'hay', 'vende', 'vendes',
            'precio', 'cuanto', 'cuesta', 'disponible', 'stock', 'inventario',
            'pieza', 'parte', 'refaccion', 'repuesto', 'quiero', 'vendo',
            'compro', 'interesa', 'cotiza', 'cotizar'
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
            print("✓ Base de datos encontrada")
        else:
            print("⚠ ADVERTENCIA: Base de datos no encontrada en esa ruta")
    
    def conectar_whatsapp(self):
        """Conectar a WhatsApp Web"""
        print("\n🚀 Iniciando WhatsApp Web...")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            print("📱 Modo sin guardar sesión - deberás escanear QR cada vez")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            self.driver.get('https://web.whatsapp.com')
            self.driver.maximize_window()
            
            print("📷 Por favor, escanea el código QR de WhatsApp Web")
            print("⏳ Esperando a que cargue WhatsApp...")
            
            # Esperar a que cargue la interfaz
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("✓ WhatsApp Web conectado!")
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            print("💡 Asegúrate de escanear el código QR")
            raise
    
    def extraer_info_auto(self, mensaje):
        """Extrae información del auto del mensaje - VERSIÓN MÁS FLEXIBLE"""
        mensaje_lower = mensaje.lower()
        
        info = {
            'marca': None,
            'modelo': None,
            'año': None,
            'nombre_parte': None,
            'texto_original': mensaje
        }
        
        # Buscar marca (más flexible)
        for marca in self.marcas_autos:
            # Buscar la marca como palabra completa o parte de palabra
            pattern = r'\b' + re.escape(marca) + r'\w*'
            if re.search(pattern, mensaje_lower):
                info['marca'] = marca
                break
        
        if not info['marca']:
            return None
        
        # Buscar año (1980-2030) - MÁS FLEXIBLE
        regex_año = r'\b(19[8-9]\d|20[0-3]\d)\b'
        años = re.findall(regex_año, mensaje)
        if años:
            info['año'] = años[0]
        
        # Buscar nombres comunes de partes
        partes_comunes = [
            'radiador', 'alternador', 'motor', 'transmision', 'transmisión',
            'faro', 'foco', 'bomba', 'filtro', 'bateria', 'batería',
            'parabrisas', 'espejo', 'puerta', 'cofre', 'capo', 'capó',
            'defensa', 'parachoques', 'llanta', 'rin', 'suspension', 'suspensión',
            'amortiguador', 'muelle', 'clutch', 'embrague', 'freno',
            'disco', 'pastilla', 'tambor', 'caliper', 'volante',
            'cremallera', 'direccion', 'dirección', 'escape', 'catalizador',
            'silenciador', 'asiento', 'tablero', 'consola', 'compresor',
            'condensador', 'evaporador', 'termostato', 'electroventilador',
            'sensor', 'switch', 'relay', 'fusible', 'control', 'modulo', 'módulo'
        ]
        
        for parte in partes_comunes:
            if parte in mensaje_lower:
                info['nombre_parte'] = parte
                break
        
        # Extraer posible modelo (palabras después de la marca) - MÁS FLEXIBLE
        palabras = mensaje.split()
        for i, palabra in enumerate(palabras):
            palabra_lower = palabra.lower()
            # Si encontramos la marca
            if info['marca'] in palabra_lower or palabra_lower in info['marca']:
                # Tomar las siguientes 1-3 palabras como modelo
                if i + 1 < len(palabras):
                    modelo_palabras = []
                    for j in range(i + 1, min(i + 4, len(palabras))):
                        palabra_modelo = palabras[j]
                        # Saltar si es un año
                        if re.match(r'^\d{4}$', palabra_modelo):
                            if not info['año']:
                                info['año'] = palabra_modelo
                            continue
                        # Saltar palabras muy cortas o comunes
                        if len(palabra_modelo) < 2 or palabra_modelo.lower() in ['de', 'del', 'la', 'el', 'y', 'o']:
                            continue
                        modelo_palabras.append(palabra_modelo)
                    
                    if modelo_palabras:
                        info['modelo'] = ' '.join(modelo_palabras[:2])  # Máximo 2 palabras
                break
        
        return info
    
    def buscar_en_inventario(self, marca, modelo=None, año=None, nombre_parte=None):
        """Busca partes en el inventario - BÚSQUEDA MÁS FLEXIBLE"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Búsqueda más flexible usando OR en lugar de AND
            query = """
                SELECT stock_number, nombre, marca, modelo, anio, 
                       categoria, ubicacion, precio, condicion
                FROM piezas 
                WHERE (LOWER(marca) LIKE ? OR LOWER(modelo) LIKE ?)
            """
            params = [f'%{marca}%', f'%{marca}%']
            
            # Si hay modelo, agregarlo como OR adicional
            if modelo:
                query += " OR LOWER(modelo) LIKE ?"
                params.append(f'%{modelo}%')
            
            # Si hay año, agregarlo como OR adicional (no AND)
            if año:
                query += " OR anio LIKE ?"
                params.append(f'%{año}%')
            
            # Si hay nombre de parte, agregarlo como OR
            if nombre_parte:
                query += " OR LOWER(nombre) LIKE ?"
                params.append(f'%{nombre_parte}%')
            
            query += " LIMIT 20"
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            # Si no encuentra nada, buscar solo por marca
            if not resultados and marca:
                print(f"   [INFO] Búsqueda flexible: solo por marca")
                cursor.execute("""
                    SELECT stock_number, nombre, marca, modelo, anio, 
                           categoria, ubicacion, precio, condicion
                    FROM piezas 
                    WHERE LOWER(marca) LIKE ?
                    LIMIT 20
                """, [f'%{marca}%'])
                resultados = cursor.fetchall()
            
            conn.close()
            return resultados
            
        except Exception as e:
            print(f"❌ Error en base de datos: {e}")
            return []
    
    def crear_mensaje_notificacion(self, chat_nombre, info_auto, partes):
        """Crea el mensaje de notificación con emojis de WhatsApp"""
        mensaje = "🚨 ALERTA DE INVENTARIO 🚨\n\n"
        mensaje += f"💬 Chat: {chat_nombre}\n"
        mensaje += f"🔍 Busqueda:\n"
        mensaje += f"   🚗 Marca: {info_auto['marca'].upper()}\n"
        
        if info_auto['modelo']:
            mensaje += f"   📋 Modelo: {info_auto['modelo']}\n"
        
        if info_auto['año']:
            mensaje += f"   📅 Año: {info_auto['año']}\n"
        
        if info_auto['nombre_parte']:
            mensaje += f"   🔧 Parte: {info_auto['nombre_parte']}\n"
        
        # Mensaje original sin caracteres especiales
        texto_limpio = info_auto['texto_original'].replace('\n', ' ')[:100]
        mensaje += f"\n💭 Mensaje: {texto_limpio}\n\n"
        
        if partes:
            mensaje += f"✅ {len(partes)} PARTE(S) DISPONIBLE(S):\n"
            mensaje += "━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for i, parte in enumerate(partes[:10], 1):
                stock, nombre, marca, modelo, año, cat, ubic, precio, cond = parte
                mensaje += f"{i}. {nombre}\n"
                mensaje += f"🏷 Stock: {stock}\n"
                mensaje += f"🚙 Auto: {marca} {modelo} {año}\n"
                mensaje += f"📍 Ubicacion: {ubic}\n"
                mensaje += f"📦 Categoria: {cat}\n"
                if precio:
                    mensaje += f"💰 Precio: ${precio:.2f} MXN\n"
                mensaje += f"⭐ Estado: {cond}\n\n"
            
            if len(partes) > 10:
                mensaje += f"➕ ...y {len(partes) - 10} parte(s) mas\n"
        else:
            mensaje += "❌ No se encontraron partes\n"
        
        mensaje += "━━━━━━━━━━━━━━━━━━━━"
        return mensaje
    
    def enviar_notificacion(self, mensaje):
        """Envía notificación a ti mismo - VERSION ROBUSTA"""
        max_intentos = 3
        
        for intento in range(max_intentos):
            try:
                if intento > 0:
                    print(f"   ↻ Reintentando envío ({intento + 1}/{max_intentos})...")
                    time.sleep(2)
                else:
                    print("📤 Enviando notificación...")
                
                # Re-obtener elementos en cada intento (evita stale element)
                search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.click()
                time.sleep(0.5)
                
                # Limpiar búsqueda anterior
                search_box.clear()
                time.sleep(0.3)
                search_box.send_keys(Keys.ESCAPE)
                time.sleep(0.3)
                
                # Re-obtener el search_box después de limpiar
                search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.clear()
                time.sleep(0.3)
                
                search_box.send_keys(self.mi_nombre)
                time.sleep(2)
                
                # Hacer clic en el primer resultado
                try:
                    chat = self.driver.find_element(By.XPATH, f'//span[@title="{self.mi_nombre}"]')
                    chat.click()
                    time.sleep(1.5)
                except:
                    print(f"   ⚠ No se encontró chat con nombre '{self.mi_nombre}'")
                    if intento < max_intentos - 1:
                        continue
                    else:
                        print("   💡 Intenta enviar un mensaje a ti mismo primero en WhatsApp")
                        return
                
                # Limpiar mensaje de caracteres especiales
                mensaje_limpio = ''.join(c if ord(c) < 128 else ' ' for c in mensaje)
                
                # Re-obtener el input box
                input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                input_box.click()
                time.sleep(0.5)
                
                # Limpiar cualquier texto previo
                input_box.clear()
                time.sleep(0.3)
                
                # Re-obtener input box después de limpiar
                input_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
                
                # Enviar mensaje
                input_box.send_keys(mensaje_limpio)
                time.sleep(0.5)
                input_box.send_keys(Keys.ENTER)
                time.sleep(1)
                
                print("✓ Notificación enviada exitosamente")
                return  # Éxito, salir de la función
                
            except Exception as e:
                error_msg = str(e).lower()
                if "stale element" in error_msg:
                    if intento < max_intentos - 1:
                        print(f"   ⚠ Elemento stale detectado, reintentando...")
                        continue
                    else:
                        print(f"   ⚠ Error stale persistente, la notificación puede haberse enviado")
                        return
                elif intento < max_intentos - 1:
                    print(f"   ⚠ Error en intento {intento + 1}: {str(e)[:60]}...")
                    continue
                else:
                    print(f"❌ Error al enviar notificación después de {max_intentos} intentos")
                    print(f"   Error: {str(e)[:80]}...")
    
    def monitorear_chat(self, nombre_chat):
        """Monitorea un chat específico - VERSIÓN FINAL CORREGIDA"""
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
                print(f"❌ No se encontró el chat '{nombre_chat}'")
                print("💡 Verifica que el nombre sea exacto (mayúsculas, espacios, emojis)")
                
                # Limpiar búsqueda antes de salir
                try:
                    search_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                    search_box.clear()
                    search_box.send_keys(Keys.ESCAPE)
                except:
                    pass
                return
            
            # ============================================
            # SCROLL HACIA ABAJO - CORREGIDO
            # ============================================
            try:
                # Ejecutar scroll usando JavaScript - más confiable
                self.driver.execute_script("""
                    var element = document.querySelector('div[data-testid="conversation-panel-body"]');
                    if (element) {
                        element.scrollTop = element.scrollHeight;
                    }
                """)
                time.sleep(1)
            except Exception as e:
                # Si falla, intentar método alternativo
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                except:
                    pass
                # No es crítico si falla el scroll
            
            # ============================================
            # OBTENER MENSAJES - SELECTOR CORRECTO
            # ============================================
            mensajes = []
            
            # Selector encontrado por diagnóstico: div._akbu span
            try:
                mensajes = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'div._akbu span'
                )
                print(f"   ✓ Selector principal: {len(mensajes)} elementos")
            except Exception as e:
                print(f"   ⚠ Error con selector principal: {e}")
            
            # Backup: Selector alternativo XPATH genérico
            if not mensajes:
                try:
                    mensajes = self.driver.find_elements(
                        By.XPATH,
                        '//span[@dir="ltr"]'
                    )
                    print(f"   ✓ Selector alternativo: {len(mensajes)} elementos")
                except Exception as e:
                    print(f"   ⚠ Error con selector alternativo: {e}")
            
            # DEBUG: Mostrar primeros mensajes
            if mensajes:
                print(f"\n   📊 Total mensajes encontrados: {len(mensajes)}")
                print(f"   📋 Mostrando últimos 5 mensajes:")
                for i, msg in enumerate(mensajes[-5:], 1):
                    try:
                        texto = msg.text
                        if texto:
                            print(f"      {i}. {texto[:80]}...")
                    except:
                        pass
                print()
            else:
                print(f"   ⚠ NO se encontraron mensajes en el chat")
                return
            
            # ============================================
            # PROCESAR MENSAJES
            # ============================================
            mensajes_nuevos = 0
            mensajes_con_auto = 0
            
            for elemento_mensaje in mensajes[-30:]:  # Últimos 30 mensajes
                try:
                    texto = elemento_mensaje.text
                    
                    if not texto or len(texto) < 3:
                        continue
                    
                    # Crear ID único usando hash
                    mensaje_hash = hashlib.md5(texto.encode()).hexdigest()
                    mensaje_id = f"{nombre_chat}:{mensaje_hash}"
                    
                    # Evitar procesar el mismo mensaje dos veces
                    if mensaje_id in self.mensajes_procesados:
                        continue
                    
                    self.mensajes_procesados.add(mensaje_id)
                    mensajes_nuevos += 1
                    
                    # Analizar el mensaje
                    info_auto = self.extraer_info_auto(texto)
                    
                    if info_auto:
                        mensajes_con_auto += 1
                        print(f"\n   🚗 AUTO DETECTADO en '{nombre_chat}':")
                        print(f"      ├─ Marca: {info_auto['marca']}")
                        if info_auto['modelo']:
                            print(f"      ├─ Modelo: {info_auto['modelo']}")
                        if info_auto['año']:
                            print(f"      ├─ Año: {info_auto['año']}")
                        if info_auto['nombre_parte']:
                            print(f"      ├─ Parte: {info_auto['nombre_parte']}")
                        print(f"      └─ Texto: {texto[:60]}...")
                        
                        # Verificar si parece una búsqueda
                        es_busqueda = any(palabra in texto.lower() for palabra in self.palabras_clave)
                        
                        if not es_busqueda:
                            print(f"      💡 El mensaje menciona auto pero no parece búsqueda activa")
                        
                        # Buscar en inventario (siempre, incluso si no parece búsqueda)
                        partes = self.buscar_en_inventario(
                            info_auto['marca'],
                            info_auto['modelo'],
                            info_auto['año'],
                            info_auto['nombre_parte']
                        )
                        
                        print(f"      🔍 Partes encontradas: {len(partes)}")
                        
                        # Enviar notificación si hay partes
                        if partes:
                            mensaje_notif = self.crear_mensaje_notificacion(
                                nombre_chat, info_auto, partes
                            )
                            self.enviar_notificacion(mensaje_notif)
                        else:
                            print(f"      ℹ No hay partes disponibles para este auto")
                
                except Exception as e:
                    error_msg = str(e).lower()
                    if "stale element" in error_msg:
                        # Elemento stale - el mensaje ya fue procesado o WhatsApp lo actualizó
                        continue
                    else:
                        print(f"   ⚠ Error procesando mensaje: {str(e)[:60]}...")
                    continue
            
            if mensajes_nuevos == 0:
                print(f"   ℹ Sin mensajes nuevos")
            else:
                print(f"   ✓ Procesados: {mensajes_nuevos} mensajes nuevos")
                print(f"   🚗 Autos detectados: {mensajes_con_auto}")
            
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
            print(f"❌ Error monitoreando '{nombre_chat}': {e}")
            import traceback
            traceback.print_exc()
            
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
        print("🔍 MONITOR DE WHATSAPP - INVENTARIO DE AUTOPARTES")
        print("="*60)
        print(f"📂 Base de datos: {self.db_path}")
        print(f"💬 Chats monitoreados: {', '.join(self.chats_monitoreados)}")
        print(f"⏱️  Intervalo: {intervalo} segundos")
        print("="*60 + "\n")
        
        self.conectar_whatsapp()
        
        print("\n✓ Monitoreo iniciado. Presiona Ctrl+C para detener.\n")
        
        try:
            ciclo = 0
            while True:
                ciclo += 1
                print(f"\n{'='*60}")
                print(f"🔄 Ciclo #{ciclo} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")
                
                for chat in self.chats_monitoreados:
                    print(f"\n📱 Revisando '{chat}'...")
                    self.monitorear_chat(chat)
                
                print(f"\n⏳ Esperando {intervalo} segundos hasta el próximo ciclo...")
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo monitor...")
            self.cerrar()
        except Exception as e:
            print(f"\n❌ Error crítico: {e}")
            import traceback
            traceback.print_exc()
            self.cerrar()
    
    def cerrar(self):
        """Cierra el navegador"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        print("✓ Monitor cerrado")


if __name__ == "__main__":
    print("Este archivo debe ser importado desde run_monitor.py")
    print("Ejecuta: python run_monitor.py")
