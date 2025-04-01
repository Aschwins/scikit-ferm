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


@app.cell
def _(mo):
    mo.md(
        r"""
        # Curve Smoothing


        Curve smoothing is used for noisy fermentation time series. `sk-ferm` has the `smoothing` module to deal with these nasty curves.
        """
    )
    return


@app.cell
def _(logger):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    from skferm.datasets.synthetic import generate_synthetic_growth
    from skferm.smoothing.moving_average import moving_average
    from skferm.smoothing.savgol_filter import savitzky_golay
    from skferm.smoothing.transformer import SmoothingTransformer

    # Define time points
    time_points = np.linspace(0, 100, 50)

    # Generate synthetic data using the logistic growth model with noise
    synthetic_data = generate_synthetic_growth(
        time=time_points,
        model="logistic",
        noise_std=1.5,  # Add Gaussian noise with standard deviation 0.5
        N0=1,  # Logistic growth parameter, Initial population
        r=0.1,  # Logistic growth parameter, growth rate
        Nmax=100,  # Logistic growth parameter, Maximum population
    )

    # Convert the result to a pandas DataFrame for easier handling
    df = pd.DataFrame({"time": synthetic_data["time"], "population": synthetic_data["population"], "sample_id": "A"})

    logger.info(df.head())
    return (
        SmoothingTransformer,
        df,
        generate_synthetic_growth,
        moving_average,
        np,
        pd,
        plt,
        savitzky_golay,
        synthetic_data,
        time_points,
    )


@app.cell
def _(df, plt):
    plt.scatter(df["time"], df["population"], label="Original")
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
def _(SmoothingTransformer, df, savitzky_golay):
    # Initialize the transformer
    transformer = SmoothingTransformer(smoothing_function=savitzky_golay, window_size=10, poly_order=2)

    # Transform the data
    cleaned_df = df.rename(columns={"time": "time", "population": "value"})
    smoothed_data = transformer.fit_transform(cleaned_df)
    # logger.info(smoothed_data)
    return cleaned_df, smoothed_data, transformer


@app.cell
def _(smoothed_data):
    smoothed_data
    return


@app.cell
def _(df, plt, smoothed_data):
    plt.scatter(smoothed_data["time"], smoothed_data["value"], label="Smoothed")
    plt.scatter(df["time"], df["population"], label="Original")
    plt.legend()
    return


@app.cell
def _(np):
    from scipy.interpolate import interp1d
    from scipy.signal import savgol_filter

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
        interpolator = interp1d(time, smoothed, kind="linear")

        return smoothed, interpolator

    return interp1d, savgol_filter, savitzky_golay2


@app.cell
def _(logger, np, pd, savitzky_golay2):
    # Example noisy data
    time = np.linspace(0, 10, 20)  # Original time points
    values = np.sin(time) + np.random.normal(0, 0.1, len(time))  # Noisy sine wave

    # Apply Savitzky-Golay smoothing
    smoothed_values, interpolator = savitzky_golay2(values, time, window_size=5, poly_order=2)

    # Interpolate at new time points
    new_time = np.linspace(0, 10, 50)  # Higher resolution time points
    interpolated_values = interpolator(new_time)

    # Convert to DataFrame for visualization
    df_original = pd.DataFrame({"time": time, "value": values})
    df_smoothed = pd.DataFrame({"time": time, "value": smoothed_values})
    df_interpolated = pd.DataFrame({"time": new_time, "value": interpolated_values})

    # Print results
    logger.info("Original Data:")
    logger.info(df_original.head())
    logger.info("\nSmoothed Data:")
    logger.info(df_smoothed.head())
    logger.info("\nInterpolated Data:")
    logger.info(df_interpolated.head())
    return (
        df_interpolated,
        df_original,
        df_smoothed,
        interpolated_values,
        interpolator,
        new_time,
        smoothed_values,
        time,
        values,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
