# example/example.py
import sys
import os
sys.path.append(os.getcwd().replace('/example',''))


from tsontson_learn import LinearRegression
import pandas as pd
import numpy as np

n_features = 5
n_rows = 1000

# Create some sample data
df = pd.DataFrame(data = np.random.randn(n_rows, n_features + 1).astype(np.float64), columns = ['y'] + [f'X_{i}' for i in range(n_features)])

# Split the data into features and target
X = df[[c for c in df.columns if "X" in c]]  # DataFrame for features
y = df['y']    # Series for target

# Initialize and train the model
model = LinearRegression(fit_intercept=True)
model.fit(X, y)
print(f"fitted successfully, intercept is {model.intercept} and coeffs are {model.coeffs}")

# Make predictions
X_new = pd.DataFrame(np.random.randn(n_rows, n_features), columns = [f'X_{i}' for i in range(n_features)])
predictions = model.predict(X_new)

print("Predictions:", predictions)
