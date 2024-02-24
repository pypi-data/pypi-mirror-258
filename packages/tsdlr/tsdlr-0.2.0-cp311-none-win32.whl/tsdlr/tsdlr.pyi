"""Typing stubs for the package."""

import numpy
import numpy.typing as npt


def denoise_linear_regression(
    samples: npt.NDArray[numpy.float32],
    window_size: int,
) -> npt.NDArray[numpy.float32]:
    """Denoise a set of time-series samples using linear regression.

    Args:
        samples: The time-series samples to denoise.
        window_size: The size of the window to use for linear regression.
    """
    ...


def denoise_decision_tree(
    samples: npt.NDArray[numpy.float32],
    window_size: int,
) -> npt.NDArray[numpy.float32]:
    """Denoise a set of time-series samples using linear regression.

    Args:
        samples: The time-series samples to denoise.
        window_size: The size of the window to use for linear regression.
    """
    ...
