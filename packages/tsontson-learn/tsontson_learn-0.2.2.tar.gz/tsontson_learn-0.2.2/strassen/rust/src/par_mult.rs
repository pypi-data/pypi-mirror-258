pub use crate::matrix::Matrix;
pub use crate::mult::*;

use threadpool::ThreadPool;
use std::sync::{Arc, Mutex};

static mut TEST_STATE:bool = false;

/**
 * Strassen algorithm. See https://en.wikipedia.org/wiki/Strassen_algorithm
 * Breaks the provided matrices down into 7 smaller submatrices for multiplication, which results in 
 * smaller asymptotic complexity of around O(n^2.8), at the expense of a higher scalar constant due to the extra work required.
 * Falls back to the transpose naive multiplication method if row and column dimensions are 64 or less.
 * Recurses as input matrices are broken down and this algorithm is run further on those submatrices.
 * Panics if matrices `a` and `b` are of incompatbile dimensions.
 */
fn nearest_power_of_two(x: usize) -> usize {
    let mut result = 1;
    while result < x {
        result <<= 1;
    }
    result
}

pub fn mult_par_strassen(a: &Matrix, b: &Matrix) -> Matrix {
    assert_eq!(a.cols, b.rows, "Matrix sizes do not match for multiplication.");

    // Adjust each dimension individually to the nearest power of two.
    let a_rows_padded = nearest_power_of_two(a.rows);
    let a_cols_padded = nearest_power_of_two(a.cols);
    let b_cols_padded = nearest_power_of_two(b.cols);

    let pool = ThreadPool::new(7);

    // Padding matrices to enable use of the Strassen algorithm
    let a_padded = a.pad(a_rows_padded, a_cols_padded);
    let b_padded = b.pad(a_cols_padded, b_cols_padded); // b's rows should match a's cols after padding

    let result_padded = _mult_par_strassen(&a_padded, &b_padded, &pool);
    
    // Reduce the padded result to the original intended dimensions.
    result_padded.reduce(a.rows, b.cols)
}
/**
 * Inner parallel Strassen algorithm logic. 
 */
fn _mult_par_strassen(a: &Matrix, b: &Matrix, pool: &ThreadPool) -> Matrix {
    if a.rows <= 64 {
        return mult_transpose(a, b);
    }

    let n = a.rows;
    let (a11, a12, a21, a22) = a.subdivide();
    let (b11, b12, b21, b22) = b.subdivide();

    let results = (0..7).map(|_| Arc::new(Mutex::new(None))).collect::<Vec<_>>();

    // Launch parallel computation for each of the 7 multiplications
    strassen_parallel_compute(&a11, &a22, &b11, &b22, &results[0], pool, true, true);
    strassen_parallel_compute(&a21, &a22, &b11, &b11, &results[1], pool, true, false);
    strassen_parallel_compute(&a11, &a11, &b12, &b22, &results[2], pool, false, true);
    strassen_parallel_compute(&a22, &a22, &b21, &b11, &results[3], pool, true, false);
    strassen_parallel_compute(&a11, &a12, &b22, &b22, &results[4], pool, true, false);
    strassen_parallel_compute(&a21, &a11, &b11, &b12, &results[5], pool, true, true);
    strassen_parallel_compute(&a12, &a22, &b21, &b22, &results[6], pool, true, true);

    pool.join();

    // Combine the results
    // Assuming this is inside your `_mult_par_strassen` or a similar function
    let c11 = combine_results_for_c(&results, 0, 3, 4, 6);
    let c12 = combine_two_results(&results[2], &results[4], false);
    let c21 = combine_two_results(&results[1], &results[3], false);
    let c22 = combine_results_for_c(&results, 0, 1, 2, 5);


    Matrix::combine_quadrants(&c11, &c12, &c21, &c22, n)
}

// Helper function to execute Strassen's multiplication steps in parallel
fn strassen_parallel_compute(
    a1: &Matrix, 
    a2: &Matrix, 
    b1: &Matrix, 
    b2: &Matrix, 
    result: &Arc<Mutex<Option<Matrix>>>, 
    pool: &ThreadPool,
    subtract_b: bool,
    add_a: bool
) {
    let res_clone = result.clone();

    let a_res = if add_a {
        let mut temp = a1.clone();
        temp.add(&a2);
        temp
    } else {
        a1.clone()
    };

    let b_res = if subtract_b {
        let mut temp = b1.clone();
        temp.sub(&b2);
        temp
    } else {
        b1.clone()
    };

    pool.execute(move || {
        let result = mult_strassen(&a_res, &b_res);
        *res_clone.lock().unwrap() = Some(result);
    });
}
fn combine_results_for_c(
    results: &[Arc<Mutex<Option<Matrix>>>], 
    idx1: usize, 
    idx2: usize, 
    idx3: usize, 
    idx4: usize,
) -> Matrix {
    let lock1 = results[idx1].lock().unwrap();
    let m1 = lock1.as_ref().unwrap();

    let lock2 = results[idx2].lock().unwrap();
    let m2 = lock2.as_ref().unwrap();

    let lock3 = results[idx3].lock().unwrap();
    let m3 = lock3.as_ref().unwrap();

    let lock4 = results[idx4].lock().unwrap();
    let m4 = lock4.as_ref().unwrap();

    let mut c = m1.clone();
    c.add(m4).sub(m3).add(m2);
    c
}


