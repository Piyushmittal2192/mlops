import mlflow

from get_data import read_params

config_path = 'params.yaml'

config = read_params(config_path)

mlflow_config = config['mlflow_config']

model_name = mlflow_config['registered_model_name']
remote_server_uri = mlflow_config['remote_server_uri']
mlflow.set_tracking_uri(remote_server_uri)

experiment_name = mlflow_config['experiment_name']
print(mlflow.get_experiment_by_name(experiment_name))
current_experiment = dict(mlflow.get_experiment_by_name(experiment_name))
experiment_id = current_experiment['experiment_id']

# experiment_id = mlflow.create_experiment("ElasticNet Regression")
mlflow.delete_experiment(experiment_id)

# Examine the deleted experiment details.
experiment = mlflow.get_experiment(experiment_id)
print("Name: {}".format(experiment.name))
print("Artifact Location: {}".format(experiment.artifact_location))
print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))