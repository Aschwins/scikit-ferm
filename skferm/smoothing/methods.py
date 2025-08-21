import pandas as pd


def rolling_average(df: pd.DataFrame, x: str, y: str, window: int = 5, center: bool = True, **kwargs) -> pd.DataFrame:
    """Rolling average smoothing."""
    df = df.sort_values(x).copy()
    df[f"{y}_smooth"] = df[y].rolling(window=window, center=center, min_periods=1).mean()
    return df


def exponential_moving_average(df: pd.DataFrame, x: str, y: str, span: int = 10, **kwargs) -> pd.DataFrame:
    """Exponential moving average smoothing."""
    df = df.sort_values(x).copy()
    df[f"{y}_smooth"] = df[y].ewm(span=span, adjust=False).mean()
    return df


def savitzky_golay_smooth(
    df: pd.DataFrame, x: str, y: str, window_length: int = 5, polyorder: int = 2, **kwargs
) -> pd.DataFrame:
    """Savitzky-Golay smoothing."""
    from scipy.signal import savgol_filter

    df = df.sort_values(x).copy()
    df[f"{y}_smooth"] = savgol_filter(df[y], window_length, polyorder)
    return df
