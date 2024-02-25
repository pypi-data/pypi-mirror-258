use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::PyResult;
use numpy::{PyArray1, PyReadonlyArray1};

#[pyclass]
#[derive(Debug)]
pub struct LinearRegression {
    fit_intercept: bool,
    intercept_f64: Option<f64>,
    intercept_f32: Option<f32>,
    slope_f64: Option<f64>,
    slope_f32: Option<f32>,
}

#[pymethods]
impl LinearRegression {
    #[new]
    pub fn new(fit_intercept: bool) -> Self {
        LinearRegression {
            fit_intercept,
            intercept_f64: None,
            intercept_f32: None,
            slope_f64: None,
            slope_f32: None,
        }
    }

    pub fn fit(&mut self, x: &PyAny, y: &PyAny) -> PyResult<()> {
        if let Ok(x_array) = x.extract::<PyReadonlyArray1<f64>>() {
            let y_array = y.extract::<PyReadonlyArray1<f64>>()?;
            self.fit_f64(x_array, y_array);
        } else if let Ok(x_array) = x.extract::<PyReadonlyArray1<f32>>() {
            let y_array = y.extract::<PyReadonlyArray1<f32>>()?;
            self.fit_f32(x_array, y_array);
        } else {
            return Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "x and y must be numpy arrays of float32 or float64.",
            ));
        }
        Ok(())
    }

    fn fit_f64(&mut self, x: PyReadonlyArray1<f64>, y: PyReadonlyArray1<f64>) {
        let x_vec: Vec<f64> = x.to_vec().unwrap();
        let y_vec: Vec<f64> = y.to_vec().unwrap();

        if self.fit_intercept {
            // Calculate means for intercept
            let x_mean: f64 = x_vec.iter().sum::<f64>() / x_vec.len() as f64;
            let y_mean: f64 = y_vec.iter().sum::<f64>() / y_vec.len() as f64;

            let numerator: f64 = x_vec.iter().zip(&y_vec).map(|(&x_i, &y_i)| (x_i - x_mean) * (y_i - y_mean)).sum();
            let denominator: f64 = x_vec.iter().map(|&x_i| (x_i - x_mean).powi(2)).sum();

            let slope = numerator / denominator;
            let intercept = y_mean - slope * x_mean;

            self.slope_f64 = Some(slope);
            self.intercept_f64 = Some(intercept);
        } else {
            // If not fitting intercept, calculate slope directly
            let slope = y_vec.iter().zip(&x_vec).map(|(&y_i, &x_i)| y_i * x_i).sum::<f64>()
                / x_vec.iter().map(|&x_i| x_i * x_i).sum::<f64>();
            
            self.slope_f64 = Some(slope);
            self.intercept_f64 = Some(0.0); // No intercept
        }
    }

    fn fit_f32(&mut self, x: PyReadonlyArray1<f32>, y: PyReadonlyArray1<f32>) {
        let x_vec: Vec<f32> = x.to_vec().unwrap();
        let y_vec: Vec<f32> = y.to_vec().unwrap();

        if self.fit_intercept {
            // Calculate means for intercept
            let x_mean: f32 = x_vec.iter().sum::<f32>() / x_vec.len() as f32;
            let y_mean: f32 = y_vec.iter().sum::<f32>() / y_vec.len() as f32;

            let numerator: f32 = x_vec.iter().zip(&y_vec).map(|(&x_i, &y_i)| (x_i - x_mean) * (y_i - y_mean)).sum();
            let denominator: f32 = x_vec.iter().map(|&x_i| (x_i - x_mean).powi(2)).sum();

            let slope = numerator / denominator;
            let intercept = y_mean - slope * x_mean;

            self.slope_f32 = Some(slope);
            self.intercept_f32 = Some(intercept);
        } else {
            // If not fitting intercept, calculate slope directly
            let slope = y_vec.iter().zip(&x_vec).map(|(&y_i, &x_i)| y_i * x_i).sum::<f32>()
                / x_vec.iter().map(|&x_i| x_i * x_i).sum::<f32>();
            
            self.slope_f32 = Some(slope);
            self.intercept_f32 = Some(0.0); // No intercept
        }
    }

    pub fn predict(&self, x: &PyAny) -> PyResult<PyObject> {
        pyo3::Python::with_gil(|py| {
            // Predict with f64 data
            if let Ok(x_array) = x.extract::<PyReadonlyArray1<f64>>() {
                if let (Some(slope), Some(intercept)) = (self.slope_f64, self.intercept_f64) {
                    let x_vec: Vec<f64> = x_array.to_vec().unwrap();
                    let predictions: Vec<f64> = x_vec.iter().map(|&x_i| slope * x_i + intercept).collect();
                    // Convert predictions to a NumPy array and return
                    let predictions_array = PyArray1::from_vec(py, predictions);
                    return Ok(predictions_array.to_object(py));
                } else {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Model has not been fitted with float64 data.",
                    ));
                }
            }

            // Predict with f32 data
            if let Ok(x_array) = x.extract::<PyReadonlyArray1<f32>>() {
                if let (Some(slope), Some(intercept)) = (self.slope_f32, self.intercept_f32) {
                    let x_vec: Vec<f32> = x_array.to_vec().unwrap();
                    let predictions: Vec<f32> = x_vec.iter().map(|&x_i| slope * x_i + intercept).collect();
                    // Convert predictions to a NumPy array and return
                    let predictions_array = PyArray1::from_vec(py, predictions);
                    return Ok(predictions_array.to_object(py));
                } else {
                    return Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                        "Model has not been fitted with float32 data.",
                    ));
                }
            }

            // If the input is neither f32 nor f64 NumPy array
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "x must be a numpy array of float32 or float64.",
            ))
        })
    }

}
#[pymodule]
fn tsontson_learn(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<LinearRegression>()?;
    Ok(())
}
