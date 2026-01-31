"""
SCRIPT DE DIAGNÓSTICO - Encuentra el selector correcto de WhatsApp
Ejecuta: python diagnostico_whatsapp.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def diagnosticar_whatsapp():
    print("="*70)
    print("DIAGNÓSTICO DE WHATSAPP WEB")
    print("="*70)
    print("\n1. Abriendo Chrome...")
    
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    driver.get('https://web.whatsapp.com')
    driver.maximize_window()
    
    print("\n2. ⚠️ ESCANEA EL CÓDIGO QR DE WHATSAPP WEB")
    print("   Esperando 45 segundos...")
    
    # Esperar a que cargue
    try:
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("\n3. ✓ WhatsApp cargado")
    except:
        print("\n3. ❌ No se pudo cargar WhatsApp")
        driver.quit()
        return
    
    time.sleep(3)
    
    # Buscar el chat de prueba
    print("\n4. Abriendo chat 'Prueba partes'...")
    
    try:
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        time.sleep(0.5)
        search_box.send_keys("Prueba partes")
        time.sleep(2)
        
        chat = driver.find_element(By.XPATH, '//span[@title="Prueba partes"]')
        chat.click()
        print("   ✓ Chat abierto")
        time.sleep(3)
    except Exception as e:
        print(f"   ❌ Error abriendo chat: {e}")
        print("\n   💡 Asegúrate de que el chat se llame EXACTAMENTE 'Prueba partes'")
        driver.quit()
        return
    
    print("\n5. 🔍 PROBANDO SELECTORES...")
    print("="*70)
    
    # Lista de selectores a probar
    selectores = [
        ("CSS: span.selectable-text.copyable-text", 
         By.CSS_SELECTOR, "span.selectable-text.copyable-text"),
        
        ("CSS: span.selectable-text", 
         By.CSS_SELECTOR, "span.selectable-text"),
        
        ("XPATH: div[@role='row']//span", 
         By.XPATH, "//div[@role='row']//span[contains(@class, 'selectable-text')]"),
        
        ("CSS: div[data-testid='msg-container'] span", 
         By.CSS_SELECTOR, "div[data-testid='msg-container'] span"),
        
        ("XPATH: Mensajes genérico", 
         By.XPATH, "//span[@dir='ltr']"),
        
        ("CSS: Clase _ao3e", 
         By.CSS_SELECTOR, "span._ao3e"),
        
        ("CSS: Clase _akbu", 
         By.CSS_SELECTOR, "div._akbu span"),
        
        ("XPATH: conversation-panel", 
         By.XPATH, "//div[@data-testid='conversation-panel-messages']//span"),
    ]
    
    mejores_resultados = []
    
    for nombre, tipo, selector in selectores:
        try:
            elementos = driver.find_elements(tipo, selector)
            count = len(elementos)
            
            print(f"\n📊 {nombre}")
            print(f"   Elementos encontrados: {count}")
            
            if count > 0:
                # Mostrar primeros 3 mensajes
                print("   Primeros mensajes:")
                for i, elem in enumerate(elementos[:3], 1):
                    try:
                        texto = elem.text
                        if texto and len(texto.strip()) > 0:
                            print(f"      {i}. '{texto[:60]}'")
                            if count not in [x[0] for x in mejores_resultados]:
                                mejores_resultados.append((count, nombre, tipo, selector, texto))
                    except:
                        pass
            else:
                print("   ❌ No encontró nada")
                
        except Exception as e:
            print(f"\n📊 {nombre}")
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*70)
    print("📋 RESUMEN DE RESULTADOS")
    print("="*70)
    
    if mejores_resultados:
        # Ordenar por cantidad (más es mejor generalmente)
        mejores_resultados.sort(reverse=True)
        
        print(f"\n✓ Se encontraron {len(mejores_resultados)} selectores que funcionan")
        print("\n🏆 MEJORES SELECTORES (ordenados por cantidad):")
        
        for i, (count, nombre, tipo, selector, ejemplo) in enumerate(mejores_resultados[:3], 1):
            print(f"\n{i}. {nombre}")
            print(f"   Elementos: {count}")
            print(f"   Tipo: {tipo}")
            print(f"   Selector: {selector}")
            print(f"   Ejemplo: '{ejemplo[:50]}'")
        
        print("\n" + "="*70)
        print("💡 RECOMENDACIÓN:")
        print("="*70)
        
        mejor = mejores_resultados[0]
        print(f"\nUsa este selector en whatsapp_monitor.py (línea ~225):")
        print("\n```python")
        if mejor[2] == By.CSS_SELECTOR:
            print(f"mensajes = self.driver.find_elements(")
            print(f"    By.CSS_SELECTOR,")
            print(f"    '{mejor[3]}'")
            print(f")")
        else:
            print(f"mensajes = self.driver.find_elements(")
            print(f"    By.XPATH,")
            print(f"    '{mejor[3]}'")
            print(f")")
        print("```")
        
    else:
        print("\n❌ NO se encontró ningún selector que funcione")
        print("\n🔧 SOLUCIONES:")
        print("1. Asegúrate de tener mensajes en el chat 'Prueba partes'")
        print("2. WhatsApp puede haber cambiado su estructura HTML")
        print("3. Intenta actualizar WhatsApp Web")
        
        print("\n📸 Por favor, haz lo siguiente:")
        print("1. En el navegador que acaba de abrir, presiona F12")
        print("2. Haz clic en la flecha del inspector (esquina superior izquierda)")
        print("3. Haz clic en cualquier mensaje del chat")
        print("4. Mira el HTML que se resalta")
        print("5. Copia la estructura HTML y envíamela")
    
    print("\n\n⏸️  Mantendré el navegador abierto por 30 segundos para que inspecciones...")
    print("    Presiona Ctrl+C para cerrar antes")
    
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        print("\n\n🛑 Cerrando...")
    
    driver.quit()
    print("\n✓ Diagnóstico completado")

if __name__ == "__main__":
    try:
        diagnosticar_whatsapp()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
