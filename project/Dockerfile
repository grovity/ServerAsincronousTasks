# pull official base image
FROM python:3.11.2-slim-buster

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

# copy project
COPY . .
