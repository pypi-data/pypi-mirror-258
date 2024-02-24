"""Generate various kinds of time series data for the examples."""

import numpy


def sine_wave(x: numpy.ndarray, freq: float, offset: float) -> numpy.ndarray:
    """Generate a sine wave."""
    return numpy.sin(freq * x + offset)


def summed_waves(
    x: numpy.ndarray,
    freq_offset: list[tuple[float, float]],
) -> numpy.ndarray:
    """Generate a sum of sine waves."""
    y = numpy.zeros_like(x)
    for freq, offset in freq_offset:
        y += sine_wave(x, freq, offset)
    return y
