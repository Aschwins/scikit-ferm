import pandas as pd


def smooth_group(df, x: str, y: str, window=5):
    df = df.sort_values(x)  # ensure time is sorted
    df[f"{y}_smooth"] = df[y].rolling(window=window, center=True, min_periods=1).mean()
    return df


def smooth(df: pd.DataFrame, x: str, y: str, groupby_col: str) -> pd.DataFrame:
    """
    Applies smoothing to each unique fermentation curve (grouped by sample_id).

    Parameters:
    - df: Pandas DataFrame with columns ['time', 'pH', 'sample_id'].
    - x: Column name for the x-axis values.
    - y: Column name for the y-axis values.
    - groupby_col: Column name to group by (e.g., 'sample_id').

    Returns:
    - DataFrame with an added 'y_smooth' column.
    """

    return (
        df.groupby(groupby_col, group_keys=False)
        .apply(lambda group: smooth_group(group, x=x, y=y))
        .reset_index(drop=True)
    )
