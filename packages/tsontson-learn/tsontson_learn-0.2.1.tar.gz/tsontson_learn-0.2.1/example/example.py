# example/example.py

from tsontson_learn_py.linear_regression import LinearRegression
import pandas as pd

# Create some sample data
df = pd.DataFrame({
    'X': [1, 2, 3, 4],
    'y': [2, 3, 4, 5]
})

# Split the data into features and target
X = df[['X']]  # DataFrame for features
y = df['y']    # Series for target

# Initialize and train the model
model = LinearRegression(fit_intercept=True)
model.fit(X, y)

# Make predictions
X_new = pd.DataFrame({'X': [5, 6]})
predictions = model.predict(X_new)

print("Predictions:", predictions)
