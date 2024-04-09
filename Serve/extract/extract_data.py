import logging

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def read_table(engine, table_name):
    """read data from the landing schema"""
    try:
        df = pd.read_sql_query(
            f'SELECT * FROM {table_name}', engine
        )
        logger.info('Table read from the Data Warehouse view !!!!')
        return df
    except Exception as e:
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error(f'Unable to read data from Data Warehouse : {e}')