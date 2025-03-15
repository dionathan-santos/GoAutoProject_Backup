import requests

# Test health endpoint
response = requests.get("http://localhost:5000/health_status")
print("Health Status Response:", response.json())

# Test home endpoint
response = requests.get("http://localhost:5000/dealership_insights_home")
print("Home Endpoint Raw Response:", response.text)
try:
    print("Home Endpoint JSON Response:", response.json())
except Exception as e:
    print("Error parsing home endpoint JSON:", str(e))

# Test v1 predict endpoint
data = {
    "make": "Toyota",
    "model": "Camry",
    "year": 2018,
    "mileage": 35000,
    "condition": "Excellent"
}
response = requests.post("http://localhost:5000/v1/predict", json=data)
print("V1 Predict Raw Response:", response.text)
try:
    print("V1 Predict JSON Response:", response.json())
except Exception as e:
    print("Error parsing V1 predict JSON:", str(e))

# Test v2 predict endpoint
data = {
    "make": "Honda",
    "model": "Accord",
    "year": 2020,
    "mileage": 15000,
    "condition": "Excellent"
}
response = requests.post("http://localhost:5000/v2/predict", json=data)
print("V2 Predict Raw Response:", response.text)
try:
    print("V2 Predict JSON Response:", response.json())
except Exception as e:
    print("Error parsing V2 predict JSON:", str(e))