"""Showcase of denoising algorithms."""

import time

import data  # type: ignore[import]
import numpy
import plotly.express as px
import streamlit as st
import tsdlr

st.title("Showcase of denoising algorithms")

sample_num = 500
sample_len = 1024
rng = numpy.random.default_rng(42)

freq = 16
offset = 0

frequencies = [16, 24, 40]
offsets = [0 for _, _ in enumerate(frequencies)]

x = numpy.linspace(0, 2 * numpy.pi, sample_len)
clean_wave = data.summed_waves(x, zip(frequencies, offsets))

# plot the sine wave
st.line_chart(clean_wave)

# Add some noise
noise = rng.normal(0, 0.2, (sample_num, sample_len))
samples = (clean_wave + noise).astype(numpy.float32)

st.write(f"Created {sample_num} samples of a sine wave with noise.")

# plot the first sample
st.line_chart(samples[0])

# Calculate the error for each noisy sample vs the clean sample
errors = numpy.sqrt(numpy.mean((samples - clean_wave) ** 2, axis=1))

# plot the frequency distribution of errors
st.write("Plotting the distribution of initial rmse of noise vs clean ...")
st.write(f"Mean error: noisy vs clean: {numpy.mean(errors):.2e}")
st.plotly_chart(px.histogram(errors, nbins=50))

# Run the denoising algorithms
window_size = 256

st.write(f"Running the denoising algorithm with {window_size = } ...")
start = time.perf_counter()
denoised = tsdlr.denoise_linear_regression(samples, window_size)
time_taken = time.perf_counter() - start
st.write(
    f"Denoising took {time_taken:.3f} seconds for {sample_num} samples of "
    f"length {sample_len}.",
)

rmse = numpy.sqrt(numpy.mean((denoised - clean_wave) ** 2, axis=1))
st.write("Plotting the distribution of rmse of denoised vs clean ...")
st.write(f"Mean error: denoised vs clean: {numpy.mean(rmse):.2e}")
st.plotly_chart(px.histogram(rmse, nbins=50))

# Calculate the error for each denoised sample vs the noisy sample
errors = numpy.sqrt(numpy.mean((denoised - samples) ** 2, axis=1))

# plot the first sample
st.write(f"Plotting the first denoised sample error = {rmse[0]:.2e} ...")
st.line_chart(denoised[0])

# plot the distribution of errors
st.write("Plotting the distribution of rmse for denoised vs noisy ...")
st.write(f"Mean error: denoised vs noisy: {numpy.mean(errors):.2e}")
st.plotly_chart(px.histogram(errors, nbins=50))
