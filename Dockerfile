# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /music_catalog
COPY requirements.txt /music_catalog/
RUN pip install -r requirements.txt
COPY . /music_catalog/
