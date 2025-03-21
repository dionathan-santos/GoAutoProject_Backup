import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the functions to test
from src.data_analysis import load_data, display_basic_stats

def test_load_data():
    """
    Test the load_data function
    """
    # Create a temporary CSV file for testing
    test_data = pd.DataFrame({
        'make': ['Toyota', 'Honda', 'Ford'],
        'model': ['Camry', 'Civic', 'Mustang'],
        'year': [2018, 2019, 2020],
        'price': [25000, 22000, 35000]
    })
    
    # Save the test data to a temporary file
    test_file_path = 'test_data.csv'
    test_data.to_csv(test_file_path, index=False)
    
    try:
        # Test loading the data
        loaded_data = load_data(test_file_path)
        
        # Assertions
        assert loaded_data is not None
        assert isinstance(loaded_data, pd.DataFrame)
        assert len(loaded_data) == 3
        assert list(loaded_data.columns) == ['make', 'model', 'year', 'price']
    
    finally:
        # Clean up the temporary file
        os.remove(test_file_path)

def test_load_data_file_not_found():
    """
    Test loading a non-existent file
    """
    # Capture print output
    import io
    import sys
    
    # Redirect stdout to capture print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Attempt to load a non-existent file
    result = load_data('non_existent_file.csv')
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Assertions
    assert result is None
    assert "Error: File non_existent_file.csv not found." in captured_output.getvalue()

def test_display_basic_stats():
    """
    Test the display_basic_stats function
    """
    # Create a test DataFrame
    test_data = pd.DataFrame({
        'price': [25000, 22000, 35000, 30000, 28000],
        'year': [2018, 2019, 2020, 2017, 2019]
    })
    
    # Capture print output
    import io
    import sys
    
    # Redirect stdout to capture print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Call the function
    display_basic_stats(test_data)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Get the captured output
    output = captured_output.getvalue()
    
    # Assertions
    assert "Shape of the dataset: (5, 2)" in output
    assert "Statistical Summary:" in output

def test_display_basic_stats_none():
    """
    Test display_basic_stats with None input
    """
    # Capture print output
    import io
    import sys
    
    # Redirect stdout to capture print statements
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    # Call the function with None
    display_basic_stats(None)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    # Get the captured output
    output = captured_output.getvalue()
    
    # Assertions
    assert "No data available." in output