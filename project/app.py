from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from celery import Celery
from pydantic import BaseModel
from .worker import create_task,transfer,transcribe,check_task,enviar_sms,run_scraper

app = FastAPI()
""" app.mount("/static", StaticFiles(directory="project/static"), name="static")
templates = Jinja2Templates(directory="templates") """




class ScrapePayload(BaseModel):
    sheet_id: str
    descripcion_empresa: str

@app.get("/")
async def health_check():
    return {"status": "OK"}


@app.post("/scrape", status_code=201, summary="Iniciar tarea de Scraping de Convocatorias")
def start_scrape_task(payload: ScrapePayload):
    """
    Recibe un ID de Google Sheet y una descripción de la empresa para iniciar
    el scraping y análisis de relevancia en segundo plano.
    """
    print(f"[API] Petición recibida para la hoja '{payload.sheet_id}'")
    print(f"[API] Usando descripción de empresa: '{payload.descripcion_empresa}'")
    
    # Ahora pasamos ambos argumentos a la tarea de Celery
    task = run_scraper.delay(payload.sheet_id, payload.descripcion_empresa)
    
    return JSONResponse({"task_id": task.id})

# --- Tus endpoints existentes (sin cambios) ---
@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    # ... tu código ...
    return JSONResponse({"task_id": task.id})

# ... (El resto de tus endpoints: /transfer, /transcribe, /enviar_sms, /tasks/{task_id}) ...

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.post("/transfer", status_code=201)
def transfer_vid(payload = Body(...)):
    video_id = payload["id"]
    task = transfer.delay(video_id)  # Enqueue the task asynchronously
    return {"task_id": task.id}

@app.post("/transcribe", status_code=201)
def transcribe_vid(payload = Body(...)):
    video_id = payload["id"]
    task = transcribe.delay(video_id)  # Enqueue the task asynchronously
    return {"task_id": task.id}

@app.post("/enviar_sms", status_code=201)
def enviar_sms_request(payload = Body(...)):
    mensaje = payload["body"]
    telefono = payload["recipient"]
    task = enviar_sms.delay(mensaje, telefono)  # Enqueue the task asynchronously
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = check_task(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
