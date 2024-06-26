# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
