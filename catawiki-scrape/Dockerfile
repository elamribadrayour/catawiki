FROM python:3.12.4-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /code/job /code/data
WORKDIR /code/job

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/job/
RUN poetry install --without ci --no-root

COPY src/job /code/job
