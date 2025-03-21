# Dealership Insights API Guide

## API Configuration

### Port and Host
- **Port**: 5000
- **Host**: localhost (0.0.0.0)
- **Full URL**: http://localhost:5000

### Important Notes
- The API is configured to run on port 5000
- Do not attempt to change the port without modifying the source code
- All example commands use http://localhost:5000

## Endpoints Overview

### 1. Health Check
- **Endpoint**: `/health_status`
- **Method**: GET
- **Purpose**: Check if the API is running
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/health_status
  ```

### 2. API Documentation
- **Endpoint**: `/dealership_insights_home`
- **Method**: GET
- **Purpose**: Get API usage instructions and documentation
- **Example**:
  ```bash
  curl -X GET http://localhost:5000/dealership_insights_home
  ```

### 3. Model V1 Prediction
- **Endpoint**: `/v1/predict`
- **Method**: POST
- **Purpose**: Predict car price using Model V1
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/v1/predict \
    -H "Content-Type: application/json" \
    -d '{
      "make": "Toyota",
      "model": "Camry",
      "year": 2018,
      "mileage": 35000,
      "condition": "Excellent"
    }'
  ```

### 4. Model V2 Prediction
- **Endpoint**: `/v2/predict`
- **Method**: POST
- **Purpose**: Predict car price using Model V2
- **Example**:
  ```bash
  curl -X POST http://localhost:5000/v2/predict \
    -H "Content-Type: application/json" \
    -d '{
      "make": "Honda",
      "model": "Accord",
      "year": 2020,
      "mileage": 15000,
      "condition": "Excellent"
    }'
  ```

## Troubleshooting

### Common Issues
1. **Connection Refused**
   - Ensure the API is running
   - Verify you're using the correct port (5000)
   - Check that no other service is using port 5000

2. **Invalid JSON**
   - Ensure your request body matches the expected format
   - Use valid JSON syntax
   - Include all required fields

3. **Model Not Found**
   - Ensure dummy models are created before running the API
   - Check the `models/` directory for `model_v1.pkl` and `model_v2.pkl`

## Development Notes
- The API uses dummy models for demonstration
- In a production environment, replace dummy models with trained models
- Consider adding more robust error handling and logging