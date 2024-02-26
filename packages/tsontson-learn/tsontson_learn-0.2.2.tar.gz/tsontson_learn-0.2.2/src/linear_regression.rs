use numpy::{PyArray1, PyReadonlyArray2};
use pyo3::prelude::*;
use pyo3::Python;
use crate::matrix_ops::{Matrix, matmul, convert_array_to_matrix};



#[pyclass]
#[derive(Debug)]
pub struct PyLinearRegression {
    fit_intercept: bool,
    intercept: Option<f64>,
    slope: Option<Vec<f64>>,  // Assuming multiple regression, slope is a vector
}

#[pymethods]
impl PyLinearRegression {
    #[new]
    pub fn new(fit_intercept: bool) -> Self {
        PyLinearRegression {
            fit_intercept,
            intercept: None,
            slope: None,
        }
    }

    fn fit(&mut self, _py: Python, x: PyReadonlyArray2<f64>, y: PyReadonlyArray2<f64>) -> PyResult<()> {
        let mut x_matrix = convert_array_to_matrix(x);
        let y_matrix = convert_array_to_matrix(y);

        if self.fit_intercept {
            // Create a column of ones.
            let ones_matrix = Matrix::with_vector(vec![1.0; x_matrix.rows()], x_matrix.rows(), 1);
            
            // Horizontally stack the column of ones to x_matrix.
            x_matrix = match x_matrix.hstack(&ones_matrix) {
                Ok(result) => result,
                Err(e) => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(e)),
            };
        }
        
        let xt = x_matrix.transpose();
        let xtx = matmul(&xt, &x_matrix);
        let xtx_inv = xtx.inverse().map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Matrix inversion failed."))?;
        let xty = matmul(&xt, &y_matrix);
        let b = matmul(&xtx_inv, &xty);
        if self.fit_intercept {
            // If fitting intercept, the first element is the intercept, the rest are slope coefficients.
            self.intercept = Some(b.0.elements[0]);
            self.slope = Some(b.0.elements[1..].to_vec());
        } else {
            // If not fitting intercept, set intercept to 0.0 and all elements of b are slope coefficients.
            self.intercept = Some(0.0);
            self.slope = Some(b.0.elements.to_vec());
        }

        Ok(())
    }

    /// Predicts the y values for given x values using the learned regression coefficients.
    ///
    /// # Arguments
    /// * `x` - A 2D numpy array where each row represents a set of features for one observation.
    ///
    /// # Returns
    /// A numpy array of predicted y values.
    fn predict(&mut self, py: Python, x: PyReadonlyArray2<f64>) -> PyResult<Py<PyArray1<f64>>> {
        let x_matrix = convert_array_to_matrix(x);
        let intercept_val = self.intercept.unwrap_or(0.0);

        // Ensure that the slope is available and has the correct dimensions
        let slope = self.slope.as_ref().ok_or_else(|| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Model has not been fitted yet."))?;

        // Convert slope to a Matrix for multiplication
        let b_matrix = Matrix::with_vector(slope.clone(), slope.len(), 1);
        let y_matrix = matmul(&x_matrix, &b_matrix);

        // Add intercept to all y values if not included in slope
        let y_values: Vec<f64> = y_matrix.0.elements.iter().map(|&val| val + intercept_val).collect();

        // Convert the result back to a numpy array to return
        Ok(PyArray1::from_vec(py, y_values).to_owned())
    }

    #[getter]
    pub fn get_intercept(&self) -> Option<f64> {
        self.intercept
    }

    #[getter]
    pub fn get_slope(&self) -> Option<Vec<f64>> {
        self.slope.clone()
    }

}
