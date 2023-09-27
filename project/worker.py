import os
import time

from celery import Celery
from time import sleep
from .functions import obt_video_evento,upload,convertir_video_a_mp3,split_and_transcribe,dividir_y_analizar_texto,upload_text
import os


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="transfer")
def transfer(id_reu):
    try:
        print(f"Descargando reunión {id_reu}")
        obt_video_evento(id_reu)
        print("Conversión a Audio")
        convertir_video_a_mp3(id_reu)
        print(f"Cargando reunión {id_reu}")
        upload(id_reu)
        f = open('finished.txt', 'a')
        f.write(f'{id_reu}\n')
        f.close()
        os.remove(f"{id_reu}.mp4")
        
    except Exception as e:
        f = open('not_finished.txt', 'a')
        f.write(f'{id_reu}\n')
        f.close()
        print(e)
        raise

    
    return True


@celery.task(name="transcribe")
def transcribe(id_reu):
    try:
        split_and_transcribe(id_reu)
        print("Trasncripcion Finalizada")
        dividir_y_analizar_texto(id_reu)
        print("Analisis de Trascripcion Finalizado")
        upload_text(id_reu)
        print("Carga de Analisis de Trascripcion Finalizado")
        os.remove(f"{id_reu}_transcript_analized.txt")
        os.remove(f"{id_reu}_transcript.txt")
        os.remove(f"{id_reu}.mp3")
        
    except Exception as e:
        f = open('not_finished.txt', 'a')
        f.write(f'{id_reu}\n')
        f.close()
        print(e)
        raise
    return True
