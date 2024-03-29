import os

#import pandas as pd
from Ingestion.storage.connection import close_conn, create_db_conn #create_conn,
from Ingestion.extract.to_landing import load_table_to_landing, read_source_table
from Ingestion.transformation.etl import (
    clean_data,
    create_schema,
    load_tables_staging,
    read_table,
)


def main_etl():

    """ Get Data from Source System"""
    #engine = create_conn()
    engine = create_db_conn(storage_use="application")

    #file_path = os.getenv('FILE_PATH')
    ss_table_name = os.getenv('SOURCE_TABLE_NAME')
    df = read_source_table(engine, ss_table_name)

    close_conn(engine)

    """ Load the data into Warehouse Landing area """
    engine = create_db_conn()

    table_name = os.getenv('TABLE_NAME')

    #df = pd.read_csv(file_path)
    load_table_to_landing(df, engine, table_name)

    """ Transform and Load the data into Warehouse Staging area """
    df = read_table(engine, table_name)
    df_clean = clean_data(df)
    dict_tables = create_schema(df_clean)
    load_tables_staging(dict_tables, engine)

    close_conn(engine)


if __name__ == "__main__":
    main_etl()
