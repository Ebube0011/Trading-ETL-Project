import time
from datetime import datetime
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.hooks.base_hook import BaseHook
import pandas as pd
from sqlalchemy import create_engine

# Extract tasks
@task()
def get_src_tables():
    hook = MsSqlHook(mssql_conn_id='sqlserver')
    sql = """SELECT t.name AS table_name 
    FROM sys.tables
    WHERE t.name IN ('DimProduct', 'DimProductSubCategory', 'DimProductCategory')"""
    df = hook.get_pandas_df(sql)
    tbl_dict = df.to_dict('dict')
    return tbl_dict

@task()
def load_src_data(tbl_dict: dict):
    conn = BaseHook.get_connection('postgres')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    all_tbl_name = []
    start_time = time.time()
    for k, v in tbl_dict['table_name'].items():
        all_tbl_name.append(v)
        rows_imported = 8
        sql = f'SELECT * FROM {v}'
        hook = MsSqlHook(mssql_conn_id='sqlserver')
        df = hook.get_pandas_df(sql)
        print(f'Importing rows {rows_imported} to {rows_imported + len(df)}... for table {v}')
        df.to_sql(f'src_{v}', engine, if_exists= 'replace', index=False)
        rows_imported += len(df)
        print(f'Done. {str(round(time.time() - start_time, 2))} total seconds elapsed')
    print ('Data Imported successfully')
    return all_tbl_name

# transform tasks
@task()
def transform_srcProduct():
    conn = BaseHook.get_connection('postgres')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df = pd.read_sql_query('SELECT * FROM public."src_DimProduct"', engine)
    # drop columns
    revised = df[['col1', 'col2', 'etc']]
    # replace nulls
    revised ['Size'].fillna('NA', inplace=True)
    # rename columns
    revised = revised.rename(columns={'EnglishDescription' : 'Description',
                                      'EnglishProductName' : 'ProductName'})
    
    # store result
    revised.to_sql('stg_DimProduct', engine, if_exists='replace', index=False)
    return {'table(s) processed' : 'Data imported successful'}

@task()
def transform_srcProductCategory():
    conn = BaseHook.get_connection('postgres')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df = pd.read_sql_query('SELECT * FROM public."src_DimProduct"', engine)
    # drop columns
    revised = df[['col1', 'col2', 'etc']]
    # replace nulls
    revised ['Size'].fillna('NA', inplace=True)
    # rename columns
    revised = revised.rename(columns={'EnglishDescription' : 'Description',
                                      'EnglishProductName' : 'ProductName'})
    
    # store result
    revised.to_sql('sth_DimProductCategory', engine, if_exists='replace', index=False)
    return {'table(s) processed' : 'Data imported successful'}

@task()
def transform_srcProductSubCategory():
    conn = BaseHook.get_connection('postgres')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df = pd.read_sql_query('SELECT * FROM public."src_DimProduct"', engine)
    # drop columns
    revised = df[['col1', 'col2', 'etc']]
    # replace nulls
    revised ['Size'].fillna('NA', inplace=True)
    # rename columns
    revised = revised.rename(columns={'EnglishDescription' : 'Description',
                                      'EnglishProductName' : 'ProductName'})
    
    # store result
    revised.to_sql('stg_DimProductSubCategory', engine, if_exists='replace', index=False)
    return {'table(s) processed' : 'Data imported successful'}

# load
@task()
def prdProduct_Model():
    conn = BaseHook.get_connection('postgres')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    pc = pd.read_sql_query('SELECT * FROM public."stg_DimProductCategory"', engine)
    p = pd.read_sql_query('SELECT * FROM public."stg_DimProduct"', engine)
    p['ProductSubCategoryKey'] = p.ProductSubCategoryKey.astype(float)
    p['ProductSubCategoryKey'] = p.ProductSubCategoryKey.astype(int)
    ps = pd.read_sql_query('SELECT * FROM public."stg_DimProductSubCategory"', engine)
    # join all three
    merged = p.merge(ps, on='ProductSubCategoryKey').merge(pc, on='ProductCategoryKey')
    merged.to_sql('prd_DimProductCategory', engine, if_exists='replace', index=False)
    return {'table(s) processed' : 'Data imported successful'}

# Start task group
with DAG(dag_id='product_etl_dag',
         schedule_interval= '0 9 * * *',
         start_date=datetime(2022, 3, 1),
         catchup=False,
         tags=['product_model']) as dag:
    
    with TaskGroup('extract_dimProducts_load', 
                   tooltip='Extract and load source data') as extract_load_src:
        src_product_tbls = get_src_tables()
        load_dimProducts = load_src_data(src_product_tbls)
        # define order
        src_product_tbls >> load_dimProducts
        
    with TaskGroup('transform_src_Products', 
                   tooltip='Transform and stage data') as transform_src_product:
        transform_srcProduct = transform_srcProduct()
        transform_srcProductSubCategory = transform_srcProductSubCategory()
        transform_srcProductCategory = transform_srcProductCategory()
        # define task order
        [transform_src_product, transform_srcProductSubCategory, transform_srcProductCategory]
        
    with TaskGroup('load_product_model', 
                   tooltip='Final Product model') as load_product_model:
        prd_Product_model = prdProduct_Model()
        # define task order
        prd_Product_model

    extract_load_src >> transform_src_product >> load_product_model

