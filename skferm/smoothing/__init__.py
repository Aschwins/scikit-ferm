from typing import Literal, Optional

import pandas as pd

from .core import apply_method_to_groups
from .methods import exponential_moving_average, rolling_average, savitzky_golay_smooth

# Registry for smoothing methods
SMOOTHING_METHODS = {
    "rolling": rolling_average,
    "ema": exponential_moving_average,
    "savgol": savitzky_golay_smooth,
}


def smooth(
    df: pd.DataFrame,
    x: str,
    y: str,
    method: Literal["rolling", "ema", "savgol", "lowess"] = "rolling",
    groupby_col: Optional[str] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Apply smoothing to data with pandas pipe support.

    Parameters:
    - df: Input DataFrame
    - x: Column name for x-axis values
    - y: Column name for y-axis values
    - method: Smoothing method
    - groupby_col: Optional column to group by
    - **kwargs: Method-specific parameters

    Returns:
    - DataFrame with smoothed values in {y}_smooth column
    """
    if method not in SMOOTHING_METHODS:
        raise ValueError(f"Unknown smoothing method: {method}. Available: {list(SMOOTHING_METHODS.keys())}")

    method_func = SMOOTHING_METHODS[method]
    return apply_method_to_groups(df, x, y, method_func, groupby_col, **kwargs)


# Export for direct use
__all__ = ["smooth", "SMOOTHING_METHODS"]
