"""
Metrics for evaluating smoothing quality and curve smoothness.

This module provides functions to quantify:
1. How smooth a curve is (total variation metric)
2. How well the smoothed curve fits the original data (RMSE and R²)
"""

from typing import Dict, Optional, Union

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score


def total_variation(y_values: np.ndarray, normalize: bool = True) -> float:
    """
    Calculate total variation for a sequence of values.

    Parameters:
    -----------
    y_values : np.ndarray
        Array of y-values
    normalize : bool
        Whether to normalize by the range of values

    Returns:
    --------
    float
        Total variation metric
    """
    if len(y_values) < 2:
        return np.nan

    # Remove NaN values
    clean_values = y_values[~np.isnan(y_values)]
    if len(clean_values) < 2:
        return np.nan

    # Calculate total variation
    tv = np.sum(np.abs(np.diff(clean_values)))

    if normalize:
        y_range = np.ptp(clean_values)
        if y_range == 0:
            return 0.0
        tv = tv / y_range

    return tv


def fit_quality_metrics(original: np.ndarray, smoothed: np.ndarray) -> Dict[str, float]:
    """
    Calculate fit quality metrics between original and smoothed data.

    Parameters:
    -----------
    original : np.ndarray
        Original data values
    smoothed : np.ndarray
        Smoothed data values

    Returns:
    --------
    Dict[str, float]
        Dictionary with 'rmse' and 'r2' keys
    """
    if len(original) != len(smoothed):
        raise ValueError("Original and smoothed arrays must have the same length")

    # Remove NaN values
    mask = ~(np.isnan(original) | np.isnan(smoothed))
    if np.sum(mask) < 2:
        return {"rmse": np.nan, "r2": np.nan}

    original_clean = original[mask]
    smoothed_clean = smoothed[mask]

    rmse = float(np.sqrt(mean_squared_error(original_clean, smoothed_clean)))
    r2 = float(r2_score(original_clean, smoothed_clean))

    return {"rmse": rmse, "r2": r2}


def evaluate_smoothing_quality(
    df: pd.DataFrame,
    x_col: str,
    original_col: str,
    smoothed_col: str,
    group_col: Optional[str] = None,
) -> Union[pd.DataFrame, pd.Series]:
    """
    Evaluation of smoothing quality.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing the data
    x_col : str
        Column name for x-axis (for sorting)
    original_col : str
        Column name for original data
    smoothed_col : str
        Column name for smoothed data
    group_col : Optional[str]
        Column to group by (returns Series if provided)

    Returns:
    --------
    pd.DataFrame or pd.Series
        DataFrame with metrics if group_col is provided, else Series
    """
    # Validate inputs
    required_cols = [x_col, original_col, smoothed_col]
    if group_col:
        required_cols.append(group_col)

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    def _calculate_group_metrics(group_df: pd.DataFrame):
        """Calculate metrics for a single group."""
        sorted_df = group_df.sort_values(x_col)

        original_vals = np.asarray(sorted_df[original_col].values)
        smoothed_vals = np.asarray(sorted_df[smoothed_col].values)

        # Calculate smoothness metrics
        orig_smoothness = total_variation(original_vals)
        smooth_smoothness = total_variation(smoothed_vals)

        # Calculate fit quality
        fit_metrics = fit_quality_metrics(original_vals, smoothed_vals)

        metrics = {
            f"{original_col}_smoothness": orig_smoothness,
            f"{smoothed_col}_smoothness": smooth_smoothness,
            f"{original_col}_{smoothed_col}_rmse_fit": fit_metrics["rmse"],
            f"{original_col}_{smoothed_col}_r2_fit": fit_metrics["r2"],
        }

        return pd.Series(metrics)

    if group_col is not None:
        return df.groupby(group_col).apply(_calculate_group_metrics).reset_index()
    else:
        return _calculate_group_metrics(df)
