import os
from datetime import timedelta
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
import pandas as pd
from Ingestion.storage.connection import close_conn, create_db_conn #create_conn
from Ingestion.extract.to_landing import load_table_to_landing
from Ingestion.transformation.etl import (
    clean_data,
    create_schema,
    load_tables_staging,
    read_table,
)



# Extract tasks
@task()
def etl_to_landing():

    engine = create_db_conn()

    file_path = os.getenv('FILE_PATH')
    table_name = os.getenv('TABLE_NAME')

    df = pd.read_csv(file_path)
    load_table_to_landing(df, engine, table_name)

    close_conn(engine)
    return {'table(s) loaded' : 'Data imported successfully'}

# Transformation tasks
@task()
def transform_data():

    engine = create_db_conn()

    table_name = os.getenv('TABLE_NAME')
    df = read_table(engine, table_name)
    df_clean = clean_data(df)
    dict_tables = create_schema(df_clean)

    close_conn(engine)
    return dict_tables


# Loading tasks
@task()
def load_data(dict_tables: dict):

    engine = create_db_conn()

    load_tables_staging(dict_tables, engine)

    close_conn(engine)
    return {'table(s) loaded' : 'Data imported successfully'}

# Start task group
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
with DAG(dag_id='testing_etl_dag',
         default_args=default_args,
         description='ETL from raw data into Data Warehouse',
         schedule_interval= '@daily',
         catchup=False) as dag:
    
    with TaskGroup('extract_source_data', 
                   tooltip='Extract and load source data to landing') as extract_to_landing:
        extract = etl_to_landing()
        # define task order
        extract
    
    with TaskGroup('transform_dataset', 
                   tooltip='Transform and stage data') as transform_to_staging:
        transformed_dataset = transform_data()
        load_dataset = load_data(transformed_dataset)
        # define task order
        transformed_dataset >> load_dataset

    # define task group order
    extract_to_landing >> transform_to_staging
