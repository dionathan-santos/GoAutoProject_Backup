import sys
import os
import pytest
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def generate_synthetic_car_data(n_samples=1000):
    """
    Generate synthetic car sales data for testing
    """
    np.random.seed(42)
    
    # Synthetic features
    makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW']
    models = ['Camry', 'Civic', 'F-150', 'Malibu', '3 Series']
    conditions = ['Poor', 'Fair', 'Good', 'Excellent']
    
    data = {
        'make': np.random.choice(makes, n_samples),
        'model': np.random.choice(models, n_samples),
        'year': np.random.randint(2010, 2023, n_samples),
        'mileage': np.random.randint(0, 200000, n_samples),
        'condition': np.random.choice(conditions, n_samples)
    }
    
    # Generate synthetic price based on features
    base_price = 20000
    price_factors = {
        'Toyota': 1.2, 'Honda': 1.1, 'Ford': 1.0, 
        'Chevrolet': 0.9, 'BMW': 1.5
    }
    condition_factors = {
        'Poor': 0.6, 'Fair': 0.8, 'Good': 1.0, 'Excellent': 1.2
    }
    
    prices = []
    for i in range(n_samples):
        make_factor = price_factors.get(data['make'][i], 1.0)
        condition_factor = condition_factors.get(data['condition'][i], 1.0)
        
        price = (base_price + 
                 (data['year'][i] - 2010) * 1000 * make_factor - 
                 data['mileage'][i] * 0.1 * condition_factor)
        
        prices.append(max(5000, min(price, 100000)))  # Bound the price
    
    data['price'] = prices
    
    return pd.DataFrame(data)

def test_model_training_and_prediction():
    """
    Integration test for model training and prediction pipeline
    """
    # Generate synthetic data
    df = generate_synthetic_car_data()
    
    # Prepare features and target
    def preprocess_features(df):
        # Convert categorical features to numerical
        features = pd.DataFrame({
            'make_encoded': [hash(make) % 100 for make in df['make']],
            'model_encoded': [hash(model) % 100 for model in df['model']],
            'year': df['year'],
            'mileage': df['mileage'],
            'condition_encoded': [hash(condition) % 10 for condition in df['condition']]
        })
        return features
    
    X = preprocess_features(df)
    y = df['price']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Save the model
    with open('models/test_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Assertions
    assert mse < 10000  # Mean squared error should be reasonable
    assert r2 > 0.5     # R-squared should indicate decent model performance
    
    # Test model loading and prediction
    with open('models/test_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    
    # Make a single prediction
    test_input = X_test.iloc[0].to_frame().T
    prediction = loaded_model.predict(test_input)[0]
    
    assert isinstance(prediction, float)
    assert prediction > 0

def test_model_robustness():
    """
    Test model's performance with various input scenarios
    """
    # Generate synthetic data
    df = generate_synthetic_car_data()
    
    # Prepare features and target
    def preprocess_features(df):
        features = pd.DataFrame({
            'make_encoded': [hash(make) % 100 for make in df['make']],
            'model_encoded': [hash(model) % 100 for model in df['model']],
            'year': df['year'],
            'mileage': df['mileage'],
            'condition_encoded': [hash(condition) % 10 for condition in df['condition']]
        })
        return features
    
    X = preprocess_features(df)
    y = df['price']
    
    # Train a model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Test scenarios
    test_scenarios = [
        # Normal case
        [50, 30, 2018, 50000, 5],
        # Low mileage, new car
        [20, 10, 2022, 5000, 9],
        # High mileage, old car
        [80, 70, 2010, 180000, 2],
        # Extreme values
        [99, 99, 2000, 250000, 1]
    ]
    
    for scenario in test_scenarios:
        prediction = model.predict([scenario])[0]
        
        # Basic sanity checks
        assert isinstance(prediction, float)
        assert prediction > 0
        assert prediction < 200000  # Reasonable upper bound