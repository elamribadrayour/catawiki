FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code/app /code/data
WORKDIR /code/app

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/app/
RUN poetry install --without ci --no-root

COPY src/app /code/app
