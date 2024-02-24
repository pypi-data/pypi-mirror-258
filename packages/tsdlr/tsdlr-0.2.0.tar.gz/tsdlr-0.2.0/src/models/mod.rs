//! ML Models that can be trained for denoising time series data.

mod decision_tree;
mod linear_regression;

use ndarray::prelude::*;
use rayon::prelude::*;
use smartcore::{
    api::SupervisedEstimator,
    linalg::basic::{arrays::Array2, matrix::DenseMatrix},
};

pub use decision_tree::DTModel;
pub use linear_regression::LRModel;

/// A model that can be trained, evaluated, and used for prediction.
///
/// # Type Parameters
///
/// * `M`: The type of the model.
/// * `P`: The type of the model parameters.
pub trait Model<M, P>: Sized + Send + Sync
where
    M: SupervisedEstimator<DenseMatrix<f32>, Array1<f32>, P> + Send + Sync,
    P: Clone + Send + Sync,
{
    /// Creates a new model.
    fn new(models: Vec<M>, window_size: usize) -> Self;

    /// Returns the inner models.
    fn models(&self) -> &[M];

    /// Returns the window size.
    fn window_size(&self) -> usize;

    /// Trains the model.
    ///
    /// # Parameters
    ///
    /// * `samples`: The time-series samples to create the data from.
    /// * `window_size`: The number of elements in each window.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The trained model.
    fn train<'a>(
        samples: &'a ArrayView2<'a, f32>,
        window_size: usize,
        parameters: P,
    ) -> Result<Self, String> {
        let sample_len = samples.len_of(Axis(1));
        let num_windows = 2 * sample_len / window_size - 1;

        let windows = crate::data::create_windows(samples, window_size);
        assert_eq!(windows.len(), num_windows, "Window creation failed");

        let inner_models = (0..window_size)
            .into_par_iter()
            .map(|i| {
                let (train_x, train_y) = crate::data::windows_to_train(&windows, i);
                assert_eq!(
                    train_y.len_of(Axis(0)),
                    samples.len_of(Axis(0)) * num_windows,
                    "Train data creation failed"
                );
                let train_x = DenseMatrix::from_slice(&train_x);
                M::fit(&train_x, &train_y, parameters.clone())
                    .map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        Ok(Self::new(inner_models, window_size))
    }

    /// Predicts the denoised time-series using the model.
    ///
    /// # Parameters
    ///
    /// * `x`: The input data to predict the target data.
    ///
    /// # Errors
    ///
    /// * Depends on the implementation.
    ///
    /// # Returns
    ///
    /// The denoised time-series.
    fn denoise<'a>(
        &self,
        samples: &'a ArrayView2<'a, f32>,
    ) -> Result<ndarray::Array2<f32>, String> {
        let num_windows = 2 * samples.len_of(Axis(1)) / self.window_size() - 1;
        let num_samples = samples.len_of(Axis(0));

        let windows = crate::data::create_windows(samples, self.window_size());
        let predicted = (0..self.window_size())
            .into_par_iter()
            .map(|i| {
                let (test_x, _) = crate::data::windows_to_train(&windows, i);
                let test_x = DenseMatrix::from_slice(&test_x);
                let model = &self.models()[i];
                M::predict(model, &test_x)
                    // .map(|p| p.into_shape((num_samples, num_windows)))
                    .map_err(|e| e.to_string())
            })
            .collect::<Result<Vec<_>, _>>()?;
        let predicted = predicted.iter().map(ArrayBase::view).collect::<Vec<_>>();
        let predicted =
            ndarray::stack(Axis(1), &predicted).map_err(|e| e.to_string())?;
        let predicted = Array1::from_iter(predicted.into_iter())
            .into_shape((num_samples, num_windows * self.window_size()))
            .map_err(|e| e.to_string())?;

        #[allow(clippy::cast_possible_wrap)]
        let stride = (self.window_size() / 2) as isize;
        let first_stride = predicted.slice(s![.., ..stride]);
        let last_stride = predicted.slice(s![.., -stride..]);

        #[allow(clippy::cast_sign_loss)]
        let stride = stride as usize;
        let inner_strides = (0..=(predicted.ncols() - stride))
            .step_by(stride)
            .map(|i| predicted.slice(s![.., i..i + stride]));

        let predicted = core::iter::once(first_stride)
            .chain(inner_strides)
            .chain(core::iter::once(last_stride))
            .collect::<Vec<_>>();

        let predicted = predicted
            .chunks_exact(2)
            .map(|chunk| {
                let (left, right) = (chunk[0], chunk[1]);
                (left.to_owned() + right.to_owned()) / 2.0
            })
            .collect::<Vec<_>>();

        let predicted = predicted.iter().map(ArrayBase::view).collect::<Vec<_>>();
        ndarray::concatenate(Axis(1), &predicted).map_err(|e| e.to_string())
    }
}
