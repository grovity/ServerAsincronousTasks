# pull official base image
FROM public.ecr.aws/docker/library/python:3.11.4

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_SECRET_ZOOM "p2juMvG4ifA9x8StadY1lixePaH7Z7nMQuNy"
ENV API_KEY_ZOOM "UEd0Za_eTvq2AC1fC5E-dQ"
ENV USER_ZOOM "servidorgenie@gmail.com"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8004/tcp
EXPOSE 5555/tcp

CMD ["sh", "-c", "if [ \"$SERVICE_TYPE\" = \"web\" ]; then uvicorn project.main:app --host 0.0.0.0 --port 8004; elif [ \"$SERVICE_TYPE\" = \"worker\" ]; then celery -A worker.celery worker --loglevel=info --logfile=logs/celery.log; elif [ \"$SERVICE_TYPE\" = \"dashboard\" ]; then celery --broker=redis://redis:6379/0 flower --port=5555; else echo \"Invalid service type\"; fi"]
