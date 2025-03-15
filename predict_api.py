from flask import Flask, request, jsonify
import pickle
import os
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# Project name
PROJECT_NAME = "dealership_insights"

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Create dummy models if they don't exist
def create_dummy_models():
    # Create a dummy model v1
    if not os.path.exists('models/model_v1.pkl'):
        model_v1 = RandomForestRegressor(n_estimators=10, random_state=42)
        # Fit with dummy data
        X = np.random.rand(100, 5)
        y = np.random.rand(100) * 50000  # Random car prices
        model_v1.fit(X, y)
        # Save model v1
        with open('models/model_v1.pkl', 'wb') as f:
            pickle.dump(model_v1, f)
        print("Created dummy model v1")
    
    # Create a slightly different model v2
    if not os.path.exists('models/model_v2.pkl'):
        model_v2 = RandomForestRegressor(n_estimators=20, random_state=42)
        # Fit with dummy data
        X = np.random.rand(100, 5)
        y = np.random.rand(100) * 50000  # Random car prices
        model_v2.fit(X, y)
        # Save model v2
        with open('models/model_v2.pkl', 'wb') as f:
            pickle.dump(model_v2, f)
        print("Created dummy model v2")

# Load models
def load_model(version):
    try:
        model_path = f"models/model_v{version}.pkl"
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None

# Home endpoint
@app.route(f"/{PROJECT_NAME}_home", methods=["GET"])
def home():
    return jsonify({
        "message": f"Welcome to the {PROJECT_NAME} API",
        "description": "This API provides car price prediction services",
        "endpoints": {
            "/v1/predict": "Prediction using model version 1",
            "/v2/predict": "Prediction using model version 2",
            "/health_status": "Check if the API is running"
        },
        "sample_payload": {
            "make": "Toyota",
            "model": "Camry",
            "year": 2018,
            "mileage": 35000,
            "condition": "Excellent"
        },
        "usage": "Send a POST request to /v1/predict or /v2/predict with the sample payload format"
    })

# Health status endpoint
@app.route("/health_status", methods=["GET"])
def health_status():
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    })

# V1 predict endpoint
@app.route("/v1/predict", methods=["POST"])
def predict_v1():
    model = load_model(1)
    
    # If model doesn't exist, return an error
    if model is None:
        return jsonify({
            "error": "Model v1 not found. Please ensure model_v1.pkl exists in the models directory."
        }), 404
    
    # Get data from request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        # Process input data - convert strings to numerical values
        features = [
            float(hash(data.get('make', '')) % 100),  # Convert make to a number
            float(hash(data.get('model', '')) % 100),  # Convert model to a number
            float(data.get('year', 0)),
            float(data.get('mileage', 0)),
            float(hash(data.get('condition', '')) % 10)  # Convert condition to a number
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        return jsonify({
            "model_version": "v1",
            "prediction": float(prediction),
            "input_data": data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# V2 predict endpoint
@app.route("/v2/predict", methods=["POST"])
def predict_v2():
    model = load_model(2)
    
    # If model doesn't exist, return an error
    if model is None:
        return jsonify({
            "error": "Model v2 not found. Please ensure model_v2.pkl exists in the models directory."
        }), 404
    
    # Get data from request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    try:
        # Process input data - convert strings to numerical values
        features = [
            float(hash(data.get('make', '')) % 100),  # Convert make to a number
            float(hash(data.get('model', '')) % 100),  # Convert model to a number
            float(data.get('year', 0)),
            float(data.get('mileage', 0)),
            float(hash(data.get('condition', '')) % 10)  # Convert condition to a number
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        return jsonify({
            "model_version": "v2",
            "prediction": float(prediction),
            "input_data": data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Create dummy models if they don't exist
    create_dummy_models()
    app.run(debug=True, host="0.0.0.0", port=5000)