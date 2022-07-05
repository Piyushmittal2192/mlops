import os
import argparse
import joblib
import os

import mlflow
from mlflow.tracking import MlflowClient
from get_data import read_params

from icecream import ic
import logging
import datetime

logging.basicConfig(filename='./logs/mlrun.log', level=logging.DEBUG)

def log_production_model(config_path):
    config = read_params(config_path)

    mlflow_config = config['mlflow_config']

    model_name = mlflow_config['registered_model_name']
    remote_server_uri = mlflow_config['remote_server_uri']
    mlflow.set_tracking_uri(remote_server_uri)

    experiment_name = mlflow_config['experiment_name']
    print(mlflow.get_experiment_by_name(experiment_name))
    current_experiment = dict(mlflow.get_experiment_by_name(experiment_name))
    experiment_id = current_experiment['experiment_id']

    runs = mlflow.search_runs(experiment_ids=experiment_id)
    lowest = list(runs['metrics.MAE'].sort_values(ascending=True))[0]
    lowest_run_id = runs[runs['metrics.MAE'] ==lowest]['run_id'].iloc[0]
    # ic(lowest_run_id)
    # ic(runs)
    # ic(lowest)
    # maes = runs['metrics.MAE'].sort_values(ascending=True)
    # ic(maes)
    client = MlflowClient()
    # ic(client.search_model_versions(f"name='{model_name}'"))
    for mv in client.search_model_versions(f"name='{model_name}'"):
        mv = dict(mv)
        # ic(mv)
        # ic(lowest_run_id)
        if mv['run_id'] ==lowest_run_id:
            current_version = mv['version']
            # print("lowest\n")
            # ic(current_version)
            logged_model = mv['source']
            client.transition_model_version_stage(
                name = model_name,
                version=current_version,
                stage='Production'
            )
        else:
            current_version = mv['version']
            client.transition_model_version_stage(
                name=model_name,
                version=current_version,
                stage='Staging'
            )
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    model_path = os.path.join(config['webapp_model_dir'], 'model.joblib')

    joblib.dump(loaded_model, model_path)

    logging.info('New model saved for production at : ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))



if __name__ == '__main__':

    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_arg = args.parse_args()
    log_production_model(config_path=parsed_arg.config)