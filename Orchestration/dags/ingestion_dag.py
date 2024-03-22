from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
#from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from Ingestion.main_pipeline import main_etl

#defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Ebube',
    'start_date': days_ago(0),
    #'end_date': datetime(),
    #'depends_on_past': False,
    'email': ['ezenwajiebube@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='Data _Ingestion',
    default_args=default_args,
    description='ETL from application database into Data Warehouse',
    schedule_interval='@daily'
    #schedule_interval='@once', # @hourly, @daily, @weekly, @monthly, @yearly	
)

# define the tasks
# define the first task named extract
extract = PythonOperator(
    task_id= 'ETL',
    python_callable= main_etl,
    dag= dag
)
# define the second task named transform
#transform = PythonOperator(
#    task_id= 'Transform and model the data',
#    python_callable= ingestion_dag.transform(),
#    dag= dag
#)
# define the third task named load
#load = PythonOperator(
#    task_id= 'Load the data into data warehouse',
#    python_callable= ingestion_dag.load(),
#    dag= dag
#)

# task pipeline
extract
