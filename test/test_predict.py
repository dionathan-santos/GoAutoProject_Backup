import pytest
import joblib
import pandas as pd
from model.prediction import predict_used_car_region

# Load trained model and scaler
kmeans = joblib.load("model/checkpoints/kmeans_model.pkl")
scaler = joblib.load("model/checkpoints/scaler.pkl")

# Sample aggregated data for testing
agg_data = pd.DataFrame({
    "region_label": ["Region1", "Region2", "Region3"],
    "total_sales": [500, 600, 700],
    "cluster": [0, 1, 2]
})

def test_predict_used_car_region():
    """Test the prediction function for used cars."""
    result = predict_used_car_region(25000, 60000)
    
    # Ensure output is a DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Ensure required columns exist
    assert "region_label" in result.columns
    assert "total_sales" in result.columns

    print("✅ `predict_used_car_region` passed all tests!")
