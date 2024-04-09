#import os
from Serve.storage.connection import close_conn, create_db_conn
from Serve.extract.extract_data import read_table
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
targetfile = "account_performance.csv" #os.environ.get('AMAZON_S3_BUCKET')

def serve_analytics():

    # connect to data warehouse
    engine = create_db_conn()

    try:
        # get fact data for analytics
        view_name = 'trade_analytics'
        df = read_table(engine, view_name)

        # save result in s3 bucket in csv format
        df.to_csv(targetfile, index=False)
        logger.info('!!!!!!!!')
        logger.info(f'Table loaded succesfully')

    except Exception as e:
        logger.error("!!!!!!!!!!!!!!!!!!!!!!")
        logger.error(f"Unable to load the data to Object Storage : {e}")

    close_conn(engine)