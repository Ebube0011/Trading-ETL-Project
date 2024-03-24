FROM python:3

WORKDIR /app

COPY ../Orchestration/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ../Ingestion ./Ingestion
COPY ../Ingestion/main_pipeline.py .