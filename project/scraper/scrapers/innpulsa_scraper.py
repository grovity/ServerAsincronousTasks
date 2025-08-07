import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup

URL = "https://www.innpulsacolombia.com/category/proveedores/"

def scrape_innpulsa():
    """
    Usa Selenium para navegar Innpulsa, esperar a que el contenido cargue
    vía JavaScript y navegar la paginación.
    """
    print("Iniciando scraper de Innpulsa...")
    links = []
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)
        
        while True:
            print(f"  Analizando página de listado: {driver.current_url}")
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.jet-posts__item"))
                )
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                article_links = soup.select("div.jet-posts__inner-box h3.entry-title a")
                for link_tag in article_links:
                    if href := link_tag.get('href'):
                        links.append(href)

                next_button = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3) 

            except (NoSuchElementException, TimeoutException):
                print("  -> Fin de la paginación o no se encontró más contenido.")
                break
            
    except Exception as e:
        print(f"[ERROR GRAVE] Ocurrió una excepción con Selenium: {e}")
    finally:
        driver.quit()

    return list(set(links))