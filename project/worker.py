import os
import time

from celery import Celery
from time import time
from .functions import obt_video_evento,upload
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
    start_time = time()
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

    end_time = time()
    duration = end_time - start_time
    return True