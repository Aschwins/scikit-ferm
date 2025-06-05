# skferm/interpolate/pipe.py

from typing import Literal, Optional

import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline, interp1d


def interpolate_group(
    df: pd.DataFrame, x: str, y: str, new_x: np.ndarray, method: str, spline_s: float
) -> pd.DataFrame:
    df = df.sort_values(x)
    if method == "linear":
        f = interp1d(df[x], df[y], kind="linear", bounds_error=False)
    elif method == "spline":
        f = UnivariateSpline(df[x], df[y], s=spline_s)
    else:
        raise ValueError("method must be 'linear' or 'spline'")

    y_new = f(new_x)
    out = pd.DataFrame({x: new_x, f"{y}_interp": y_new})
    return out


def interpolate(
    df: pd.DataFrame,
    x: str,
    y: str,
    new_x: np.ndarray,
    groupby_col: Optional[str] = None,
    method: Literal["linear", "spline"] = "linear",
    spline_s: float = 0.0,
) -> pd.DataFrame:
    """
    Interpolate y-values over a new x-grid, optionally grouped.

    Parameters:
    - df: Input DataFrame.
    - x: x-axis column name (e.g. "time").
    - y: y-axis column name (e.g. "elasticity_index_smooth").
    - new_x: Array of new x-values.
    - groupby_col: Optional group column (e.g. "sample_id").
    - method: Interpolation method: "linear" or "spline".
    - spline_s: Spline smoothing factor (0 for exact fit).

    Returns:
    - DataFrame with interpolated values over new_x per group.
    """
    if groupby_col:
        results = []
        for group_val, group_df in df.groupby(groupby_col):
            interpolated = interpolate_group(group_df, x, y, new_x, method, spline_s)
            interpolated[groupby_col] = group_val
            results.append(interpolated)
        return pd.concat(results, ignore_index=True)
    else:
        return interpolate_group(df, x, y, new_x, method, spline_s)
