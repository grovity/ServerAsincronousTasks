import time
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

# Pega aquí tu clave secreta de API de OpenAI (ChatGPT)
OPENAI_API_KEY = "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" 
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_text_from_url(url):
    print(f"  -> Extrayendo texto de: {url}")
    text_content = ""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5) 
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if soup.body:
            text_content = " ".join(soup.body.stripped_strings)
        else:
            text_content = " ".join(soup.stripped_strings)
    except Exception as e:
        print(f"  -> [ERROR] No se pudo obtener el contenido con Selenium: {e}")
    finally:
        driver.quit()
    return text_content

def extract_details_with_ai(text_content: str, company_description: str):
    if not text_content or not OPENAI_API_KEY or OPENAI_API_KEY == "AQUI_VA_TU_CLAVE_DE_OPENAI":
        return None

    prompt = f"""
    Eres un analista de negocios experto. Tu misión es analizar el texto de una convocatoria pública y determinar su relevancia para una empresa específica.

    **Descripción de mi empresa:**
    "{company_description}"

    **Texto de la convocatoria a analizar:**
    ---
    {text_content[:8000]}
    ---

    **Tu tarea:**
    Extrae la siguiente información y responde únicamente con un JSON.
    - nombre_convocatoria: El título oficial.
    - fecha_inicio: La fecha de publicación, apertura o inicio.
    - fecha_fin: La fecha de cierre o vencimiento.
    - objeto_descripcion: Un resumen conciso de 2-3 líneas sobre el propósito de la convocatoria.
    - puntuacion_relevancia: Una puntuación de 1 a 10, donde 10 es una "joya" (perfectamente alineada con mi empresa) y 1 es irrelevante. Basa tu puntuación en qué tan bien el objeto de la convocatoria coincide con la descripción de mi empresa.
    - justificacion_relevancia: Una frase corta explicando por qué diste esa puntuación (ej: "Se alinea perfectamente con nuestros servicios de software" o "Baja relevancia, enfocada en construcción").

    **Formato de salida JSON requerido:**
    {{
      "nombre_convocatoria": "string",
      "fecha_inicio": "string",
      "fecha_fin": "string",
      "objeto_descripcion": "string",
      "puntuacion_relevancia": "integer",
      "justificacion_relevancia": "string"
    }}
    """
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Eres un asistente experto en analizar y calificar la relevancia de convocatorias, y solo respondes con formato JSON."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=data, timeout=90)
        response.raise_for_status()
        result_text = response.json()['choices'][0]['message']['content']
        json_str = result_text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_str)
    except Exception as e:
        print(f"  -> [ERROR IA] No se pudo procesar la respuesta de OpenAI: {e}")
        return None

# --- ▼▼▼ FUNCIÓN ORQUESTADORA ACTUALIZADA ▼▼▼ ---
def process_url_with_ai(url: str, company_description: str): # Ahora acepta el nuevo parámetro
    page_text = get_text_from_url(url)
    if not page_text:
        return None
    # Pasa la descripción de la empresa a la función de la IA
    details = extract_details_with_ai(page_text, company_description)
    return details