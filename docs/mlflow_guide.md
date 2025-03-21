# MLflow Experiment Tracking Guide

## Overview
MLflow is an open-source platform for managing the end-to-end machine learning lifecycle. In this project, we use MLflow to:
- Track experiments
- Log model parameters and metrics
- Store and version machine learning models

## Setup

1. Install MLflow:
   ```bash
   pip install mlflow
   ```

2. Configure MLflow tracking:
   - Configuration is stored in `mlflow_config/config.yaml`
   - Tracking URI is set to a local SQLite database
   - Artifacts are stored in a local directory

## Basic Usage

### Starting an Experiment
```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Set the experiment
mlflow.set_experiment("GoAuto_Car_Price_Prediction")

# Start a run
with mlflow.start_run():
    # Prepare your data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Train a model
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("model_type", "RandomForestRegressor")
    
    # Log metrics
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    mlflow.log_metric("train_r2_score", train_score)
    mlflow.log_metric("test_r2_score", test_score)
    
    # Log the model
    mlflow.sklearn.log_model(model, "car_price_model")
```

## Best Practices

1. **Experiment Naming**
   - Use descriptive, consistent experiment names
   - Include project name and specific task
   - Example: "GoAuto_Car_Price_Prediction_V1"

2. **Logging**
   - Always log key parameters
   - Log performance metrics
   - Log the trained model
   - Add tags for better organization

3. **Configuration**
   - Use the provided `mlflow_config/config.yaml`
   - Never commit sensitive information to version control

## Viewing Experiments

1. Launch MLflow UI:
   ```bash
   mlflow ui
   ```
   This will start a local server where you can view all tracked experiments.

2. Access the UI at: `http://localhost:5000`

## Cleaning Up

- MLflow artifacts are stored locally in `mlartifacts/`
- Database files are local and not tracked by Git
- Periodically clean up old experiments to manage disk space

## Troubleshooting

- If you encounter tracking issues, check the configuration in `mlflow_config/config.yaml`
- Ensure you have the latest version of MLflow installed
- Verify that you have write permissions to the artifact and database locations

## Advanced Usage

For more complex scenarios like distributed training or remote tracking, refer to the [MLflow Documentation](https://mlflow.org/docs/latest/index.html).