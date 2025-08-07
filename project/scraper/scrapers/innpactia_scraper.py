import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://web.innpactia.com/#/public/convocatorias"

def scrape_innpactia():
    print("Iniciando scraper de Innpactia...")
    links = set()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        time.sleep(10) # Espera inicial generosa

        page_number = 1
        while True:
            print(f"  Analizando página {page_number} de Innpactia...")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            opportunity_links = soup.select('a[href*="/public/convocatorias/detalles/"]') or \
                                soup.select('a[href*="/public/vehiculo/detalles/"]')
            
            if not opportunity_links and page_number == 1:
                time.sleep(10) # Si en la primera página no hay nada, esperamos un poco más
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                opportunity_links = soup.select('a[href*="/public/convocatorias/detalles/"]') or \
                                    soup.select('a[href*="/public/vehiculo/detalles/"]')

            new_links_found = 0
            for link_tag in opportunity_links:
                if href := link_tag.get('href'):
                    full_link = urljoin("https://web.innpactia.com/", href)
                    if full_link not in links:
                        links.add(full_link)
                        new_links_found += 1
            
            print(f"  -> Se encontraron {new_links_found} nuevos enlaces.")

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button.mat-paginator-navigation-next")
                if not next_button.is_enabled(): break
                driver.execute_script("arguments[0].click();", next_button)
                page_number += 1
                time.sleep(4)
            except Exception:
                break
            if page_number > 1:  # Limitar a 10 páginas para evitar loops infinitos
                print(f"  -> Se procesaron {page_number} páginas de Innpactia.")
                break
        print(f"Total de enlaces únicos extraídos de Innpactia: {len(links)}")
    except Exception as e:
        print(f"[ERROR GRAVE] Ocurrió una excepción con Innpactia: {e}")
    finally:
        driver.quit()

    return list(links)