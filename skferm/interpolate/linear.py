import pandas as pd
from scipy.interpolate import interp1d


def interpolate_smoothed_curve(df, x: str, y_smooth: str, new_time):
    # Create interpolation function
    f_interp = interp1d(df[x], df[y_smooth], kind="linear", bounds_error=False)

    # Apply to new time grid
    interpolated_values = f_interp(new_time)

    return pd.DataFrame({x: new_time, f"{y_smooth}_interp": interpolated_values})
