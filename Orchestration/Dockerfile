FROM apache/airflow:2.7.3

COPY Orchestration/requirements.txt ./

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}"

RUN pip install --no-cache-dir -r requirements.txt