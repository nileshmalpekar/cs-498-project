FROM python:2.7-jessie

RUN apt-get update && apt-get -y upgrade

COPY ./requirements.txt .

RUN pip install -r requirements.txt
