from skferm.datasets.rheolaser import load_rheolaser_data


def test_load_rheolaser_data():
    # Load the raw data
    df = load_rheolaser_data(clean=False)

    # Check if the DataFrame is not empty
    assert not df.empty, "The loaded DataFrame should not be empty."


def test_load_rheolaser_data_clean():
    # Load the cleaned data
    df = load_rheolaser_data(clean=True)

    # Check if the DataFrame is not empty
    assert not df.empty, "The cleaned DataFrame should not be empty."

    # Check if the DataFrame has the expected columns
    expected_columns = ["sample_id", "time", "elasticity_index"]
    assert all(col in df.columns for col in expected_columns), f"DataFrame should contain columns: {expected_columns}"

    # Check if 'time' is in minutes and 'elasticity_index' is in mPa
    assert df["time"].min() >= 0, "Time values should be non-negative."
    assert df["elasticity_index"].min() >= 0, "Elasticity index values should be non-negative."
