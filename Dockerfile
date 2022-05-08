FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Dbanks-master

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .