from fastapi import FastAPI
from celery import Celery
import importlib
import sys
import os
module = importlib.import_module('functions')
module.run()
# add your path to the sys path
sys.path.append(os.getcwd())

app = FastAPI()

celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/transfer/{video_id}")
async def transfer_vid(video_id):
    try:
        transfer_status = transfer(video_id)
        return {"video_id": "Convertido"}
    except Exception as e:
        return {"video_id": "Error"}

@app.get("/save/{audio_path}")
async def speech(audio_path):
    text = speech_to_text(audio_path)
    return {"item_id": "Convertido"}

@app.get("/interpret/{text_path}")
async def interpret(text_path):
    resume = text_to_ia(text_path)
    return {"item_id": "Convertido"}

@celery.task
def divide(x, y):
    import time
    time.sleep(10)
    return x / y
