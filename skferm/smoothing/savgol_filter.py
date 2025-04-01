import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


def savitzky_golay(data, time=None, window_size=4, poly_order=2):
    """
    Apply Savitzky-Golay smoothing and return an interpolator.

    Parameters:
    - data: np.ndarray
        1D array of data points to smooth.
    - time: np.ndarray or None
        1D array of time points corresponding to the data. If None, indices are used.
    - window_size: int
        Window size for the Savitzky-Golay filter.
    - poly_order: int
        Polynomial order for the Savitzky-Golay filter.

    Returns:
    - smoothed: np.ndarray
        Smoothed data points.
    - interpolator: Callable
        A function that interpolates the smoothed data at arbitrary time points.
    """
    if time is None:
        time = np.arange(len(data))

    # Apply Savitzky-Golay filter
    smoothed = savgol_filter(data, window_size, poly_order)

    # Create an interpolator for the smoothed data
    interpolator = interp1d(time, smoothed, kind="linear")

    return smoothed, interpolator
