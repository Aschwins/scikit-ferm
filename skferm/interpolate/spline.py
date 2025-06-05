import pandas as pd
from scipy.interpolate import UnivariateSpline


def spline(df: pd.DataFrame, new_time: list) -> pd.DataFrame:
    """
    Example usage of UnivariateSpline for interpolation.
    This function demonstrates how to use UnivariateSpline to interpolate
    a smooth curve based on a DataFrame with time and elasticity index.
    """
    # Sample DataFrame
    df = pd.DataFrame({"time": [0, 1, 2, 3, 4, 5], "elasticity_index_smooth": [0.1, 0.2, 0.4, 0.3, 0.5, 0.6]})

    # New time grid for interpolation
    spline = UnivariateSpline(df["time"], df["elasticity_index_smooth"], s=0.1)  # s is smoothing factor
    predicted = pd.DataFrame(spline(new_time))
    return predicted
