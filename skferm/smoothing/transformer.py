from sklearn.base import BaseEstimator, TransformerMixin


class SmoothingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, smoothing_function, **kwargs):
        """
        Initialize the transformer.

        Parameters:
        - smoothing_function: Callable
            A function that applies smoothing to a 1D array.
        - kwargs: dict
            Additional arguments to pass to the smoothing function.
        """
        self.smoothing_function = smoothing_function
        self.kwargs = kwargs

    def fit(self, X, y=None):
        """
        Fit method (no-op for this transformer).

        Parameters:
        - X: pd.DataFrame
            Input DataFrame containing noisy curves.
        - y: Ignored
            Not used, present for compatibility.

        Returns:
        - self: SmoothingTransformer
            The fitted transformer.
        """
        return self

    def transform(self, X):
        """
        Apply smoothing to each curve grouped by 'sample_id'.

        Parameters:
        - X: pd.DataFrame
            Input DataFrame with columns ['sample_id', 'time', 'value'].

        Returns:
        - pd.DataFrame
            DataFrame with smoothed 'value' column.
        """
        if not {"sample_id", "time", "value"}.issubset(X.columns):
            raise ValueError("Input DataFrame must contain 'sample_id', 'time', and 'value' columns.")

        def smooth_group(group):
            group["value"] = self.smoothing_function(group["value"].values, **self.kwargs)
            return group

        return X.groupby("sample_id").apply(smooth_group).reset_index(drop=True)
