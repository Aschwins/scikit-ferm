import numpy as np


def moving_average(data, window_size):
    """
    Apply a moving average to the data.

    Parameters:
    - data: np.ndarray
        1D array of data points.
    - window_size: int
        Size of the moving average window.

    Returns:
    - np.ndarray
        Smoothed data.
    """
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")
