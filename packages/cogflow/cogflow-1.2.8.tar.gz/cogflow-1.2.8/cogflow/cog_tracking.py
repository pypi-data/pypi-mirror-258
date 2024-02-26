from mlflow.tracking import MlflowClient
import mlflow

class MLFlowManager:
    def __init__(self, tracking_uri=None):
        # Set tracking URI if provided
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        # Create an MLflow client
        self.client = MlflowClient(tracking_uri=tracking_uri)

    def start_run(self):
        return mlflow.start_run()

    def end_run(self):
        return mlflow.end_run()

    def log_model(self, *args, **kwargs):
        return mlflow.log_model(*args, **kwargs)

    def set_experiment(self, experiment_name):
        return self.client.set_experiment(experiment_name)

    def set_tracking_uri(self, tracking_uri):
        mlflow.set_tracking_uri(tracking_uri)

    def autolog(self, *args, **kwargs):
        return mlflow.autolog(*args, **kwargs)

    def log_param(self, key, value):
        return mlflow.log_param(key, value)

    def log_metric(self, key, value):
        return mlflow.log_metric(key, value)

    def get_artifact_uri(self, *args, **kwargs):
        return mlflow.get_artifact_uri(*args, **kwargs)

    def tensorflow(self, *args, **kwargs):
        return mlflow.tensorflow(*args, **kwargs)

    def sklearn(self, *args, **kwargs):
        return mlflow.sklearn(*args, **kwargs)


class CogFlow:
    def __init__(self, tracking_uri=None):
        # Instantiate MLFlowManager
        self.mlflow_manager = MLFlowManager(tracking_uri)

    # Define other functionalities of your cogflow library
