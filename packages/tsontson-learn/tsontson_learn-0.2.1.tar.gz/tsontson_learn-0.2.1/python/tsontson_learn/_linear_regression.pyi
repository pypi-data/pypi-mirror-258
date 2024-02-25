# python/tsontson_learn_py/linear_regression.py

from typing import Union, List
import numpy as np
import pandas as pd
import tsontson_learn

class LinearRegression:
    def __init__(self, fit_intercept: bool = True):
        self.model = tsontson_learn.LinearRegression(fit_intercept)

    def fit(self, X: Union[np.ndarray, pd.DataFrame, List[List[float]]], y: Union[np.ndarray, pd.Series, List[float]]) -> None:
        X_np, y_np = self._convert_inputs(X, y)
        self.model.fit(X_np, y_np)

    def predict(self, X: Union[np.ndarray, pd.DataFrame, List[List[float]]]) -> np.ndarray:
        X_np, _ = self._convert_inputs(X, None)
        return self.model.predict(X_np)

    @staticmethod
    def _convert_inputs(X: Union[np.ndarray, pd.DataFrame, List[List[float]]], y: Union[np.ndarray, pd.Series, List[float], None]) -> tuple:
        if isinstance(X, pd.DataFrame):
            X_np = X.to_numpy().astype(np.float64)
        elif isinstance(X, list):
            X_np = np.array(X).astype(np.float64)
        else:
            X_np = X

        y_np = None
        if y is not None:
            if isinstance(y, pd.Series):
                y_np = y.to_numpy()
            elif isinstance(y, list):
                y_np = np.array(y)
            else:
                y_np = y

        return X_np, y_np
