import numpy as np

from skferm.growth_models.gompertz import gompertz, modified_gompertz


def test_gompertz():
    t = np.linspace(0, 10, 100)
    a, b, c = 1.0, 1.0, 1.0
    result = gompertz(t, a, b, c)
    assert result is not None
    assert len(result) == len(t)
    assert np.all(result >= 0)


def test_modified_gompertz():
    t = np.linspace(0, 10, 100)
    A, L, mu = 1.0, 1.0, 1.0
    result = modified_gompertz(t, A, L, mu)
    assert result is not None
    assert len(result) == len(t)
    assert np.all(result >= 0)
