FROM python:3.10-slim-bullseye

#Comparison for python dist https://pythonspeed.com/articles/base-image-python-docker-images/

#Copy dependencies
COPY app app
COPY requirements.txt /app/requirements.txt
COPY logging app/logging

RUN apt-get update\
&& apt-get -y install libpq-dev gcc \
&& apt install libpq-dev python3-dev -y

RUN pip install --upgrade pip

WORKDIR /app

RUN pip install -r requirements.txt

