import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Create a dummy model v1
model_v1 = RandomForestRegressor(n_estimators=10, random_state=42)
# Fit with dummy data
X = np.random.rand(100, 5)
y = np.random.rand(100) * 50000  # Random car prices

model_v1.fit(X, y)

# Save model v1
with open('models/model_v1.pkl', 'wb') as f:
    pickle.dump(model_v1, f)

# Create a slightly different model v2
model_v2 = RandomForestRegressor(n_estimators=20, random_state=42)
model_v2.fit(X, y)

# Save model v2
with open('models/model_v2.pkl', 'wb') as f:
    pickle.dump(model_v2, f)

print("Dummy models created successfully!")