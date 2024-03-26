import logging

from sqlalchemy import create_engine
from Ingestion.storage.db import WarehouseConnection, RelationalStorageConnection
from Ingestion.storage.side_config import get_warehouse_creds, get_transaction_db_creds

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_conn(
    connection_string=WarehouseConnection(
        get_warehouse_creds()
    ).connection_string(),
):
    # connect to the postgres database
    try:
        engine = create_engine(connection_string)
        logger.info("Connected to postgres database!!")
        return engine
    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to connect to postgres : {e}")

def create_db_conn(storage_use: str = "warehouse"):

    # connect to the database
    if (storage_use == "warehouse"):
        db_name = "postgresql"
        credentials = get_warehouse_creds()
    elif (storage_use == "application"):
        db_name = "mysql+mysqlconnector"
        credentials = get_transaction_db_creds()
    
    conn_string=RelationalStorageConnection(credentials, db_name).connection_string()

    try:
        engine = create_engine(conn_string)
        logger.info(f"Connected to {db_name} database!!")
        return engine
    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to connect to {db_name} : {e}")

def close_conn(engine):
    # close the connection
    engine.dispose()