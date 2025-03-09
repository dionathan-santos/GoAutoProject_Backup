import os
import yaml
import mlflow

# Load MLflow settings from parameters.yml
def load_mlflow_config(config_path="configs/parameters.yml"):
    with open(config_path, "r") as f:
        params = yaml.safe_load(f)
    return params["mlflow"]

def initialize_mlflow():
    """Initialize MLflow with configurations from parameters.yml."""
    mlflow_config = load_mlflow_config()

    # Set tracking URI
    mlflow.set_tracking_uri(mlflow_config["tracking_uri"])

    # Create or set the experiment
    experiment_name = mlflow_config["experiment_name"]
    experiment = mlflow.get_experiment_by_name(experiment_name)

    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"Created new MLflow experiment: {experiment_name} (ID: {experiment_id})")
    else:
        print(f"Using existing MLflow experiment: {experiment_name} (ID: {experiment.experiment_id})")

    return experiment_name

if __name__ == "__main__":
    initialize_mlflow()
