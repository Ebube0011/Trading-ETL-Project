import time
from sqlalchemy import create_engine
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def get_src_tables():
    #hook = MsSqlHook(mssql_conn_id='sqlserver')
    sql = """SELECT t.name AS table_name 
    FROM sys.tables
    WHERE t.name IN ('DimProduct', 'DimProductSubCategory', 'DimProductCategory')"""
    df = hook.get_pandas_df(sql)
    tbl_dict = df.to_dict('dict')
    return tbl_dict


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