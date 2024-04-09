FROM python:3

WORKDIR /app

COPY ./Orchestration/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./Ingestion ./Ingestion
COPY ./Transformation ./Transformation
COPY ./Serve ./Serve

COPY ./Ingestion/main_pipeline.py .
COPY ./Transformation/Transform_data.py .
COPY ./Serve/main_serve.py .
