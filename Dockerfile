# Pull official base image
FROM public.ecr.aws/docker/library/python:3.11.4

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_SECRET_ZOOM "p2juMvG4ifA9x8StadY1lixePaH7Z7nMQuNy"
ENV API_KEY_ZOOM "UEd0Za_eTvq2AC1fC5E-dQ"
ENV USER_ZOOM "servidorgenie@gmail.com"

# Install system dependencies
RUN apt-get update && apt-get install -y redis-server

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose ports
EXPOSE 8004/tcp
EXPOSE 5556/tcp

# Run the application
CMD ["sh", "-c", "service redis-server start && sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8004 & sleep 5 && celery --broker=redis://localhost:6379/0 flower --port=5556 & sleep 5 && celery -A project.worker worker --loglevel=info"]
