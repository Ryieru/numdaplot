"""
Unit tests of Normal.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.normal import Normal
from numdaplot.errors.distributions.invalid_deviation_error import InvalidDeviationError

MEAN = 170.0
DEVIATION = 10.0
ZERO_DEVIATION = 0.0
NEGATIVE_DEVIATION = -1.0


def test_normal_keeps_its_mean_and_deviation() -> None:
	"""
	Check that the mean and the deviation are available as attributes.

	.. versionadded:: 0.1.0
	"""
	distribution = Normal(mean=MEAN, deviation=DEVIATION)

	assert distribution.mean == MEAN
	assert distribution.deviation == DEVIATION


def test_normal_accepts_a_zero_deviation() -> None:
	"""
	Check that a deviation of 0, giving the mean every time, is accepted.

	.. versionadded:: 0.1.0
	"""
	distribution = Normal(mean=MEAN, deviation=ZERO_DEVIATION)

	assert distribution.deviation == ZERO_DEVIATION


def test_normal_rejects_a_negative_deviation() -> None:
	"""
	Check that a negative deviation is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidDeviationError):
		Normal(mean=MEAN, deviation=NEGATIVE_DEVIATION)
