# Import libraries required for connecting to mysql
# Import libraries required for connecting to DB2 or PostgreSql

import os
import psycopg2
import mysql.connector as msc
import glob                         # this module helps in selecting files 
import pandas as pd                 # this module helps in processing CSV files
from datetime import datetime

tmpfile    = "temp.tmp"               # file used to store all extracted data
logfile    = "logfile.txt"            # all event logs will be stored in this file
targetfile = "transformed_data.csv"   # file where transformed data is stored

# get database records
def query_database_data():
	# get environment variables	
	db_user = os.environ.get('MYSQL_USER')
	db_password = os.environ.get('MYSQL_PASSWORD')
	db_host = os.environ.get('MYSQL_HOST')
	db_database = os.environ.get('MYSQL_DATABASE')
	db_table = os.environ.get('MYSQL_TABLE')

    # Connect to MySQL
	connection = None
	try:
		connection = msc.connect(user=db_user, 
							password=db_password,
							host=db_host,
							database=db_database,
							table=db_table)
            
		# create cursor
		cursor = connection.cursor()
	except Exception as e:
		print("Error connecting to Database")
		print(e)
	else:
		print("Successfully connected to Database")
            
	# query data
	if connection:
		today = datetime.date.today()
		query = f""" WITH instruments (id, market, sector) AS (
				SELECT t1.market_id, 
					t1.name,
					t2.name
				FROM market AS t1
					LEFT JOIN sectors
					ON t1.sector_id = t2.sector_id
			)
			SELECT t.trade_id, 
				t.market_id
				i.market,
				t.sector_id
				i.sector,
				t.lot_size,
				t.open_price,
				t.close_price,
				t.percent_risk,
				t.stoploss,
				t.percent_profit,
				sys.name AS system_name,
				t.direction,
				t.open_time,
				t.close_time 
			FROM trade AS t
				LEFT JOIN instruments AS i
					ON t.market_id = i.id
				LEFT JOIN system AS sys
					ON t.sys_id = sys.sys_id
			WHERE status = 'CLOSED' 
				AND close_time LIKE '{today} %'""" 

		cursor.execute(query)	
		
		# get result
		query_result = []
		for row in cursor.fetchall():
			query_result.append(row)
				
		# save data as parquet file
		df = pd.DataFrame(query_result, columns=cursor.ColumnNames)
		df.to_parquet('raw_data/data.parquet')

		# disconnect from mysql warehouse
		connection.close()
	
	

# csv extract function
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

# extract function
def extract():
	#df = pd.DataFrame(table_rows, columns=db_cursor.column_names)
	extracted_data = pd.DataFrame(columns=['name','height','weight']) # create an empty data frame to hold extracted data

	#process all csv files
	for csvfile in glob.glob("*.csv"):
		extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)

	return extracted_data

# transform function
def transform():
	df = pd.read_parquet('raw_data/data.parquet')

	dim_System = df[['id', 'system_name']]
	dim_Market = df[['id', 'market_name']]
	dim_Sector = df[['id', 'sector_name']]
	dim_Direction = df[['id', 'direction']]
	fact_Trade = df[['id', 'market_id', 'sector_id', 
				   'lot_size', 'open_price', 'close_price',
				   'percent_risk', 'stoploss', 'percent_profit', 
				   'sys_id', 'dir_id', 'open_time', 'close_time']]
	
	# load files to file system
	dim_Direction.to_parquet('transformed_data/dimDirection.parquet')
	dim_Market.to_parquet('transformed_data/dimMarket.parquet')
	dim_Sector.to_parquet('transformed_data/dimSector.parquet')
	dim_System.to_parquet('transformed_data/dimSystem.parquet')
	fact_Trade.to_parquet('transformed_data/factTrade.parquet')
	


# loading function
def load():
	"""load data into data warehouse"""
	# get environment variables
	db_user = os.environ.get('POSTGRES_USER')
	db_password = os.environ.get('POSTGRES_PASSWORD')
	db_host = os.environ.get('POSTGRES_HOST')
	db_port = os.environ.get('POSTGRES_PORT')
	db_database = os.environ.get('POSTGRES_DATABASE')

	# Connect to PostgreSql
	conn = None
	try:
		conn = psycopg2.connect(
			user = db_user,
			password = db_password,
			host = db_host,
			port = db_port,
			database = db_database)
		# create cursor
		curr = conn.cursor()
	except Exception as e:
		print("Error connecting to data warehouse")
		print(e)
	else:
		print("Successfully connected to warehouse")

	# insert data into database if connection is successful
	if conn:
		df = pd.read_parquet('transformed_data/data.parquet')
		records_to_insert = list(df.itertuples(index=False, name=None))

		# load data into database
		SQL = """INSERT INTO products(rowid,product,category) 
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		curr.executemany(SQL,records_to_insert);
		conn.commit()

		# close the connection
		conn.close()


# logging function
def log(message):
	""" write event messages to log file"""
	timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
	now = datetime.now() # get current timestamp
	timestamp = now.strftime(timestamp_format)
	with open("logfile.txt","a") as f:
		f.write(timestamp + ',' + message + '\n')



if __name__ == "__main__":
	# running the etl process
	log("ETL Job Started")

	log("Extract phase Started")
	extract()
	log("Extract phase Ended")

	log("Transform phase Started")
	transform()
	log("Transform phase Ended")

	log("Load phase Started")
	load()
	log("Load phase Ended")

	log("ETL Job Ended")