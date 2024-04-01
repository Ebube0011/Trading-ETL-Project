# Trading-ETL-Project
This project extracts data from a source database system and loads the data into a landing area in the data warehouse. It then proceeds to transform the data and loads this new data into a staging area within the data warehouse. The source system is a mysql transactional database and the data warehouse is a postgres database. Python sqlalchemy is used to perform both the extraction and the loading processes.

# Objective
This projects objective is to increase trading returns, reduce drawdowns, optimize overall performance of the trading systems, and perform analytics to better understand performance of the system's trading performance. It is designed to ingest data from an application database for analytics. The data can then be ananlysed and then used to optimize the performance of the application. 

## Stages of the project
### Data Generation
This is done in a trading application written using MQL4 and uses a mysql database to store transactional data of the trade positions taken as well as the result of the trade. The schema is below
![Trading_Employee_Project-Generation drawio](https://github.com/Ebube0011/Trading-ETL-Project/assets/149321069/bb807d7e-4520-400d-9455-a2bc055dbf54)

### Ingestion
Data is ingested using the mysql connector + sqlalchemy, transformed, and loaded into the data warehouse landing area. An orchestration tool (airflow) is used to schedule the ingestion tasks and alerts when there is a failed task. The data ingested has a typical volume in kilobytes, ingested daily, and will be used for analytics and reverse ETL.
![Trading_Employee_Project-Ingestion drawio](https://github.com/Ebube0011/Trading-ETL-Project/assets/149321069/b793c7ef-65a6-4162-9573-e2a09ca8ee55)

## How to Install and Run the Project
First, clone the repository into the virtual machine or ubuntu computer. 
```
git clone https://github.com/Ebube0011/Trading-ETL-Project.git
```
Next, install docker and python
```
chmod a+x docker_setup.sh python_setup.sh

# run the shell scripts
./docker_setup.sh
./python_setup.sh
```

### Docker Networks
Create networks which the containers will be using to communicate with each other
```
docker network create sourcesystem-net
docker network create warehouse-net
```

### Specify environment variables
Inside the 'environment_variables' folder, there are files that will be used to specify certain environment variables depending on the service. Edit the files to specify the values of the variables necessary for the project.
Be careful if using a 'file path' environment variable with airflow as airflow runs its dags in a seperate file path than is in the container. In that case, either use an absolute file path or use code to identify current working directory.

### Run the storage containers
After modifying the environment variables, return to the project directory and proceed to run the storage services. 
This is done by using the 'docker compose' command. we start by running the services for the storages, and then the services for orchestration
For the storages; transactional and warehouse. To view performance of each service using a terminal each, remove the '-d' that is at the end of the docker compose command.
```
# for storages
docker compose -f docker-compose-storage.yml up -d

# for the orchestration (airflow)
docker compose -f docker-compose-orchestration.yml up -d
```

### Testing pipeline so far
To view results on data warehouse and manually query it
```
# testing the application database
docker exec -it mysql bash
mysql -P 3306 --protocol=tcp -u user -p

USE TFEmployee;
SELECT * FROM Sector;



# testing the data warehouse
docker exec -it warehouse bash
psql -U postgres

\c TFEmployee
SELECT * FROM landing_area."Trade_results";
```
The pipeline can be tested by putting the code in a seperate container using a dockerfile to check the performance of the python script. Open another terminal, enter into the project folder, then enter
```
# incase it already exists
docker image rm pipeline:latest -f

# build the image
docker build -t pipeline:latest -f test/Dockerfile .

# run and interact with the container
docker run --rm -it --env-file ./environment_variables/mysql.env --env-file ./environment_variables/postgres.env --env-file ./environment_variables/others.env --network warehouse-net --network sourcesystem-net pipeline bash

# run the main pipeline script
cp Ingestion/main_pipeline.py .
python3 main_pipeline.py
```

### Orchestraion
Using the dns/localhost of the virtual machine or pc, include the port '8080' and open the airflow page on the web browser
eg. 'localhost:8080' or '<aws ipv4 dns>:8080'.
Proceed to locate the dag and run it.


### Shut down
To shut down, using a fresh terminal
```
docker compose -f docker-compose-orchestration.yml down
docker compose -f docker-compose-storage.yml down
```

