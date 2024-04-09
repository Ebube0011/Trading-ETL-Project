from sqlalchemy import text
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def update_system_stats(engine, df):
    """load the tables to the staging schema for visualization"""
    try:
        with engine.connect() as conn:
            for i in range(len(df)):
                sys_code = df.iloc[i, 0]
                winrate = df.iloc[i, 1]
                rr_ratio = df.iloc[i, 2]

                winrate_sql = text(f""" 
                    UPDATE Trading_System
                    SET winrate = {winrate}
                    WHERE system_code = {sys_code}""")
                rr_ratio_sql = text(f""" 
                    UPDATE Trading_System
                    SET rr_ratio = {rr_ratio}
                    WHERE system_code = {sys_code}""")
                
                conn.execute(winrate_sql.execution_options(autocommit=True))
                conn.execute(rr_ratio_sql.execution_options(autocommit=True))
                conn.commit()
        logger.info("system stats updated in source system!!!")

    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to update data in source system : {e}")
