from typing import Callable, Optional

import pandas as pd


def apply_method_to_groups(
    df: pd.DataFrame, x: str, y: str, method_func: Callable, groupby_col: Optional[str] = None, **kwargs
) -> pd.DataFrame:
    """Apply a method function to groups or entire dataframe."""
    if groupby_col is None:
        return method_func(df, x, y, **kwargs)
    else:
        grouped = [method_func(group, x, y, **kwargs) for _, group in df.groupby(groupby_col, group_keys=False)]
        return pd.concat(grouped, ignore_index=True)
