import marimo

__generated_with = "0.12.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import logging

    import marimo as mo

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger, logging, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Curve Smoothing

        Curve smoothing is used for noisy fermentation time series. `sk-ferm` has the `smoothing` module to deal with these nasty curves. In this notebook we describe two different cases of curve smoothing.

        ## Infrequent timepoints
        Here we want to interpolate between the measured timepoints. We have a lot of time between the measurements, so we can use a spline interpolation to fill in the gaps.

        ## Frequent timepoints
        Here we want to filter the noise from the data, so we can use a moving average or a Savitzky-Golay filter. The Savitzky-Golay filter is a popular method for smoothing data while preserving important features such as peak height and width. It works by fitting successive sub-sets of adjacent data points with a low-degree polynomial by the method of linear least squares.

        ## TODO: Regression models

        ## Examples with more than 1 time series in the dataset.


        Each smoother works on some x and y data. The x and y data should resemble a single a curve. A smoother is created and can be call on a new domain to either get more frequent interpolated timepoints of your curve or smoothed out / noise filtered out curves.
        """
    )
    return


@app.cell
def _(logger):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.interpolate import interp1d
    from scipy.signal import savgol_filter

    from skferm.datasets.synthetic import generate_synthetic_growth
    from skferm.smoothing.moving_average import moving_average
    from skferm.smoothing.savgol_filter import savitzky_golay
    from skferm.smoothing.transformer import SmoothingTransformer

    # Define time points
    time_points = np.linspace(0, 300, int(300 / 30))

    # Generate synthetic data using the logistic growth model with noise
    synthetic_data = generate_synthetic_growth(
        time=time_points,
        model="logistic",
        noise_std=0.5,  # Add Gaussian noise with standard deviation 0.5
        N0=1,  # Logistic growth parameter, Initial population
        r=0.05,  # Logistic growth parameter, growth rate
        Nmax=100,  # Logistic growth parameter, Maximum population
    )

    # Convert the result to a pandas DataFrame for easier handling
    df = pd.DataFrame({"time": synthetic_data["time"], "population": synthetic_data["population"], "sample_id": "A"})

    logger.info(df.head())
    return (
        SmoothingTransformer,
        df,
        generate_synthetic_growth,
        interp1d,
        moving_average,
        np,
        pd,
        plt,
        savgol_filter,
        savitzky_golay,
        synthetic_data,
        time_points,
    )


@app.cell
def _(df, plt):
    plt.plot(df["time"], df["population"], label="Original")
    plt.xlabel("Time")
    plt.ylabel("Population")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        Here we have a nice fermentation curve, where some microbe is grown. There are two problems with this dataset.

        1. The data is noisy, there are some up and downshifts in the meaurements
        2. We have measured frequency of 1 measurement per 2 minutes.

        This can both be solved by curve smoothing.
        """
    )
    return


@app.cell
def _():
    from skferm.smoothing.spline import FermentationCurveSmoother

    return (FermentationCurveSmoother,)


@app.cell
def _(df, mo):
    x = df.time.values
    y = df.population.values

    smoothing_factor = mo.ui.slider(0, 1000, 0.05)
    return smoothing_factor, x, y


@app.cell
def _(FermentationCurveSmoother, np, smoothing_factor, x, y):
    fcm = FermentationCurveSmoother(x=x, y=y, smoothing_factor=smoothing_factor.value)
    new_x = np.arange(0, 300, 1)
    y_smooth = fcm.get_smoothed_values(new_x)
    return fcm, new_x, y_smooth


@app.cell
def _(mo):
    k = mo.ui.slider(1, 5, 1)
    return (k,)


@app.cell
def _(k, smoothing_factor, x, y):
    from scipy.interpolate import UnivariateSpline

    spl = UnivariateSpline(x, y, s=smoothing_factor.value, k=k.value)
    return UnivariateSpline, spl


@app.cell
def _(k, smoothing_factor):
    smoothing_factor, k
    return


@app.cell
def _(new_x, plt, spl, x, y):
    plt.scatter(new_x, spl(new_x))
    plt.scatter(x, y, alpha=0.2)
    return


@app.cell
def _(interp1d, np, savgol_filter):
    def savitzky_golay2(data, time=None, window_size=4, poly_order=2):
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
        interpolator = interp1d(time, smoothed, kind="linear", fill_value="extrapolate")

        return smoothed, interpolator

    return (savitzky_golay2,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
