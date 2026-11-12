FROM python:3.11-slim

WORKDIR /app

COPY rag /app/rag
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r /app/backend/requirements.txt

COPY backend/app /app/backend/app
COPY backend/alembic /app/backend/alembic
COPY backend/alembic.ini /app/backend/alembic.ini

WORKDIR /app/backend

