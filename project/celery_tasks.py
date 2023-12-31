from celery import Celery
from time import sleep
from functions import request_zoom,obt_video_evento,upload
import os
# Configuración de Celery
celery = Celery('tasks', broker='redis://localhost:6379/0')

# Definición de la función para la tarea Celery
@celery.task
def transfer(id_reu):
    try:
        print(f"Descargando reunión {id_reu}")
        obt_video_evento(id_reu)
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
    return f"Ejecución finalizada"
