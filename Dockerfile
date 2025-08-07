# Pull official base image
FROM public.ecr.aws/docker/library/python:3.11.4

# Set work directory
WORKDIR /usr/src/app


ARG SECRET_ZOOM
ARG KEY_ZOOM
ARG OPENAI_KEY

# Set environment variables
#ENV AWS_STORAGE_BUCKET_NAME=$AWS_SBN
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_SECRET_ZOOM=$SECRET_ZOOM
ENV API_KEY_ZOOM=$KEY_ZOOM
ENV USER_ZOOM "servidorgenie@gmail.com"
ENV OPENAI_API_KEY=$OPENAI_KEY

ENV EMAIL_ADMIN=$EMAIL_ADMIN
ENV PWSD_ADMIN=$PWSD_ADMIN
ENV USER_ZOOM "servidorgenie@gmail.com"

ENV WEBHOOKCACUMBA "MFo0EhaTiyAExPC2chcssFwFwNunaSFeBqULMx7tW2wPvsHvqEY2dmvMY/0m4VDMK_MeDqZi-BAU9LGA=="
#ENV OPENAI_API_KEY=$OPENAI_KEY

# Install system dependencies
RUN apt-get update && apt-get install -y redis-server

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# Copy the rest of the project
COPY . .

# Expose ports
EXPOSE 8004/tcp
EXPOSE 5556/tcp

# Run the application
CMD ["sh", "-c", "sed -e 's/^bind.*/bind 127.0.0.1/' /etc/redis/redis.conf > redis.conf && mv redis.conf /etc/redis && service redis-server start && sleep 5 && uvicorn project.app:app --host 0.0.0.0 --port 8004 & sleep 5 && celery --broker=redis://localhost:6379/0 flower --port=5556 & sleep 5 && celery -A project.worker worker --loglevel=info"]

