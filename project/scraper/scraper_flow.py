# Importamos las nuevas funciones de data_handler
from .data_handler import read_existing_links, append_to_google_sheet
from .nlp_processor import process_url_with_ai
from .scrapers.innpactia_scraper import scrape_innpactia
from .scrapers.innpulsa_scraper import scrape_innpulsa
from .scrapers.rutan_scraper import scrape_rutan


COMPANY_DESCRIPTION = "Somos una consultora de desarrollo de software especializada en inteligencia artificial y análisis de datos para el sector financiero."

def run_full_scrape(sheet_id: str, descripcion_empresa: str): # Acepta el nuevo parámetro
    """
    Scrapea, compara datos, y procesa solo lo nuevo,
    pasando la descripción de la empresa a la IA para el análisis de relevancia.
    """
    print(f"--- INICIANDO SCRAPING CON DESCRIPCIÓN: '{descripcion_empresa[:50]}...' ---")
    
    existing_links = read_existing_links(sheet_id)
    
    # ... (la lógica de scraping para obtener los enlaces no cambia) ...
    rutan_links = scrape_rutan()
    innpulsa_links = scrape_innpulsa()
    innpactia_links = scrape_innpactia()
    all_scraped_links = set(rutan_links + innpulsa_links + innpactia_links)
    new_links_to_process = all_scraped_links - existing_links

    if not new_links_to_process:
        print("\n--- No se encontraron convocatorias nuevas. Proceso finalizado. ---")
        return

    new_data = []
    print("\n--- FASE 2: Extrayendo y analizando detalles con IA ---")
    for link in new_links_to_process:
        print(f"\nProcesando nuevo enlace: {link}")
        # Pasamos la descripción dinámica (que viene como parámetro) a la función de IA
        details = process_url_with_ai(link, descripcion_empresa)
        if details:
            # ... (el resto de la lógica no cambia) ...
            if 'rutanmedellin.org' in link: details['fuente'] = 'Ruta N'
            elif 'innpulsacolombia.com' in link: details['fuente'] = 'Innpulsa'
            elif 'innpactia.com' in link: details['fuente'] = 'Innpactia'
            details['enlace_principal'] = link
            new_data.append(details)
            print(f"  -> ¡Datos y relevancia extraídos por IA!: {details.get('nombre_convocatoria')}")

    if new_data:
        print("\n--- FASE 3: Añadiendo nuevos datos a Google Sheets ---")
        append_to_google_sheet(new_data, sheet_id)
    else:
        print("\n[FIN] Aunque se encontraron enlaces nuevos, no se pudo extraer información para guardar.")