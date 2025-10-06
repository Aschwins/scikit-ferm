"""Plotting functions for fermentation curves."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if TYPE_CHECKING:
    from matplotlib.axes import Axes


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
    ax: Optional["Axes"] = None,
    **kwargs,
):
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
        Figure size as (width, height). Only used when ax is None
    style : str, default 'whitegrid'
        Seaborn style
    ax : matplotlib.axes.Axes, optional
        Axes object to plot on. If None, creates new figure and axes
    **kwargs : additional keyword arguments for seaborn.lineplot
    Returns
    -------
    matplotlib.figure.Figure or matplotlib.axes.Axes
        Returns Figure if ax is None (new figure created), otherwise returns the provided Axes
    """
    sns.set_style(style)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        created_figure = True
    else:
        fig = ax.figure
        created_figure = False

    sns.lineplot(data=data, x=x, y=y, hue=sample_col, ax=ax, linewidth=2, **kwargs)

    ax.set_xlabel(xlabel if xlabel else x.replace("_", " ").title())
    ax.set_ylabel(ylabel if ylabel else y.replace("_", " ").title())
    ax.set_title(title if title else f"{y.replace('_', ' ').title()} Over {x.replace('_', ' ').title()} by Sample")
    ax.legend(title=sample_col.replace("_", " ").title(), bbox_to_anchor=(1.05, 1), loc="upper left")

    if created_figure:
        plt.tight_layout()
        return fig
    else:
        return ax
