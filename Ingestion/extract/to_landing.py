import logging
import pandas as pd
from datetime import date

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def read_source_table(engine, table_name):
    """read data from the application dastabase table"""
    if (table_name == 'Trading_operation'):
        format = "%Y-%m-%d"
        #today = date.today()
        today = date(year=2020, month=1, day=20)
        today = today.strftime(format)
        query = f""" SELECT *
                FROM {table_name}
                WHERE trade_date IS '{str(today)}'"""
    else:
        query = f"""SELECT * 
                FROM {table_name}"""
    try:
        df = pd.read_sql_query(query, engine)
        logger.info('Table read from the source system!!!!')
        return df
    except Exception as e:
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error(f'Unable to read data from source system: {e}')


def load_table_to_landing(df, engine, table_name):
    # load the csv file to the schema
    try:
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False,
            schema='landing_area',
        )
        logger.info("Table loaded to the landing area!!!")
    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to load the data to landing area : {e}")
