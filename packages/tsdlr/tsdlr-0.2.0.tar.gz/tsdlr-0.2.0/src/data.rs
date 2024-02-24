//! Creating training data from time-series data.

use ndarray::prelude::*;

/// Converts a 2d array of time-series samples into a collection of windows.
///
/// We assume that the time-series `samples` are stored in the rows of the 2d array.
/// The `window_size` is an even number and evenly divides the length of the
/// time-series.
///
/// # Parameters
///
/// * `samples`: The time-series samples to convert.
/// * `window_size`: The number of elements in each window.
///
/// # Returns
///
/// The collection of windows.
pub fn create_windows<'a>(
    samples: &'a ArrayView2<'a, f32>,
    window_size: usize,
) -> Vec<ArrayView2<'a, f32>> {
    let stride = window_size / 2;
    let sample_len = samples.ncols();
    let window_starts = (0..=(sample_len - window_size)).step_by(stride);
    let windows = window_starts
        .map(|i| samples.slice(s![.., i..i + window_size]))
        .collect::<Vec<_>>();
    windows
}

/// Converts a collection of windows into training data.
///
/// We assume that the `index` is less than the window size.
/// The column at the `index` will be removed from the windows and used as the target.
///
/// # Parameters
///
/// * `windows`: The collection of windows.
/// * `index`: The index of the column to use as the target.
///
/// # Returns
///
/// * The training data.
/// * The target data.
pub fn windows_to_train(
    windows: &[ArrayView2<'_, f32>],
    index: usize,
) -> (Array2<f32>, Array1<f32>) {
    let train = windows
        .iter()
        .map(|w| {
            let pre_index = w.slice(s![.., ..index]);
            let post_index = w.slice(s![.., index + 1..]);
            ndarray::concatenate(Axis(1), &[pre_index, post_index]).unwrap_or_else(
                |_| {
                    unreachable!(
                        "We made the slices, so they should have the correct shape."
                    )
                },
            )
        })
        .collect::<Vec<_>>();

    let target = windows
        .iter()
        .map(|w| w.index_axis(Axis(1), index).to_owned())
        .collect::<Vec<_>>();

    let train = train.iter().map(ArrayBase::view).collect::<Vec<_>>();
    let target = target.iter().map(ArrayBase::view).collect::<Vec<_>>();

    let train = ndarray::concatenate(Axis(0), &train).unwrap_or_else(|_| {
        unreachable!("We made the arrays, so they should have the correct shape.")
    });
    let target = ndarray::concatenate(Axis(0), &target).unwrap_or_else(|_| {
        unreachable!("We made the arrays, so they should have the correct shape.")
    });
    (train, target)
}
