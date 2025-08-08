import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlunsplit
import re

# La URL base para construir los enlaces de las convocatorias.
BASE_CONTRATACION_URL = "https://rutanmedellin.org/contratacion/"
START_URL = "https://rutanmedellin.org/contratacion/"

def scrape_rutan():
    """
    Navega por Ruta N, extrae los enlaces y los construye a partir de la URL
    base de la sección de contratación para asegurar el formato correcto.
    """
    print("--- Iniciando scraper de Ruta N (con URL base corregida) ---")
    links = []
    current_page_url = START_URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    while current_page_url:
        print(f"Analizando página de listado: {current_page_url}")
        try:
            response = requests.get(current_page_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            card_links = soup.select(".dynamic-page__card-button a.btn-dark")
            print(f"  -> Se encontraron {len(card_links)} enlaces en esta página.")
            
            for link_tag in card_links:
                href = link_tag.get('href')
                if href:
                    # 1. Construir la URL completa usando la base de /contratacion/
                    # Esto soluciona el problema si los href son relativos (ej: "convocatoria-cp-001-2025")
                    initial_link = urljoin(BASE_CONTRATACION_URL, href)
                    
                    # 2. Descomponer para limpiar y formatear con el parámetro de idioma
                    parts = list(urlsplit(initial_link))
                    parts[3] = "hsLang=es"  # Forzar el parámetro de consulta
                    
                    # 3. Reconstruir la URL final y añadirla a la lista
                    final_link = urlunsplit(parts)
                    links.append(final_link)

            # Lógica de paginación
            next_button_tag = soup.find('a', class_='pagination__link', text=re.compile(r'\s*Siguiente\s*'))
            if next_button_tag and next_button_tag.get('href'):
                # Para la paginación, usamos la URL base del dominio
                current_page_url = urljoin("https://rutanmedellin.org/", next_button_tag['href'])
            else:
                print("  -> No se encontró botón 'Siguiente'. Fin de la paginación.")
                current_page_url = None
        except Exception as e:
            print(f"[ERROR] Ocurrió una excepción: {e}")
            break
            
    unique_links = list(set(links))
    print(f"\nTotal de enlaces únicos extraídos de Ruta N: {len(unique_links)}")
    return unique_links

# --- Bloque de Prueba ---
if __name__ == "__main__":
    extracted_links = scrape_rutan()
    
    if extracted_links:
        print("\n--- ¡ÉXITO! Enlaces corregidos de Ruta N: ---")
        for link in extracted_links:
            print(link)
    else:
        print("\n--- FALLO: No se encontró ningún enlace. ---")