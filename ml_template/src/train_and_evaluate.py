import os
import pandas as pd
import numpy as np
from get_data import read_params
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse # this is to check if mlflow server is up and running
import joblib
import json
import argparse
import mlflow
import pysftp
from icecream import ic

#
# os.environ['MLFLOW_TRACKING_USERNAME'] = 'emitpiy'
# os.environ['MLFLOW_TRACKING_PASSWORD'] = 'Temp123!'



def eval_metrics(actuals, prediction ):

    rmse = np.sqrt(mean_squared_error(actuals, prediction))
    mae = mean_absolute_error(actuals, prediction)
    r2 = r2_score(actuals, prediction)

    return rmse, mae, r2

def load_train_test_data(config_path):
    config = read_params(config_path)
    train_data_path = config['split_data']['train_path']
    test_data_path = config['split_data']['test_path']

    train_data = pd.read_csv(train_data_path, sep=',', encoding='utf-8')
    test_data = pd.read_csv(test_data_path, sep=',', encoding='utf-8')
    return train_data , test_data

def train_and_evaluate(config_path):
    config = read_params(config_path)


    random_state = config['base']['random_state']
    target = config['base']['target_col']
    alpha = config['estimators']['ElasticNet']['params']['alpha']
    l1_ratio = config['estimators']['ElasticNet']['params']['l1_ratio']
    model_directory = config['models']['model_dir']

    train_data, test_data = load_train_test_data(config_path)

    train_y = train_data[target]
    test_y = test_data[target]

    train_x = train_data.drop(target, axis = 1)
    test_x = test_data.drop(target, axis= 1)

    # model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
    # model.fit(train_x, train_y)
    # prediction = model.predict(test_x)
    # (rmse, mae, r2) = eval_metrics(test_y, prediction)
    #
    # os.makedirs(model_directory, exist_ok=True)
    # model_path = os.path.join(model_directory, "model.joblib")
    #
    # joblib.dump(model, model_path)
    # try:
    #     transfer_artifacts(config_path)
    # except Exception as e:
    #     print(str(e))
    mlflow_config = config['mlflow_config']
    remote_server_uri = mlflow_config['remote_server_uri']
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment(mlflow_config['experiment_name'])

    # mlflow.create_experiment(mlflow_config['experiment_name'], artifact_location='sftp://emitpiy:Temp123!@138.85.180.211:22/data/ml_pipeline/mlruns/mlflow_artifacts')
    #
    # experiment = mlflow.get_experiment_by_name(mlflow_config['experiment_name'])

    experiment_name = mlflow_config['experiment_name']

    try:
        current_experiment = dict(mlflow.get_experiment_by_name(experiment_name))
        experiment_id = current_experiment['experiment_id']

        runs = mlflow.search_runs(experiment_ids=experiment_id)
        len_runs = len(runs)
    except:
        len_runs = 0
    ## adding run_name=mlflow_config['run_name'] + str(len_runs + 1) makes each run unique
    with mlflow.start_run(run_name=mlflow_config['run_name'] + str(len_runs + 1)):
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
        model.fit(train_x, train_y)
        prediction = model.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, prediction)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2-Score", r2)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

        if tracking_url_type_store != 'file':
            mlflow.sklearn.log_model(model, 'models', registered_model_name=mlflow_config['registered_model_name'])
        else:
            mlflow.sklearn.load_model(model, 'models')

        os.makedirs(model_directory, exist_ok=True)
        model_path = os.path.join(model_directory, "model.joblib")

        joblib.dump(model, model_path)
        # try:
        #     transfer_artifacts(config_path)
        # except Exception as e:
        #     print(str(e))


    ###### print results #######
    # print(r"RMSE: {}".format(rmse))
    # print(r"MAE: {}".format(mae))
    # print(r"r2: {}".format(r2))
    ##########

if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_arg = args.parse_args()
    train_and_evaluate(config_path=parsed_arg.config)




