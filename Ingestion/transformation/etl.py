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
            f'SELECT * FROM landing_area."{table_name}"', engine
        )
        logger.info('Table read from the landing_area!!!!')
        return df
    except Exception as e:
        logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        logger.error(f'Unable to read data from landing_area: {e}')


def clean_data(df):
    # data cleaning
    df['op_type'] = df['op_type'].fillna("No operations")
    df['system_name'] = df['system_name'].fillna("No name")
    df['market'] = df['market'].fillna("Unidentified market")
    df['sector'] = df['sector'].fillna("Unidentified sector")
    df['profit'] = df['profit'].fillna(-1)

    return df


def create_schema(df):
    """Build a star schema"""

    dim_operation = df[['op_type']]
    dim_operation = dim_operation.drop_duplicates()
    dim_operation = dim_operation.reset_index(drop=True)
    dim_operation = dim_operation.reset_index(names="op_id")
    dim_operation["op_id"] += 1

    dim_system = df[['system_code', 'system_name']]
    dim_system = dim_system.rename(
        columns={
            'system_code': 'sys_code',
            'system_name': 'sys_name',
        }
    )
    dim_system = dim_system.drop_duplicates()

    
    dim_sector = df[['sector']]
    dim_sector = dim_sector.drop_duplicates()
    dim_sector = dim_sector.reset_index(drop=True)
    dim_sector = dim_sector.reset_index(names="sector_id")
    dim_sector["sector_id"] += 1


    dim_market = df[['market']]
    dim_market = dim_market.drop_duplicates()
    dim_market = dim_market.reset_index(drop=True)
    dim_market = dim_market.reset_index(names="market_id")
    dim_market["market_id"] += 1
    

    dim_date = df[['trade_date']]
    dim_date = dim_date.drop_duplicates()
    dim_date = dim_date.reset_index(drop=True)
    dim_date = dim_date.reset_index(names="date_id")
    dim_date["date_id"] += 1

    fact_table = (
        df.merge(dim_operation, on='op_type')
        .merge(dim_system, left_on="system_code", right_on="sys_code")
        .merge(dim_market, on='market')
        .merge(dim_sector, on='sector')
        .merge(dim_date, on=["trade_date"])[
            [
                'trade_id',
                'trade_identifier',
                'date_id',
                'op_id',
                'sys_code',
                'sector_id',
                'market_id',
                'profit',
            ]
        ]
    )

    fact_table = fact_table.drop_duplicates()

    return {
        "dim_operation": dim_operation.to_dict(orient="dict"),
        "dim_system": dim_system.to_dict(orient="dict"),
        "dim_sector": dim_sector.to_dict(orient="dict"),
        "dim_market": dim_market.to_dict(orient="dict"),
        "dim_date": dim_date.to_dict(orient="dict"),
        "fact_trades": fact_table.to_dict(orient="dict"),
    }


def load_tables_staging(dict, engine):
    """load the tables to the staging schema for visualization"""
    try:
        for df_name, value_dict in dict.items():
            value_df = pd.DataFrame(value_dict)
            logger.info(
                f'Importing {len(value_df)} rows from '
                f'landing_area to staging_area.{df_name}'
            )
            value_df.to_sql(
                df_name,
                engine,
                if_exists='replace',
                index=False,
                schema='staging_area',
            )

            logger.info('!!!!!!!!')
            logger.info(f'Table {df_name} loaded succesfully')

    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to load the data to staging area : {e}")
