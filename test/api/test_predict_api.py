import pytest
import json
import requests
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_status():
    """
    Test the health status endpoint
    """
    response = requests.get(f"{BASE_URL}/health_status")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_home_endpoint():
    """
    Test the home endpoint
    """
    response = requests.get(f"{BASE_URL}/dealership_insights_home")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "endpoints" in data

def test_predict_v1_endpoint():
    """
    Test the V1 prediction endpoint
    """
    payload = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2018,
        "mileage": 35000,
        "condition": "Excellent"
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/predict", 
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "model_version" in data
    assert data["model_version"] == "v1"
    assert "prediction" in data
    assert "input_data" in data
    assert isinstance(data["prediction"], float)

def test_predict_v2_endpoint():
    """
    Test the V2 prediction endpoint
    """
    payload = {
        "make": "Honda",
        "model": "Accord",
        "year": 2020,
        "mileage": 15000,
        "condition": "Excellent"
    }
    
    response = requests.post(
        f"{BASE_URL}/v2/predict", 
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "model_version" in data
    assert data["model_version"] == "v2"
    assert "prediction" in data
    assert "input_data" in data
    assert isinstance(data["prediction"], float)

def test_predict_invalid_payload():
    """
    Test prediction with invalid payload
    """
    # Missing required fields
    payload = {
        "make": "Toyota"
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/predict", 
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    # Expect a 500 or 400 error for invalid input
    assert response.status_code in [400, 500]

def test_predict_empty_payload():
    """
    Test prediction with empty payload
    """
    response = requests.post(
        f"{BASE_URL}/v1/predict", 
        json={},
        headers={"Content-Type": "application/json"}
    )
    
    # Expect a 400 error for empty payload
    assert response.status_code == 400