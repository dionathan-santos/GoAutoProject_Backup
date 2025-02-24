import sys
import os
import pytest
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.clustering import ClusteringModel

def test_preprocess_used_cars():
    # Test data with at least 3 rows (for 3 clusters)
    data = pd.DataFrame({
        "avg_price": [20000, 25000, 30000, 35000],
        "avg_mileage": [50000, 60000, 70000, 80000]
    })
    
    clustering = ClusteringModel(n_clusters=3, random_state=42)  # Initialize model
    agg_data = clustering.train(data, ["avg_price", "avg_mileage"])  # Train model
    
    assert len(agg_data) == 4  # Ensure all rows are clustered
    assert "cluster" in agg_data.columns  # Check if 'cluster' column is added
