# Trading-ETL-Project
This project extracts data from a source database system and loads the data into a landing area in the data warehouse. It then proceeds to transform the data and loads this new data into a staging area within the data warehouse. The source system is a mysql transactional database and the data warehouse is a postgres database. Python sqlalchemy is used to perform both the extraction and the loading processes.

## How to Install and Run the Project
First, clone the repository into the virtual machine or computer. 
```
git clone https://github.com/Ebube0011/Trading-ETL-Project.git
```
Next, install docker and python
```
chmod a+x docker_setup.sh
chmod a+x python_setup.sh

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
Be careful if using the 'file path' with airflow as airflow runs its dags in a seperate file path than is in the container. In this case, either use an absolute file path or use code to identify current working directory.

### Run the storage containers
This is done by using the 'docker compose' command. we start by running the services for the storages, and then the services for orchestration
For the storages; transactional and warehouse, using a terminal each
```
# for storages
docker compose -f docker-compose-storage.yml up 

# for the orchestration (airflow)
docker compose -f docker-compose-orchestration.yml up
```

### Test
The app can be tested by using a dockerfile to check the performance of the python script. Open another terminal, enter into the test folder, then enter
```
# incase it already exists
docker image rm pipeline:latest -f

# build the image
docker build -t pipeline:latest .

# run and interact with the container
docker run --rm -it --env-file ../environment_variables/postgres.env --env-file ../environment_variables/others.env --network warehouse-net pipeline bash

# run the main pipeline script
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

