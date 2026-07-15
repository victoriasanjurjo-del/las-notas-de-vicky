import feedparser # type: ignore
import json
import urllib.parse
import os
from datetime import datetime
from difflib import SequenceMatcher

def son_similares(titulo1, titulo2, umbral=0.55):
    """Compara dos textos. Si la similitud supera el umbral, devuelve True."""
    return SequenceMatcher(None, titulo1.lower(), titulo2.lower()).ratio() > umbral

def obtener_noticias_economia():
    # 1. Definimos la carpeta y el nombre del archivo con la fecha de hoy
    carpeta_destino = "economia-argentina"
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"{fecha_hoy}.json"
    
    # Nos aseguramos de que la carpeta exista
    os.makedirs(carpeta_destino, exist_ok=True)
    
    # Armamos la ruta completa (ej. economia-argentina/2026-07-14.json)
    ruta_completa = os.path.join(carpeta_destino, nombre_archivo)

    # 2. Búsqueda y filtrado: priorizamos economía, alejamos política y elecciones
    query = 'economía argentina -"política" -"elecciones" -"congreso" -"interna" -"corrupción"'
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote_plus(query)}&hl=es-419&gl=AR&ceid=AR:es-419"
    
    feed = feedparser.parse(url)
    noticias_seleccionadas = []
    
    for entry in feed.entries:
        if len(noticias_seleccionadas) >= 10:
            break
            
        titulo_bruto = entry.title
        titulo_limpio = titulo_bruto.rsplit(" - ", 1)[0] if " - " in titulo_bruto else titulo_bruto
            
        es_repetida = False
        for noticia in noticias_seleccionadas:
            if son_similares(titulo_limpio, noticia["Título"]):
                es_repetida = True
                break
                
        if not es_repetida:
            fuente = entry.source.title if hasattr(entry, 'source') else "Desconocida"
            noticias_seleccionadas.append({
                "Título": titulo_limpio,
                "Fuente": fuente,
                "Link": entry.link
            })
    
    # 3. Guardamos el archivo
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(noticias_seleccionadas, f, ensure_ascii=False, indent=4)
        
    print(f"¡Listo! Archivo de economía generado en: {ruta_completa}")

if __name__ == "__main__":
    obtener_noticias_economia()