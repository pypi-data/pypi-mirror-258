use numpy::PyReadonlyArray2;
use strassen::matrix::Matrix as StrassenMatrix;
use strassen::par_mult::mult_transpose as from_strassen_matmul;

extern crate lapack_src;


pub struct Matrix(pub StrassenMatrix);

impl Matrix {

    pub fn new(rows: usize, cols: usize) -> Matrix {
        Matrix(StrassenMatrix::with_vector(vec![0.0; rows * cols], rows, cols))
    }

    pub fn is_square(&self) -> bool {
        self.0.rows == self.0.cols
    }

    pub fn identity(size: usize) -> Matrix {
        let mut elements = vec![0.0; size * size];
        for i in 0..size {
            elements[i * size + i] = 1.0;
        }
        Matrix::with_vector(elements, size, size)
    }

    // Forward substitution for solving Ly = b for y, where L is a lower triangular matrix
    fn forward_substitution(&self, b: &Matrix) -> Result<Matrix, &'static str> {
        if !self.is_square() || b.rows() != self.rows() {
            return Err("Invalid matrix dimensions for forward substitution.");
        }

        let n = self.rows();
        let mut y = vec![0.0; n];

        for i in 0..n {
            let mut sum = 0.0;
            for j in 0..i {
                sum += self.0.at(i, j) * y[j];
            }
            y[i] = (b.0.at(i, 0) - sum) / self.0.at(i, i);
        }

