from scipy.interpolate import UnivariateSpline


class FermentationCurveSmoother:
    def __init__(self, x, y, smoothing_factor=None):
        """Initialize the curve smoother."""
        self.spline = UnivariateSpline(x, y, s=smoothing_factor, k=3)

    def get_smoothed_values(self, new_x):
        """Get smoothed values at given new_x."""
        return self.spline(new_x)


# Function to apply smoothing to each sample_id
def smooth_fermentation_data(df, x, y, groupby_col, smoothing_factor=None):
    """
    Applies smoothing to each unique fermentation curve (grouped by sample_id).

    Parameters:
    - df: Pandas DataFrame with columns ['time', 'pH', 'sample_id'].
    - smoothing_factor: Optional, controls smoothness.

    Returns:
    - DataFrame with an added 'pH_smooth' column.
    """

    def smooth_group(group):
        smoother = FermentationCurveSmoother(group[x].values, group[y].values, smoothing_factor)
        group["pH_smooth"] = smoother.get_smoothed_values(group[x].values)
        return group

    return df.groupby(groupby_col, group_keys=False).apply(smooth_group)
