use numpy::{PyArray1, PyReadonlyArray2};
use pyo3::prelude::*;
use pyo3::Python;
use strassen::matrix::Matrix as StrassenMatrix;
use strassen::par_mult::mult_par_strassen;
extern crate blas;
extern crate lapack;


use lapack::{dgetrf, dgetri};

struct Matrix(StrassenMatrix);

impl Matrix {
    pub fn inverse(&self) -> Result<Matrix, &'static str> {
        let StrassenMatrix { rows, cols, elements, .. } = &self.0;

        if *rows != *cols {
            return Err("Matrix inversion requires a square matrix.");
        }

        let mut a = elements.clone();
        let n = *rows as i32;
        let mut ipiv = vec![0_i32; *rows];
        let mut info = 0;

        let lda = n;
        unsafe {
            dgetrf(n, n, &mut a, lda, &mut ipiv, &mut info);
            if info != 0 {
                return Err("Failed to compute LU factorization.");
            }

            let lwork = n;
            let mut work = vec![0.0; lwork as usize];
            dgetri(n, &mut a, lda, &mut ipiv, &mut work, lwork, &mut info);
            if info != 0 {
                return Err("Failed to compute the inverse.");
            }
        }

        Ok(Matrix(StrassenMatrix::with_vector(a, *rows, *cols)))
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
}

// Assuming a function to convert StrassenMatrix multiplication to Matrix
fn strassen_multiply(a: &Matrix, b: &Matrix) -> Matrix {
    let result = mult_par_strassen(&a.0, &b.0);
    Matrix(result)
}

fn convert_array_to_matrix(array: PyReadonlyArray2<f64>) -> Matrix {
    let array = array.as_array(); // Get ndarray view

    let elements: Vec<f64> = array.iter().copied().collect();
    let rows = array.nrows();
    let cols = array.ncols();

    Matrix(StrassenMatrix::with_vector(elements, rows, cols))
}

#[pyclass]
#[derive(Debug)]
pub struct LinearRegression {
    fit_intercept: bool,
    intercept: Option<f64>,
    slope: Option<Vec<f64>>,  // Assuming multiple regression, slope is a vector
}

#[pymethods]
impl LinearRegression {
    #[new]
    pub fn new(fit_intercept: bool) -> Self {
        LinearRegression {
            fit_intercept,
            intercept: None,
            slope: None,
        }
    }

    fn fit(&mut self, _py: Python, x: PyReadonlyArray2<f64>, y: PyReadonlyArray2<f64>) -> PyResult<()> {
        let mut x_matrix = convert_array_to_matrix(x);
        let y_matrix = convert_array_to_matrix(y);

        if self.fit_intercept {
            let ones = vec![1.0; x_matrix.rows()];
            let ones_matrix = Matrix::with_vector(ones, x_matrix.rows(), 1);
            x_matrix = strassen_multiply(&ones_matrix, &x_matrix);
        }

        let xt = x_matrix.transpose();
        let xtx = strassen_multiply(&xt, &x_matrix);

        let xtx_inv = xtx.inverse().map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Matrix inversion failed."))?;

        let xty = strassen_multiply(&xt, &y_matrix);
        let b = strassen_multiply(&xtx_inv, &xty);

        self.intercept = Some(b.0.elements[0]);
        self.slope = Some(b.0.elements[1..].to_vec());

        Ok(())
    }

    /// Predicts the y values for given x values using the learned regression coefficients.
    ///
    /// # Arguments
    /// * `x` - A 2D numpy array where each row represents a set of features for one observation.
    ///
    /// # Returns
    /// A numpy array of predicted y values.
    fn predict(&self, py: Python, x: PyReadonlyArray2<f64>) -> PyResult<Py<PyArray1<f64>>> {
        let x_matrix = convert_array_to_matrix(x);

        // Handle fit_intercept: prepend a column of ones if intercept is to be considered
        let x_matrix = if self.fit_intercept {
            let ones = vec![1.0; x_matrix.rows()];
            let ones_matrix = Matrix::with_vector(ones, x_matrix.rows(), 1);
            strassen_multiply(&ones_matrix, &x_matrix)
        } else {
            x_matrix
        };

        // Ensure that the slope is available
        let slope = self.slope.as_ref().ok_or_else(|| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Model has not been fitted yet."))?;
        let intercept_val = self.intercept.unwrap_or(0.0);

        // Compute the predictions: y = Xb + intercept
        // Converting slope to a Matrix for multiplication
        let b_matrix = Matrix::with_vector(slope.clone(), slope.len(), 1);
        let y_matrix = strassen_multiply(&x_matrix, &b_matrix);

        // Add intercept to all y values
        let y_values: Vec<f64> = y_matrix.0.elements.iter().map(|&val| val + intercept_val).collect();

        // Convert the result back to a numpy array to return
        Ok(PyArray1::from_vec(py, y_values).to_owned())
    }
}

#[pymodule]
fn tsontson_learn(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<LinearRegression>()?;
    Ok(())
}
