import numpy as np
from tsontson_learn import LinearRegression

# Original X is a 2D array.
X = np.array([[1], [2], [3], [4]], dtype=np.float64)
# Flatten X to a 1D array for compatibility with Rust code.
X_flat = X.flatten()

y = np.array([2, 4, 6, 8], dtype=np.float64)

lr = LinearRegression(fit_intercept=True)
# Use the flattened X array.
lr.fit(X_flat, y)
predictions = lr.predict(X_flat)

print(predictions)

