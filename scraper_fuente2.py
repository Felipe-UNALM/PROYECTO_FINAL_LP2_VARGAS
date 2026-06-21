from bs4 import BeautifulSoup
import json
import os

def ejecutar_scraper_meneame_local():
    print("🚀 [Felipe Bot] Iniciando scraping local y seguro de Menéame (Modo Resiliente)...")
    
    archivo_html = "fuente2_meneame.html"
    
    if not os.path.exists(archivo_html):
        print(f"❌ Error: No se encuentra el archivo simulado {archivo_html}")
        return

    # Leemos el HTML local que guardamos
    with open(archivo_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    datos_meneame = []

    # Extraemos usando exactamente las mismas etiquetas que usaríamos en la web real
    articulos = soup.find_all('div', class_='news-summary')
    print(f"➔ Se encontraron {len(articulos)} publicaciones simuladas para el análisis de riesgo.")

    for art in articulos:
        header = art.find('h2')
        if not header:
            continue
        a_tag = header.find('a')
        titulo = a_tag.text.strip() if a_tag else "Sin título"
        url_noticia = a_tag['href'] if a_tag else "Sin URL"

        noticia_contenido = art.find('div', class_='news-content')
        texto_principal = noticia_contenido.text.strip() if noticia_contenido else "Sin descripción"

        comentarios_div = art.find('a', class_='comments')
        num_comentarios = comentarios_div.text.replace("comentarios", "").strip() if comentarios_div else "0"

        datos_meneame.append({
            "titulo": titulo,
            "url": url_noticia,
            "autor": "Usuario Menéame Anónimo",  # Factor de riesgo IRD
            "fecha": "Reciente / Post Social",
            "texto_principal": texto_principal,
            "enlaces_externos": 1,
            "referencias": [url_noticia],
            "metricas_sociales": {
                "comentarios": num_comentarios  # Alto número = Mayor polémica/riesgo
            }
        })

    # Guardamos los resultados
    with open("datos_raw_meneame.json", "w", encoding="utf-8") as f:
        json.dump(datos_meneame, f, ensure_ascii=False, indent=4)

    print("✅ ¡Éxito! Archivo 'datos_raw_meneame.json' generado correctamente.")

if __name__ == "__main__":
    ejecutar_scraper_meneame_local()