# GoAuto Project

## Overview
This project analyzes car sales data to optimize dealership performance in Edmonton by leveraging machine learning models, exploratory data analysis (EDA), and predictive analytics. It is designed to provide insights into geographical clusters, sales patterns, and inventory optimization.

---

## Features
- **Exploratory Data Analysis (EDA):**
  - Analyze car sales data to uncover trends and patterns.
- **Clustering:**
  - Group regions based on average price and mileage using KMeans clustering.
- **Predictive Modeling:**
  - Predict sales regions and dealership performance.
- **Interactive Visualizations:**
  - Use Streamlit to present data and insights interactively.
- **REST API for Model Predictions:**
  - Flask-based API to serve multiple versions of trained models.

---

## Folder Structure
```plaintext
GoAuto Project/
├── app_files/          # Static assets for the Streamlit app
│   ├── Dealership-map.html # Map visualization
│   ├── image.png       # Logo or other static images
├── configs/            # Configuration files
│   ├── config.yaml     # YAML configuration file
├── data/               # Datasets for analysis
│   ├── CBB_Listings_LongLat.csv # Main dataset
│   ├── used_cars.csv   # Sample used cars data
│   ├── new_cars.csv    # Sample new cars data
├── docs                # Documentation
├── experiment          # Experimentation
├── models/             # Machine learning models
│   ├── model_v1.pkl    # Version 1 of the model
│   ├── model_v2.pkl    # Version 2 of the model
├── notebook/           # Jupyter notebooks for experimentation
│   ├── GoAuto.ipynb    # Exploratory Data Analysis notebook
├── src/                # Main application logic
│   ├── app.py          # Basic Streamlit app
│   ├── advanced_app.py # Advanced Streamlit app
│   ├── data_analysis.py # Data exploration and visualization logic
│   ├── visualization.py # Visualization functions
│   ├── utilities.py    # Utility functions
├── test/               # Unit tests for the codebase
├── predict_api.py      # Flask API for model predictions
├── requirements.txt    # Python dependencies
├── makefile            # Automation tasks (setup, run, test)
├── README.md           # Main Project documentation
```

---

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GoAuto Project
   ```

2. Pull the data using DVC:
   ```bash
   # Install DVC if not already installed
   pip install dvc
   
   # Pull the data and models
   dvc pull
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Version Control
This project uses a combination of Git, DVC (Data Version Control), and MLflow to manage code, data, and machine learning experiments:

- **Git**: Tracks code, configuration files, and documentation
- **DVC**: Tracks data files and ML models
- **MLflow**: Tracks machine learning experiments, metrics, and model artifacts

### Version Control Structure
- Code files (.py, .yaml, etc.) are tracked with Git
- Data files (.csv, etc.) are tracked with DVC
- Model files (.pkl) are tracked with DVC
- MLflow artifacts and configurations are excluded from version control

### Working with DVC
1. After making changes to tracked data:
   ```bash
   dvc add data/
   dvc add models/
   ```

2. Commit the changes to Git:
   ```bash
   git add .
   git commit -m "Update data and models"
   ```

3. Push the changes:
   ```bash
   git push
   dvc push
   ```

4. To get the latest data:
   ```bash
   git pull
   dvc pull
   ```

### MLflow Experiment Tracking
1. MLflow is used to track machine learning experiments:
   ```python
   import mlflow

   # Start an MLflow run
   with mlflow.start_run():
       # Log parameters
       mlflow.log_param("model_type", "RandomForest")
       
       # Log metrics
       mlflow.log_metric("accuracy", 0.85)
       
       # Log the model
       mlflow.sklearn.log_model(model, "model")
   ```

2. MLflow configuration is stored in `mlflow_config/config.yaml`

3. MLflow artifacts and database files are intentionally excluded from version control

### Best Practices
- Never commit MLflow database files or artifact directories to Git
- Use the provided MLflow configuration for consistent experiment tracking
- Store sensitive information like API keys in environment variables or a secure configuration management system

## Usage
### Run the Streamlit App
```bash
streamlit run src/app.py
```

### Run the Advanced Streamlit App
```bash
streamlit run src/advanced_app.py
```

## Prediction API

### **1️⃣ API Overview**
The **Dealership Insights API** serves trained models for predicting car prices based on various features like make, model, year, mileage, and condition.

It includes:
- **Two prediction endpoints** for comparing different model versions.
- **Health check & home endpoints** for API status and usage details.

---

### **2️⃣ API Setup and Installation**

1. Install dependencies (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. Create dummy models for testing (optional):
   ```bash
   python models/create_dummy_models.py
   ```

3. Run the API:
   ```bash
   python predict_api.py
   ```
   The API will be available at http://localhost:5000
   
   ⚠️ **Important Note**: 
   - The API is specifically configured to run on port 5000
   - Do not use any other port when accessing the API
   - All example curl commands use http://localhost:5000

---

### **3️⃣ API Endpoints**
| **Method** | **Endpoint**                | **Description**                                     |
|------------|----------------------------|-----------------------------------------------------|
| `GET`      | `/health_status`           | Check if the API is running.                        |
| `GET`      | `/dealership_insights_home`| API welcome page with usage instructions.           |
| `POST`     | `/v1/predict`              | Predict car price using Model V1.                   |
| `POST`     | `/v2/predict`              | Predict car price using Model V2.                   |

---

### **4️⃣ Example Requests & Responses**

#### ✅ **Check API Health**
```bash
curl -X GET http://localhost:5000/health_status
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2023-11-15 12:34:56",
  "version": "1.0.0"
}
```

#### ✅ **Get API Documentation**
```bash
curl -X GET http://localhost:5000/dealership_insights_home
```

#### ✅ **Make a Prediction with Model V1**
```bash
curl -X POST http://localhost:5000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Toyota",
    "model": "Camry",
    "year": 2018,
    "mileage": 35000,
    "condition": "Excellent"
  }'
```

Response:
```json
{
  "model_version": "v1",
  "prediction": 18500.75,
  "input_data": {
    "make": "Toyota",
    "model": "Camry",
    "year": 2018,
    "mileage": 35000,
    "condition": "Excellent"
  }
}
```

#### ✅ **Make a Prediction with Model V2**
```bash
curl -X POST http://localhost:5000/v2/predict \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Honda",
    "model": "Accord",
    "year": 2020,
    "mileage": 15000,
    "condition": "Excellent"
  }'
```

Response:
```json
{
  "model_version": "v2",
  "prediction": 22750.50,
  "input_data": {
    "make": "Honda",
    "model": "Accord",
    "year": 2020,
    "mileage": 15000,
    "condition": "Excellent"
  }
}
```