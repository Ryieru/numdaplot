"""
Unit tests of Uniform.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.distribution import Distribution
from numdaplot.arrays.creation.uniform import Uniform
from numdaplot.errors.rules.invalid_bounds_error import InvalidBoundsError

LOW = 0.0
HIGH = 1.0


def test_uniform_is_a_distribution() -> None:
	"""
	Check that Uniform can be given where a distribution is expected.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(Uniform, Distribution)


def test_uniform_keeps_its_bounds() -> None:
	"""
	Check that the bounds are available as attributes.

	.. versionadded:: 0.1.0
	"""
	distribution = Uniform(low=LOW, high=HIGH)

	assert distribution.low == LOW
	assert distribution.high == HIGH


def test_uniform_rejects_reversed_bounds() -> None:
	"""
	Check that a low bound greater than the high bound is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		Uniform(low=HIGH, high=LOW)
