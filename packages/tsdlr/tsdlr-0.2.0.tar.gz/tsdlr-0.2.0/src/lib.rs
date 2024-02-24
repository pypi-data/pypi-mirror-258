#![deny(clippy::correctness)]
#![warn(
    missing_docs,
    clippy::all,
    clippy::suspicious,
    clippy::style,
    clippy::complexity,
    clippy::perf,
    clippy::pedantic,
    clippy::nursery,
    clippy::missing_docs_in_private_items,
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::cast_lossless
)]
#![doc = include_str!("../README.md")]

pub(crate) mod data;
pub(crate) mod models;

use models::{DTModel, LRModel, Model};

use ndarray::prelude::*;
use numpy::{IntoPyArray, PyArray2, PyReadonlyArray2};
use pyo3::{exceptions::PyValueError, prelude::*};
use smartcore::{
    api::SupervisedEstimator, linalg::basic::matrix::DenseMatrix,
    linear::linear_regression::LinearRegressionParameters,
    tree::decision_tree_regressor::DecisionTreeRegressorParameters,
};

/// Denoise a set of time-series samples.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * `window_size` is not an even number.
/// * `window_size` does not evenly divide the length of the time-series.
pub fn denoise<'a, M, Mp, P>(
    samples: &'a ArrayView2<'a, f32>,
    window_size: usize,
    parameters: P,
) -> Result<Array2<f32>, String>
where
    M: Model<Mp, P>,
    Mp: SupervisedEstimator<DenseMatrix<f32>, ndarray::Array1<f32>, P> + Send + Sync,
    P: Clone + Send + Sync,
{
    if window_size % 2 != 0 {
        Err("The window size must be an even number.".to_string())
    } else if samples.len_of(Axis(1)) % window_size != 0 {
        Err(format!(
            "The window size must evenly divide the length of the time-series ({:?}).",
            samples.len_of(Axis(1))
        ))
    } else {
        let model = M::train(samples, window_size, parameters)?;
        model.denoise(samples)
    }
}

/// Denoise a set of time-series samples using linear regression.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * Shape mismatch. Should not happen.
///
/// # Returns
///
/// The denoised samples and the mean squared error.
#[allow(clippy::needless_pass_by_value)]
#[pyfunction]
pub fn denoise_linear_regression(
    py: Python,
    samples: PyReadonlyArray2<'_, f32>,
    window_size: usize,
) -> PyResult<Py<PyArray2<f32>>> {
    let samples = samples.as_array();
    denoise::<LRModel, _, _>(
        &samples,
        window_size,
        LinearRegressionParameters::default(),
    )
    .map_err(PyValueError::new_err)
    .map(|x| x.into_pyarray(py).to_owned())
}

/// Denoise a set of time-series samples using decision trees.
///
/// # Parameters
///
/// * `samples`: The time-series samples to denoise.
/// * `window_size`: The number of elements in each window.
///
/// # Errors
///
/// * Shape mismatch. Should not happen.
///
/// # Returns
///
/// The denoised samples and the mean squared error.
#[allow(clippy::needless_pass_by_value)]
#[pyfunction]
pub fn denoise_decision_tree(
    py: Python,
    samples: PyReadonlyArray2<'_, f32>,
    window_size: usize,
) -> PyResult<Py<PyArray2<f32>>> {
    let samples = samples.as_array();
    let params = DecisionTreeRegressorParameters {
        max_depth: Some(16),
        min_samples_leaf: 1,
        min_samples_split: 2,
        seed: None,
    };
    denoise::<DTModel, _, _>(&samples, window_size, params)
        .map_err(PyValueError::new_err)
        .map(|x| x.into_pyarray(py).to_owned())
}

/// A Python module implemented in Rust.
///
/// # Errors
///
/// * If the module cannot be created.
/// * If the function cannot be added to the module.
#[pymodule]
pub fn tsdlr(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(denoise_linear_regression, m)?)?;
    m.add_function(wrap_pyfunction!(denoise_decision_tree, m)?)?;
    Ok(())
}
