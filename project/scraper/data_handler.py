import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

def get_sheet(sheet_id):
    # ... (código auxiliar sin cambios) ...
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_script_dir))
    credentials_path = os.path.join(project_root, "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1

def read_existing_links(sheet_id):
    # ... (código sin cambios) ...
    print("--- LEYENDO DATOS EXISTENTES DE GOOGLE SHEETS ---")
    try:
        sheet = get_sheet(sheet_id)
        records = sheet.get_all_records()
        if not records:
            print("La hoja está vacía. No hay enlaces existentes.")
            return set()
        existing_links = {row.get('enlace_principal') for row in records if row.get('enlace_principal')}
        print(f"Se encontraron {len(existing_links)} enlaces existentes en la hoja.")
        return existing_links
    except Exception as e:
        print(f"[ERROR] No se pudo leer la hoja de Google: {e}. Se asumirá que está vacía.")
        return set()

def append_to_google_sheet(data_list, sheet_id):
    if not data_list:
        print("No hay datos nuevos para añadir a Google Sheets.")
        return
    print(f"--- AÑADIENDO {len(data_list)} FILAS NUEVAS A GOOGLE SHEETS ---")
    try:
        sheet = get_sheet(sheet_id)
        header = sheet.row_values(1)
        new_header = ["fuente", "nombre_convocatoria", "puntuacion_relevancia", "justificacion_relevancia", "fecha_inicio", "fecha_fin", "objeto_descripcion", "enlace_principal"]

        # Si la hoja está vacía, creamos los encabezados.
        if not header:
            sheet.append_row(new_header)
            header = new_header # Actualizamos el header que usaremos

        df = pd.DataFrame(data_list)
        rows_to_append = []
        for _, row in df.iterrows():
            # Aseguramos que los datos se añadan en el orden correcto de las columnas
            ordered_row = [row.get(col, "") for col in header]
            rows_to_append.append(ordered_row)

        sheet.append_rows(rows_to_append)
        
        print(f"¡Éxito! Se añadieron {len(data_list)} filas nuevas a la hoja.")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar en Google Sheets: {e}")