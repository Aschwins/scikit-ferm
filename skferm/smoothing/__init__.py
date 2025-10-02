from typing import Any, Dict, List, Literal, Optional, Tuple

import pandas as pd

from .core import apply_method_to_groups
from .methods import exponential_moving_average, rolling_average, savitzky_golay_smooth
from .metrics import (
    evaluate_smoothing_quality,
    fit_quality_metrics,
    total_variation,
)

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
    method: Literal["rolling", "ema", "savgol"] = "rolling",
    groupby_col: Optional[str] = None,
    **kwargs,
) -> pd.DataFrame:
    r"""
    Apply smoothing to data with pandas pipe support.

    Parameters:
    - df: Input DataFrame
    - x: Column name for x-axis values
    - y: Column name for y-axis values
    - method: Smoothing method
    - groupby_col: Optional column to group by
    - \*\*kwargs: Method-specific parameters

    Returns:
    - DataFrame with smoothed values in {y}_smooth column
    """
    if method not in SMOOTHING_METHODS:
        raise ValueError(f"Unknown smoothing method: {method}. Available: {list(SMOOTHING_METHODS.keys())}")

    method_func = SMOOTHING_METHODS[method]
    return apply_method_to_groups(df, x, y, method_func, groupby_col, **kwargs)


def smooth_sequential(
    df: pd.DataFrame,
    x: str,
    y: str,
    stages: List[Tuple[str, Dict[str, Any]]],
    groupby_col: Optional[str] = None,
    output_suffix: str = "_smooth",
) -> pd.DataFrame:
    """
    Apply multiple smoothing methods in sequence.

    Parameters:
    - stages: List of (method_name, parameters) tuples
    - output_suffix: Suffix for the final smoothed column

    Returns:
    - DataFrame with final smoothed column named {y}{output_suffix}
    """
    result_df = df.copy().assign(new_y=lambda d: d[y])  # Temporary column to hold intermediate y values

    for i, (method_name, params) in enumerate(stages):
        if method_name not in SMOOTHING_METHODS:
            raise ValueError(f"Unknown method: {method_name}")

        method_func = SMOOTHING_METHODS[method_name]
        result_df = apply_method_to_groups(result_df, x, "new_y", method_func, groupby_col, **params)
        # overwrite y to the new smoothed y for next iteration
        result_df = result_df.assign(new_y=lambda d: d["new_y_smooth"]).drop(columns="new_y_smooth")

    return result_df.rename(columns={"new_y": f"{y}{output_suffix}"})


# Export for direct use
__all__ = [
    "smooth",
    "smooth_sequential",
    "SMOOTHING_METHODS",
    "total_variation",
    "fit_quality_metrics",
    "evaluate_smoothing_quality",
]
