import pytest
import os
import joblib
from model.train import clustering

def test_train_model():
    """Test if the training script saves the model correctly."""
    # Ensure model files exist
    assert os.path.exists("model/checkpoints/kmeans_model.pkl")
    assert os.path.exists("model/checkpoints/scaler.pkl")

    # Load saved models
    kmeans = joblib.load("model/checkpoints/kmeans_model.pkl")
    scaler = joblib.load("model/checkpoints/scaler.pkl")

    # Ensure models are not None
    assert kmeans is not None
    assert scaler is not None

    print("✅ Model training test passed!")
