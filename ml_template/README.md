## TO DO
    After each succful run add schema_in.json to server config location 


# ml_template
### Create a conda environment
```buildoutcfg
conda create -n env_name python=3.7 -y
conda activate env_name
```

### Start your local mlflow server
```buildoutcfg
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts --host 127.0.0.1 -p 1234
```

### Install python requirements 
```buildoutcfg
pip install -r requirements.txt
```

### Create template
```buildoutcfg
 Execute python template.py to create basic template for project 
```

### Initialize git
```buildoutcfg
git remote add origin https://github.com/<username>/<project_name>.git
git init
```

### Initialize dvc
    dvc ini
    dvc add data_given/winquality.csv
    git add . && git commit -m "add dvc" && git push origin main



#### Update production Model Artifact
    Put production model to api server model location using pysftp
    New model would be used to perform inferencing
    dvc add ./production_model/model.joblib
####  


### app.py
    UI for initialiting the training job and changing the parameters
    will initiate the monitor_data_and_target_drift to give results for drift


### setup mysql server
    persistant mysql location:
        - mkdir /data/ml_pipeline/mysql
        - chmod -R 777 ./mysql
    docker network create prometheus-grafana-network --driver bridge
    docker pull mysql:latest
    # start mysql server
    docker run --network=prometheus-grafana-network -p 3306:3306 --name docker-mysql -v /data/ml_pipeline/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=dl123! -d mysql:latest
    # enter in mysql server as a client
    docker run -it --name=doc-mysql --network=prometheus-grafana-network --rm mysql mysql -hdocker-mysql -uroot -p
    # create database
        - CREATE DATABASE ml_data;
        - CREATE USER 'ml'@'%' IDENTIFIED BY 'ml123!';
        - GRANT ALL ON *.* TO 'ml'@'%';
        - flush privileges;

table create query:    
```buildoutcfg
CREATE TABLE `ml_data`.`raw_data` (
  `id` INT NOT NULL AUTO_INCREMENT,
   `timestamp` TIMESTAMP NOT NULL,
  `fixed_acidity` FLOAT NULL,
  `volatile_acidity` FLOAT NULL,
  `citric_acid` FLOAT NULL,
  `residual_sugar` FLOAT NULL,
  `chlorides` FLOAT NULL,
  `free_sulfur_dioxide` FLOAT NULL,
  `total_sulfur_dioxide` FLOAT NULL,
  `density` FLOAT NULL,
  `pH` FLOAT NULL,
  `sulphates` FLOAT NULL,
  `alcohol` FLOAT NULL,
  `TARGET` INT NULL,
  `PRED_TARGET` INT NULL,
  PRIMARY KEY (`id`));
```
### Store original data in a DB
    new data will be added when a prediction is made
    store data using inset_data_to_db.py

### monitor_data_and_target_drift.py
    
    rerfernce data: data till last run of the model training
    new data : data between last production model update date and current date 
    run evidently package on the reference data and new data to monitor the drift




