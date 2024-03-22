import os

from Ingestion.storage.db import DBConnection


def get_warehouse_creds() -> DBConnection:
    return DBConnection(
        user=os.getenv('POSTGRES_USER', ''),
        pwd=os.getenv('POSTGRES_PASSWORD', ''),
        database=os.getenv('POSTGRES_DB', ''),
        host=os.getenv('POSTGRES_HOST', ''),
        port=int(os.getenv('POSTGRES_PORT', 5432))
    )

def get_transaction_db_creds() -> DBConnection:
    return DBConnection(
        user=os.getenv('MYSQL_USER', ''),
        pwd=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DB', ''),
        host=os.getenv('MYSQL_HOST', ''),
        port=int(os.getenv('MYSQL_PORT', 3306))
    )