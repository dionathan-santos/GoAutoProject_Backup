import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from opencage.geocoder import OpenCageGeocode

# Load configuration
with open("configs/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Constants from config
CSV_FILE = config["paths"]["data"] + "CBB_Listings_LongLat.csv"
API_KEY = config["api"]["opencage_key"]

def load_data(file_path):
    """
    Loads the dataset from the specified file path.
    """
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

def display_basic_stats(df):
    """
    Displays basic stats about the dataset.
    """
    if df is not None:
        print("Shape of the dataset:", df.shape)
        print("\nStatistical Summary:")
        print(df.describe())
    else:
        print("No data available.")

def geocode_addresses(df, column_name, api_key):
    """
    Geocodes addresses in the specified column of the DataFrame.
    Requires a valid OpenCage API key.
    """
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in DataFrame.")
        return df

    geocoder = OpenCageGeocode(api_key)
    coordinates = []

    for idx, address in enumerate(df[column_name]):
        try:
            result = geocoder.geocode(address)
            if result:
                lat, lng = result[0]["geometry"]["lat"], result[0]["geometry"]["lng"]
                coordinates.append((lat, lng))
            else:
                coordinates.append((None, None))
        except Exception as e:
            print(f"Error geocoding {address}: {e}")
            coordinates.append((None, None))

        # Progress feedback every 10 rows
        if idx % 10 == 0:
            print(f"Processed {idx}/{len(df)} addresses.")

    df["Latitude"], df["Longitude"] = zip(*coordinates)
    print("Geocoding completed.")
    return df

def plot_data(df, column):
    """
    Generates and displays a histogram for the specified column.
    """
    if column in df.columns:
        sns.histplot(df[column], kde=True)
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.show()
    else:
        print(f"Column {column} not found in DataFrame.")

if __name__ == "__main__":
    # Load dataset
    data = load_data(CSV_FILE)

    # Display basic stats
    display_basic_stats(data)

    # Example: Geocode addresses (replace 'address_column' with actual column name)
    # if data is not None:
    #     data = geocode_addresses(data, "address_column", API_KEY)

    # Plot data
    if data is not None and "price" in data.columns:
        plot_data(data, "price")
    else:
        print("The column 'price' is missing or data could not be loaded.")
