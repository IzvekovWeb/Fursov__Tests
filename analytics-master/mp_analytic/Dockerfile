FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend/
EXPOSE 8000
RUN python manage.py makemigrations
RUN python manage.py migrate
