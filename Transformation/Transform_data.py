import os
import psycopg2
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def create_logic_views(cursor):
    """
    Parameters
    ----------
    cursor : database cursor object
    
    DESCRIPTION: executes queries in data warehouse to store logic in views

    Returns
    -------
    None.

    """
    
    positive_trades_sql = """ 
        CREATE OR REPLACE VIEW positive_trades AS
        SELECT sys_code, COUNT(profit)
        FROM staging_area."fact_trades"
        WHERE profit > 0
        GROUP BY sys_code;"""
    negative_trades_sql = """ 
        CREATE OR REPLACE VIEW negative_trades AS
        SELECT sys_code, COUNT(profit)
        FROM staging_area."fact_trades"
        WHERE profit < 0
        GROUP BY sys_code;"""
    winning_trades_sql = """
        CREATE OR REPLACE VIEW winning_trades AS
        SELECT sys_code, SUM(profit)
        FROM staging_area."fact_trades"
        WHERE profit > 0
        GROUP BY sys_code;"""
    losing_trades_sql = """
        CREATE OR REPLACE VIEW losing_trades AS
        SELECT sys_code, SUM(profit)
        FROM staging_area."fact_trades"
        WHERE profit < 0
        GROUP BY sys_code;"""
    
    # execute the SQL statements
    cursor.execute(winning_trades_sql)
    cursor.execute(losing_trades_sql)
    cursor.execute(positive_trades_sql)
    cursor.execute(negative_trades_sql)
    
    
def transform_analytics(cursor):
    """
    Parameters
    ----------
    cursor : database cursor object
    
    DESCRIPTION: executes query to transform data in data warehouse for analytics

    Returns
    -------
    None.

    """
    
    analytics_sql = """ 
        CREATE MATERIALIZED VIEW IF NOT EXISTS trade_analytics AS
        SELECT ft.trade_id, ft.trade_identifier, dd.trade_date, dsys.sys_code, dsys.sys_name, dsc.sector, dm.market, ft.profit
        FROM staging_area."fact_trades" AS ft
            LEFT JOIN staging_area."dim_date" AS dd
            ON ft.date_id = dd.date_id
            LEFT JOIN staging_area."dim_system" AS dsys
            ON ft.sys_code = dsys.sys_code
            LEFT JOIN staging_area."dim_sector" AS dsc
            ON ft.sector_id = dsc.sector_id
            LEFT JOIN staging_area."dim_market" AS dm
            ON ft.market_id = dm.market_id
        WITH DATA;"""
    refresh_sql = "REFRESH MATERIALIZED VIEW trade_analytics;"
    
    # execute the SQL statements
    cursor.execute(analytics_sql)
    cursor.execute(refresh_sql)
    

    
def transform_reverse_ETL(cursor):
    """
    Parameters
    ----------
    cursor : database cursor object
    
    DESCRIPTION: executes query to transform data in data warehouse for reverse ETL

    Returns
    -------
    None.

    """
    #cast(pt.count AS DECIMAL)
    #TRUNC((pt.count::numeric/nt.count::numeric),4)
    rev_ETL_sql = """ 
        CREATE MATERIALIZED VIEW IF NOT EXISTS system_statistics AS
        WITH system_winrate AS (
            SELECT pt.sys_code, TRUNC((cast(pt.count AS DECIMAL)/cast(nt.count AS DECIMAL)),4) AS winrate
            FROM positive_trades AS pt
                LEFT JOIN negative_trades AS nt
                ON pt.sys_code = nt.sys_code
        ), system_rr_ratio AS (
            SELECT wt.sys_code, TRUNC(ABS(cast(wt.sum AS DECIMAL)/cast(lt.sum AS DECIMAL)),2) AS rr_ratio
            FROM winning_trades AS wt
                LEFT JOIN losing_trades AS lt
                ON wt.sys_code = lt.sys_code
        )
        SELECT sw.sys_code, sw.winrate, sr.rr_ratio
        FROM system_winrate AS sw
                LEFT JOIN system_rr_ratio AS sr
                ON sw.sys_code = sr.sys_code
        WITH DATA;"""
    refresh_sql = "REFRESH MATERIALIZED VIEW system_statistics;"
    
    # execute the SQL statements
    cursor.execute(rev_ETL_sql)
    cursor.execute(refresh_sql)
    
    
def main_Transformation():
    """
    Parameters
    ----------
    None
    
    DESCRIPTION: connects to datawarehouse and transforms data

    Returns
    -------
    None.

    """

    dsn_hostname = os.getenv('POSTGRES_HOST', '')
    dsn_user= os.getenv('POSTGRES_USER', '')
    dsn_pwd = os.getenv('POSTGRES_PASSWORD', '')
    dsn_port = int(os.getenv('POSTGRES_PORT', 5432))
    dsn_database = os.getenv('POSTGRES_DB', '')

    # create connection
    conn = None
    is_connected : bool = False
    try:
        conn = psycopg2.connect(
            database=dsn_database, 
            user=dsn_user,
            password=dsn_pwd,
            host=dsn_hostname, 
            port= dsn_port
        )
        is_connected = True
    except Exception as e:
        print("Error connecting to data warehouse")
        print(e)
    else:
        print("Successfully connected to warehouse")


    if is_connected:
        try:
            #Create a cursor onject using cursor() method
            cursor = conn.cursor()

            # create views for logic
            create_logic_views(cursor=cursor)
            logger.info('!!!!!!!!')
            logger.info('Views created succesfully')

            # transform data for analytics
            transform_analytics(cursor=cursor)
            logger.info('!!!!!!!!')
            logger.info('Analytics Data transformed into Materialized view succesfully')

            # transform data for reverse ETL
            transform_reverse_ETL(cursor=cursor)
            logger.info('!!!!!!!!')
            logger.info('Reverse ETL Data transformed into Materialized view succesfully')
            
            conn.commit()

        except Exception as e:
            conn.rollback()
            logger.error('!!!!!!!!!!!!!!!!!!!!!!')
            logger.error(f'Transformation changes rolled back due to Error transforming data: {e}')
    
    conn.close()
    


if __name__ == "__main__":
    main_Transformation()