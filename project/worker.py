import os
import time
from celery.result import AsyncResult
from celery import Celery
from time import sleep
from .functions import obt_video_evento,upload,convertir_video_a_mp3,split_and_transcribe,dividir_y_analizar_texto,upload_text,obt_audio_evento,dwl_file_drive
from .grovity_api import ApiClient
import os


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name="check_task")
def check_task(task_uuid):
    try:
        estado = AsyncResult(task_uuid)
    except Exception as e:
        print(e)
    return estado

@celery.task(name="transfer")
def transfer(id_reu):
    try:
        print(f"Descargando reunión video de reunión {id_reu}")
        obt_video_evento(id_reu)
        #convertir_video_a_mp3(id_reu)
        print(f"Cargando reunión {id_reu}")
        upload(id_reu)
        f = open('finished.txt', 'a')
        f.write(f'{id_reu}\n')
        f.close()
        os.remove(f"{id_reu}.mp4")
        api_client = ApiClient("https://api.grovity.co", "")  # Deja el token vacío inicialmente
        api_client.login()
        video_update_url = api_client.get_video_update_url(id_reu)
        print(video_update_url)
        
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
       
        if not obt_audio_evento(id_reu):
            print("Descargando video zoom \n --------------")
            dwl_file_drive(id_reu,"MP4")
            print("Descarga de audio Finalizada \n --------------")
            print("Convirtiendo a audio \n --------------")
            convertir_video_a_mp3(id_reu)
            print("Transcribiendo \n --------------")
            split_and_transcribe(id_reu,".mp3")
            os.remove(f"{id_reu}.MP4")
        else:
            print("Descargando audio de zoom \n --------------")
            obt_audio_evento(id_reu)
            print("Transcribiendo \n --------------")
            split_and_transcribe(id_reu,".m4a")
            os.remove(f"{id_reu}.m4a")

        print("Analizando Transcripción \n --------------")
        dividir_y_analizar_texto(id_reu)
        print("Analisis de Trascripcion Finalizado \n --------------")
        upload_text(id_reu)
        print("Carga de Analisis de Trascripcion Finalizado \n --------------")
        print("Notificando al servidor")
        os.remove(f"{id_reu}.txt")
        os.remove(f"{id_reu}_transcript.txt")
        os.remove(f"{id_reu}.mp3")
        api_client = ApiClient("https://api.grovity.co", "")  # Deja el token vacío inicialmente
        api_client.login()
        video_update_url = api_client.get_transcrip_status(id_reu)
        print(video_update_url)
        
        
        
    except Exception as e:
        f = open('not_finished.txt', 'a')
        f.write(f'{id_reu}\n')
        f.close()
        print(e)
        raise
    return True
