"""Plotting functions for fermentation curves."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def plot_fermentation_curves(
    data: pd.DataFrame,
    sample_col: str = "sample_id",
    x: str = "x",
    y: str = "y",
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6),
    style: Literal["white", "dark", "whitegrid", "darkgrid", "ticks"] = "whitegrid",
) -> Figure:
    """
    Plot fermentation curves with different samples distinguished by color.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing fermentation data
    sample_col : str, default 'sample_id'
        Column name for sample identification
    x : str, default 'x'
        Column name for x-axis values
    y : str, default 'y'
        Column name for y-axis values
    title : str, optional
        Plot title. If None, generates default title
    xlabel : str, optional
        X-axis label. If None, uses x column name
    ylabel : str, optional
        Y-axis label. If None, uses y column name
    figsize : tuple, default (10, 6)
        Figure size as (width, height)
    style : str, default 'whitegrid'
        Seaborn style

    Returns
    -------
    plt.Figure
        The matplotlib figure object
    """
    sns.set_style(style)
    fig, ax = plt.subplots(figsize=figsize)

    sns.lineplot(data=data, x=x, y=y, hue=sample_col, ax=ax, linewidth=2, alpha=0.8)

    ax.set_xlabel(xlabel if xlabel else x.replace("_", " ").title())
    ax.set_ylabel(ylabel if ylabel else y.replace("_", " ").title())
    ax.set_title(title if title else f"{y.replace('_', ' ').title()} Over {x.replace('_', ' ').title()} by Sample")
    ax.legend(title=sample_col.replace("_", " ").title(), bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()

    return fig
