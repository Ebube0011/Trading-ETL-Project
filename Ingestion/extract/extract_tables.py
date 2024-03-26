import time
import logging
import pandas as pd
from Ingestion.extract.to_landing import load_table_to_landing, read_source_table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def get_src_tables(engine):
    
    query = """SELECT t.name AS table_name 
            FROM sys.tables t
            WHERE t.name IN ('DimProduct', 'DimProductSubCategory', 'DimProductCategory')"""
    try:
        df = pd.read_sql_query(query, engine)
        tbl_dict = df.to_dict('dict')
        logger.info('Table names read from the source system!!!!')
        return tbl_dict
    except Exception as e:
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error(f'Unable to get tables from source system: {e}')


def load_src_data(engine, tbl_dict: dict):
    
    start_time = time.time()
    for k, v in tbl_dict['table_name'].items():
        df = read_source_table(engine, v)
        print(f'Importing rows 0 to {len(df)}... for table {v}')
        load_table_to_landing(df, engine, f'src_{v}')
        logger.info('Table read from the source system!!!!')
        logger.info(f'{str(round(time.time() - start_time, 2))} total seconds elapsed')
    print ('Data Imported successfully')