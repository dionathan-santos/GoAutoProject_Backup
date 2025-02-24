# Importing Required Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from opencage.geocoder import OpenCageGeocode
from pprint import pprint
import yaml

# Load YAML configuration
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["api"]["opencage_key"]
geocoder = OpenCageGeocode(API_KEY)

# ✅ Function to Load Data
def load_csv(file_path):
    """Loads a CSV file into a Pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Successfully loaded {file_path} with {df.shape[0]} rows.")
        return df
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

# ✅ Function to Geocode Address
def geocode_address(address):
    """Converts an address into latitude and longitude."""
    try:
        result = geocoder.geocode(address)
        if result:
            lat, lon = result[0]["geometry"]["lat"], result[0]["geometry"]["lng"]
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f"❌ Geocoding error: {e}")
        return None, None

# ✅ Function to Plot Data Distribution
def plot_distribution(df, column):
    """Plots the distribution of a numerical column."""
    plt.figure(figsize=(8, 5))
    sns.histplot(df[column], bins=30, kde=True)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.show()
