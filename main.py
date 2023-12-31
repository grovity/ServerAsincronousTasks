from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from celery import Celery
from pydantic import BaseModel
from project.worker import create_task,transfer,transcribe,check_task,enviar_sms

app = FastAPI()
""" app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") """


@app.get("/")
async def get_status():
    return {"status": "OK"}


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
    print(task_result)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
