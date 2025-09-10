import pytest
from brain.core import entropy_delta


def test_entropy_delta_basics():
    assert entropy_delta([1, 1, 1]) == 0.0
    assert 0.0 < entropy_delta([1, 2, 3]) <= 1.0


def test_entropy_delta_empty_and_nans_safe():
    assert entropy_delta([]) == 0.0
    assert entropy_delta([float("nan"), 5.0]) == 0.0


def test_entropy_delta_ignores_internal_nans():
    assert entropy_delta([1.0, float("nan"), 5.0]) == pytest.approx(0.8)
