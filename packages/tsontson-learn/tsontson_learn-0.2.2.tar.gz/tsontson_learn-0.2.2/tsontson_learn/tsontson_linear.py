# python/tsontson_linear_py/linear_regression.py

from typing import Union, Iterable, List
import numpy as np
import pandas as pd


class LinearRegression:
    def __init__(self, fit_intercept: bool = True):
        from tsontson_learn.tsontson_learn import PyLinearRegression
        self.model = PyLinearRegression(fit_intercept)

    @property
    def intercept(self):
        return self.model.intercept

    @property
    def coeffs(self):
        return self.model.slope

    def fit(self, X: Union[np.ndarray, pd.DataFrame, List[List[float]]], y: Union[np.ndarray, pd.Series, List[float]]) -> None:
        X_np, y_np = self._convert_inputs(X, y)
        self.model.fit(X_np, y_np)

    def predict(self, X: Union[np.ndarray, pd.DataFrame, List[List[float]]]) -> np.ndarray:
        X_np, _ = self._convert_inputs(X, None)
        return self.model.predict(X_np)

    @staticmethod
    def _convert_inputs(X: Union[np.ndarray, pd.DataFrame, List[List[float]]], 
                        y: Union[np.ndarray, pd.Series, List[float], None]) -> tuple:
        # Type checking and conversion for X
        if isinstance(X, np.ndarray):
            X_np = X.astype(np.float64)
        elif isinstance(X, pd.DataFrame):
            X_np = X.to_numpy().astype(np.float64)
        elif isinstance(X, List) or all(isinstance(xi, Iterable) for xi in X):
            X_np = np.array(X, dtype=np.float64)
        else:
            raise TypeError(f"X is {type(X)} while only pandas DataFrame, numpy array, and iterable of iterable are supported")

        # Initialization of y_np
        y_np = None
        
        # Type checking and conversion for y if it is not None
        if y is not None:
            if isinstance(y, np.ndarray):
                y_np = y.astype(np.float64)
            elif isinstance(y, pd.Series):
                y_np = y.to_numpy().astype(np.float64)
            elif isinstance(y, pd.DataFrame):
                if y.shape[1] > 1:
                    raise TypeError(f"y received has {y.shape[1]} columns while expected is one")
                y_np = y.iloc[:, 0].to_numpy().astype(np.float64)
            elif isinstance(y, List) or all(isinstance(yi, (float, int)) for yi in y):
                y_np = np.array(y, dtype=np.float64)
            else:
                raise TypeError(f"y is {type(y)} while only pandas DataFrame, Series, numpy array, and iterable are supported")
        return X_np, np.expand_dims(y_np, axis=1) if y_np is not None else y_np
