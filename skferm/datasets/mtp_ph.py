from importlib.resources import files

import pandas as pd


def load_mtp_ph_data() -> pd.DataFrame:
    """
    Load the MTP pH dataset from the package resources. This data represents acidification curves coming from a micro titer plate.

    Returns:
        pd.DataFrame: DataFrame containing the MTP pH dataset.
    """
    mtp_ph_path = files("skferm.data").joinpath("mtp_ph_data.csv.gz")
    with mtp_ph_path.open("rb") as f:
        df = pd.read_csv(f, compression="gzip")

    return df