        Ok(Matrix(StrassenMatrix::with_vector(y, n, 1)))
    }

    // Backward substitution for solving Ux = y for x, where U is an upper triangular matrix
    fn backward_substitution(&self, y: &Matrix) -> Result<Matrix, &'static str> {
        if !self.is_square() || y.rows() != self.rows() {
            return Err("Invalid matrix dimensions for backward substitution.");
        }

        let n = self.rows();
        let mut x = vec![0.0; n];

        for i in (0..n).rev() {
            let mut sum = 0.0;
            for j in (i + 1)..n {
                sum += self.0.at(i, j) * x[j];
            }
            x[i] = (y.0.at(i, 0) - sum) / self.0.at(i, i);
        }

        Ok(Matrix(StrassenMatrix::with_vector(x, n, 1)))
    }

    pub fn inverse(&self) -> Result<Matrix, &'static str> {
        // Ensure the matrix is square
        if !self.is_square() {
            return Err("Matrix inversion requires a square matrix.");
        }

        // LU decomposition
        let (l, u) = self.lu_decompose()?;

        // The identity matrix for the forward and backward substitution
        let identity = Matrix::identity(self.0.rows);

        // Allocate space for the inverse matrix
        let mut inverse = Matrix::new(self.0.rows, self.0.cols);

        // Solve for each column of the inverse
        for i in 0..self.0.cols {
            let column = identity.extract_column(i)?;
            let y = l.forward_substitution(&column)?;
            let x = u.backward_substitution(&y)?;

            // Place x into the correct column of the inverse matrix
            inverse.set_column(i, &x)?;
        }

        Ok(inverse)
    }

    // Assuming you have methods to extract and set columns in a matrix
    fn extract_column(&self, index: usize) -> Result<Matrix, &'static str> {
        if index >= self.0.cols {
            return Err("Column index out of bounds.");
        }

        let mut column_elements = Vec::new();
        for i in 0..self.0.rows {
            column_elements.push(self.0.elements[i * self.0.cols + index]);
        }

        Ok(Matrix(StrassenMatrix::with_vector(column_elements, self.0.rows, 1)))
    }

    fn set_column(&mut self, index: usize, column: &Matrix) -> Result<(), &'static str> {
        if index >= self.0.cols || column.0.rows != self.0.rows || column.0.cols != 1 {
            return Err("Invalid dimensions for column set operation.");
        }

        for i in 0..self.0.rows {
            self.0.elements[i * self.0.cols + index] = column.0.elements[i];
        }

        Ok(())
    }
    // Utility function to convert a StrassenMatrix multiplication result into Matrix
    pub fn multiply(&self, other: &Matrix) -> Result<Matrix, &'static str> {
        // Check dimensions for multiplication compatibility
        if self.0.cols != other.0.rows {
            return Err("Matrix dimensions do not allow multiplication.");
        }

        // Use strassen multiplication function
        Ok(matmul(self, other))
    }

    pub fn lu_decompose(&self) -> Result<(Matrix, Matrix), &'static str> {
        if !self.is_square() {
            return Err("LU decomposition requires a square matrix.");
        }

        let n = self.0.rows;
        let mut l = Matrix(StrassenMatrix::new(n, n)); // Adjust to use StrassenMatrix constructor
        let mut u = Matrix(StrassenMatrix::new(n, n)); // Adjust to use StrassenMatrix constructor

        // Initialize L to be an identity matrix using StrassenMatrix methods/structure
        for i in 0..n {
            l.0.elements[i * n + i] = 1.0;
        }

        for i in 0..n {
            for j in i..n {
                let mut sum = 0.0;
                for k in 0..i {
                    sum += l.0.elements[i * n + k] * u.0.elements[k * n + j];
                }
                u.0.elements[i * n + j] = self.0.elements[i * n + j] - sum;
            }

            for j in i + 1..n {
                let mut sum = 0.0;
                for k in 0..i {
                    sum += l.0.elements[j * n + k] * u.0.elements[k * n + i];
                }
                if u.0.elements[i * n + i] == 0.0 {
                    return Err("Matrix is singular and cannot be decomposed.");
                }
                l.0.elements[j * n + i] = (self.0.elements[j * n + i] - sum) / u.0.elements[i * n + i];
            }
        }

        Ok((l, u))
    }

    pub fn transpose(&self) -> Matrix {
        let transposed = self.0.transpose();
        Matrix(transposed)
    }

    // Placeholder for with_vector, assuming similar to StrassenMatrix::with_vector
    pub fn with_vector(elements: Vec<f64>, rows: usize, cols: usize) -> Matrix {
        Matrix(StrassenMatrix::with_vector(elements, rows, cols))
    }

    pub fn rows(&self) -> usize {
        self.0.rows
    }

    /**
     * Horizontally concatenates this matrix with another matrix, b.
     * It appends the matrix b to the right side of this matrix.
     * This operation is only valid if both matrices have the same number of rows.
     */
    pub fn hstack(&self, b: &Matrix) -> Result<Matrix, &'static str> {
        if self.rows() != b.rows() {
            return Err("Matrix row counts do not match for horizontal stacking.");
        }

        let mut new_elements = Vec::with_capacity(self.rows() * (self.0.cols + b.0.cols));
        for i in 0..self.rows() {
            // Append row from the first matrix.
            new_elements.extend_from_slice(&self.0.elements[i * self.0.cols..(i + 1) * self.0.cols]);
            // Append row from the second matrix.
            new_elements.extend_from_slice(&b.0.elements[i * b.0.cols..(i + 1) * b.0.cols]);
        }

        Ok(Matrix(StrassenMatrix::with_vector(new_elements, self.rows(), self.0.cols + b.0.cols)))
    }

    //Not tested yet
    pub fn gauss_jordan_inverse(&mut self) -> Result<(), &'static str> {
        if !self.is_square() {
            return Err("Matrix must be square to invert");
        }
    
        let n = self.0.rows;
        let _result = self.0.copy();
        let mut identity = Matrix::new(n, n);
    
        for i in  0..n {
            identity.0.elements[i * n + i] =  1.0;
        }
    
        // Gauss-Jordan elimination
        for i in  0..n {
            let pivot = self.0.elements[i * n + i];
            if pivot ==  0.0 {
                return Err("Matrix is singular and cannot be inverted");
            }
    
            for j in  0..n {
                self.0.elements[i * n + j] /= pivot;
                identity.0.elements[i * n + j] /= pivot;
            }
    
            for j in  0..n {
                if j != i {
                    let ratio = self.0.elements[j * n + i];
                    for k in  0..n {
                        self.0.elements[j * n + k] -= ratio * self.0.elements[i * n + k];
                        identity.0.elements[j * n + k] -= ratio * identity.0.elements[i * n + k];
                    }
                }
            }
        }
    
        *self = identity; // The original matrix is now its inverse
        Ok(())
    }
    

}

// Assuming a function to convert StrassenMatrix multiplication to Matrix
pub fn matmul(a: &Matrix, b: &Matrix) -> Matrix {

    let result = from_strassen_matmul(&a.0, &b.0);

    Matrix(result)
}

pub fn convert_array_to_matrix(array: PyReadonlyArray2<f64>) -> Matrix {
    let array = array.as_array(); // Get ndarray view

    let elements: Vec<f64> = array.iter().copied().collect();
    let rows = array.nrows();
    let cols = array.ncols();

    Matrix(StrassenMatrix::with_vector(elements, rows, cols))
}