fn combine_two_results(
    res1: &Arc<Mutex<Option<Matrix>>>, 
    res2: &Arc<Mutex<Option<Matrix>>>,
    is_subtract: bool
) -> Matrix {
    let lock1 = res1.lock().unwrap();
    let m1 = lock1.as_ref().unwrap();

    let lock2 = res2.lock().unwrap();
    let m2 = lock2.as_ref().unwrap();

    let mut c = m1.clone();
    if is_subtract {
        c.sub(m2);
    } else {
        c.add(m2);
    }
    c
}


/**
 * Execute a recursive strassen multiplication of the given vectors, from a thread contained
 * within the provided thread pool.
 */
fn 
_par_run_strassen (a: Vec<f64>, b: Vec<f64>, 
                   m: usize, pool: &ThreadPool) 
                     -> Arc<Mutex<Option<Matrix>>> {
    let m1: Arc<Mutex<Option<Matrix>>> = Arc::new(Mutex::new(None));
    let m1_clone = Arc::clone(&m1);
     
    pool.execute(move|| { 
        // Use non-parallel algorithm once we're in a working thread
        let result = mult_strassen(
            &mut Matrix::with_vector(a, m, m),
            &mut Matrix::with_vector(b, m, m)
        );
        
        *m1_clone.lock().unwrap() = Some(result);
    });

    return m1;
}

#[cfg(test)]
mod tests {

    use rand::Rng;

    use super::*;

    fn test_multiplication_outputs (multipler: fn(&Matrix, &Matrix) -> Matrix) {
        let v1: Vec<f64> = vec![12.0, 8.0, 4.0, 3.0, 17.0, 14.0, 9.0, 8.0, 10.0];
        let v2: Vec<f64> = vec![5.0, 19.0, 3.0, 6.0, 15.0, 9.0, 7.0, 8.0, 16.0];
        let v3: Vec<f64> = vec![136.0, 380.0, 172.0, 215.0, 424.0, 386.0, 163.0, 371.0, 259.0];

        let a: Matrix = Matrix::with_vector(v1, 3, 3);
        let b: Matrix = Matrix::with_vector(v2, 3, 3);
        let c: Matrix = Matrix::with_vector(v3, 3, 3);

        assert!(a.mult(&b, multipler).eq(&c));

        let v4: Vec<f64> = vec![7.0, 14.0, 15.0, 6.0, 4.0, 8.0, 12.0, 3.0, 14.0, 21.0, 6.0, 9.0, 13.0, 7.0, 6.0, 4.0];
        let v5: Vec<f64> = vec![5.0, 7.0, 14.0, 2.0, 8.0, 16.0, 4.0, 9.0, 13.0, 6.0, 8.0, 4.0, 6.0, 3.0, 2.0, 4.0];
        let v6: Vec<f64> = vec![378.0, 381.0, 286.0, 224.0, 258.0, 237.0, 190.0, 140.0, 370.0, 497.0, 346.0, 277.0, 223.0, 251.0, 266.0, 129.0];

        let d: Matrix = Matrix::with_vector(v4, 4, 4);
        let e: Matrix = Matrix::with_vector(v5, 4, 4);
        let f: Matrix = Matrix::with_vector(v6, 4, 4);

        assert!(d.mult(&e, multipler).eq(&f));
    }

    #[test]
    fn test_mult_par_strassen () {
        unsafe {
            TEST_STATE = true;
        }

        test_multiplication_outputs(mult_par_strassen);
    }

    #[test]
    fn test_mult_par_aggregate () {
        unsafe {
            TEST_STATE = true;
        }

        let cols = 123;
        let rows = 219;
        let n = rows * cols;
        let mut v1: Vec<f64> = Vec::with_capacity(n);
        let mut v2: Vec<f64> = Vec::with_capacity(n);

        let mut rng = thread_rng();

        for _ in 0..n {
            v1.push(rng.gen::<f64>() % 1000000.0);
            v2.push(rng.gen::<f64>() % 1000000.0);
        }

        let a: Matrix = Matrix::with_vector(v1, rows, cols);
        let b: Matrix = Matrix::with_vector(v2, cols, rows);

        let transpose_result = a.mult(&b, mult_transpose);
        let strassen_par_result = a.mult(&b, mult_par_strassen);

        assert!(transpose_result.eq(&strassen_par_result));
        assert!(strassen_par_result.eq(&transpose_result));
    }
}