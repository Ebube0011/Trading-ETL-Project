from Serve.storage.connection import close_conn, create_db_conn
from Serve.extract.extract_data import read_table
from Serve.load.update_data import update_system_stats

def serve_reverse_etl():
    """ Get Data from Data Warehouse"""
    # connect to data warehouse
    engine = create_db_conn()

    # get fact data for the etl
    view_name = 'system_statistics'
    df = read_table(engine, view_name)

    # close the connection
    close_conn(engine)

    """ Load the data into Application database """
    # connect to application database
    engine = create_db_conn(storage_use="application")

    # update system stats data in database
    update_system_stats(engine, df)

    # close the connection
    close_conn(engine)