pub mod matrix_ops;
mod linear_regression;


use pyo3::prelude::*;

#[pymodule]
fn tsontson_learn(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<linear_regression::PyLinearRegression>()?;
    Ok(())
}
