import requests
from bs4 import BeautifulSoup
import time
import random
import json

# 1. Configuración Ética Obligatoria
USER_AGENT = "MonitorDesinformacionBot/1.0 (+felipe.estudiante@universidad.edu.pe)"
HEADERS = {"User-Agent": USER_AGENT}
BASE_URL = "https://medlineplus.gov/spanish/healthtopics.html"

def extraer_detalle_medline(url_detalle):
    """Entra a un artículo específico de MedlinePlus y extrae su contenido."""
    try:
        if not url_detalle.startswith("http"):
            url_full = "https://medlineplus.gov" + url_detalle
        else:
            url_full = url_detalle

        response = requests.get(url_full, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Selectores adaptados a la enciclopedia/temas de MedlinePlus
        titulo = soup.find('h1').text.strip() if soup.find('h1') else "Sin título"
        
        # Extraemos el resumen del tema de salud
        resumen_div = soup.find('div', id='topic-summary')
        if resumen_div:
            texto_principal = resumen_div.text.strip()
        else:
            # Respuesto si no encuentra el div específico
            parrafos = soup.find_all('p')
            texto_principal = " ".join([p.text.strip() for p in parrafos if len(p.text.strip()) > 20])

        enlaces = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]

        return {
            "titulo": titulo,
            "url": url_full,
            "autor": "MedlinePlus Oficial",
            "fecha": "Institucional / Actualizado", 
            "texto_principal": texto_principal,
            "enlaces_externos": len(enlaces),
            "referencias": list(set(enlaces))
        }
    except Exception as e:
        print(f"⚠️ Error al extraer detalle en {url_detalle}: {e}")
        return None

def ejecutar_scraper_medline():
    """Función principal que lee el listado y coordina la extracción."""
    print("🚀 [Felipe Bot] Iniciando scraping en MedlinePlus...")
    response = requests.get(BASE_URL, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ No se pudo acceder al listado principal. Código: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links_articulos = []
    
    for a in soup.find_all('a', href=True):
        # Capturamos enlaces válidos a temas específicos en español
        if "/spanish/" in a['href'] and a['href'].endswith('.html'):
            if "healthtopics" not in a['href'] and "ayuda" not in a['href']:
                links_articulos.append(a['href'])
    
    links_articulos = list(set(links_articulos))
    print(f"➔ Se encontraron {len(links_articulos)} temas de salud en el listado.")

    datos_recolectados = []
    
    # Extraemos solo 3 para verificar que el JSON se cree bien sin demoras
    for link in links_articulos[:3]: 
        print(f"🕵️ Analizando artículo: {link}")
        info_articulo = extraer_detalle_medline(link)
        
        if info_articulo:
            datos_recolectados.append(info_articulo)
        
        tiempo_espera = random.uniform(2.0, 4.0)
        time.sleep(tiempo_espera)

    with open("datos_raw.json", "w", encoding="utf-8") as f:
        json.dump(datos_recolectados, f, ensure_ascii=False, indent=4)
    
    print("✅ ¡Éxito! Archivo 'datos_raw.json' generado correctamente.")

if __name__ == "__main__":
    ejecutar_scraper_medline()