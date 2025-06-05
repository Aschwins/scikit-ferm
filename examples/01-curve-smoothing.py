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

        Curve smoothing is used for noisy fermentation time series. `scikit-ferm` has the `smoothing` module to deal with these curves. In this notebook we describe two different cases of curve smoothing.

        ## Infrequent timepoints
        Here we want to interpolate between the measured timepoints. We have a lot of time between the measurements, so we can use a spline interpolation to fill in the gaps.

        ## Frequent timepoints
        Here we want to filter the noise from the data, so we can use a moving average or a Savitzky-Golay filter. The Savitzky-Golay filter is a popular method for smoothing data while preserving important features such as peak height and width. It works by fitting successive sub-sets of adjacent data points with a low-degree polynomial by the method of linear least squares.

        ## Examples with more than 1 time series in the dataset.

        Each smoother works on some x and y data. The x and y data should resemble a single a curve. A smoother is created and can be call on a new domain to either get more frequent interpolated timepoints of your curve or smoothed out / noise filtered out curves.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Imports""")
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.interpolate import interp1d
    from scipy.signal import savgol_filter

    from skferm.datasets.rheolaser import load_rheolaser_data
    from skferm.datasets.synthetic import generate_synthetic_growth
    from skferm.smoothing.pipe import smooth

    plt.rcParams.update(
        {
            "font.size": 8,
            "axes.labelsize": 10,
            "axes.titlesize": 12,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "figure.dpi": 300,  # For print quality
            "figure.figsize": [4, 3],  # Size in inches (typical for 1-column paper figs)
            "axes.grid": True,
            "grid.alpha": 0.3,
        }
    )
    return (
        generate_synthetic_growth,
        interp1d,
        load_rheolaser_data,
        np,
        pd,
        plt,
        savgol_filter,
        smooth,
    )


@app.cell
def _(mo):
    mo.md(r"""# Infrequent Timepoints""")
    return


@app.cell
def _(generate_synthetic_growth, logger, np, pd):
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
    return df, synthetic_data, time_points


@app.cell
def _(df, plt):
    fig = plt.figure(figsize=(8, 4))
    plt.scatter(df["time"], df["population"], label="Original")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Population")
    plt.title("Logistic Growth Data")
    return (fig,)


@app.cell
def _(mo, time_points):
    mo.md(
        rf"""
        Here we have a nice fermentation curve, where some microbe is grown. There are two problems with this dataset.

        1. The data is noisy, there are some up and downshifts in the meaurements
        2. We have measured frequency of 1 measurement per ~{time_points[1] - time_points[0]:.0f} minutes.

        This can both be solved by curve smoothing.)
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""# Frequent Time Points""")
    return


@app.cell
def _(load_rheolaser_data):
    df2 = load_rheolaser_data()
    df2.head(2)
    return (df2,)


@app.cell
def _(df2, plt):
    fig2 = plt.figure(figsize=(8, 4))
    plt.scatter(df2["time"], df2["elasticity_index"], c=df2["sample_id"].factorize()[0], alpha=0.5)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Elasticity Index")
    plt.title("Raw Rheolaser Data")
    return (fig2,)


@app.cell
def _(df2, smooth):
    smoothed_df2 = smooth(df2, x="time", y="elasticity_index", groupby_col="sample_id", window=10)
    smoothed_df2.head(2)
    return (smoothed_df2,)


@app.cell
def _(plt, smoothed_df2):
    fig3 = plt.figure(figsize=(8, 4))
    plt.scatter(
        smoothed_df2["time"],
        smoothed_df2["elasticity_index_smooth"],
        c=smoothed_df2["sample_id"].factorize()[0],
        alpha=0.5,
    )
    plt.xlabel("Time (minutes)")
    plt.ylabel("Elasticity Index")
    plt.title("Raw Rheolaser Data")
    return (fig3,)


@app.cell
def _(df2):
    df2["time"]
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
