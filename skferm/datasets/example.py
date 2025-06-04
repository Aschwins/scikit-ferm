from importlib.resources import files

import pandas as pd


def load_rheolaser_data():
    """
    Load the Rheolaser dataset from the package resources.

    Returns:
        pd.DataFrame: DataFrame containing the Rheolaser dataset.
    """
    rheolaser_path = files("skferm.data").joinpath("rheolaser_export.csv.gz")
    with rheolaser_path.open("rb") as f:
        df = pd.read_csv(f, compression="gzip")

    return df
