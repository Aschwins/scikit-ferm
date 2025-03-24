import pytest
import numpy as np
from skferm.datasets.synthetic import generate_synthetic_growth


def test_generate_synthetic_growth_logistic_no_noise():
    time = np.linspace(0, 10, 100)
    result = generate_synthetic_growth(
        time, model="logistic", noise_std=0.0, r=0.1, Nmax=100, N0=1
    )
    assert "time" in result
    assert "population" in result
    assert len(result["time"]) == len(time)
    assert len(result["population"]) == len(time)
    assert np.all(result["population"] >= 0)


def test_generate_synthetic_growth_logistic_with_noise():
    time = np.linspace(0, 10, 100)
    noise_std = 0.1
    result = generate_synthetic_growth(
        time, model="logistic", noise_std=noise_std, r=0.1, Nmax=100, N0=1
    )
    assert "time" in result
    assert "population" in result
    assert len(result["time"]) == len(time)
    assert len(result["population"]) == len(time)
    assert np.all(result["population"] >= 0)
    assert (
        np.std(
            result["population"]
            - generate_synthetic_growth(
                time, model="logistic", noise_std=0.0, r=0.1, Nmax=100, N0=1
            )["population"]
        )
        > 0
    )


def test_generate_synthetic_growth_invalid_model():
    time = np.linspace(0, 10, 100)
    with pytest.raises(ValueError, match="Unsupported model: invalid_model"):
        generate_synthetic_growth(
            time, model="invalid_model", noise_std=0.0, r=0.1, Nmax=100, N0=1
        )
