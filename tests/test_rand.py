"""Test random.py"""
import pytest
import torch  # type: ignore

from leabra7 import rand as rn


def test_distribution_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        rn.Distribution()


def test_scalar_is_always_equal_to_its_value() -> None:
    dist = rn.Scalar(3)
    x = torch.Tensor(10)
    dist.fill(x)
    assert (x == 3).all()


def test_uniform_is_always_within_its_range() -> None:
    dist = rn.Uniform(2, 3)
    x = torch.Tensor(10)
    dist.fill(x)
    assert ((2 <= x) & (x <= 3)).all()


def test_uniform_checks_low_is_less_than_high() -> None:
    with pytest.raises(ValueError):
        rn.Uniform(3, 2)


def test_gaussian_can_be_used() -> None:
    dist = rn.Gaussian(2, 3)
    x = torch.Tensor(10)
    dist.fill(x)


def test_gaussian_checks_variance_is_positive() -> None:
    with pytest.raises(ValueError):
        rn.Gaussian(mean=0, var=-1)


def test_lognormal_is_always_postiive() -> None:
    dist = rn.LogNormal(2, 3)
    x = torch.Tensor(10)
    dist.fill(x)
    assert (x >= 0).all()


def test_lognormal_checks_variance_is_positive() -> None:
    with pytest.raises(ValueError):
        rn.LogNormal(2, -3)


def test_exponential_can_be_used() -> None:
    dist = rn.Exponential(3)
    x = torch.Tensor(10)
    dist.fill(x)
