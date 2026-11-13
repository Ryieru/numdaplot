"""
Unit tests of require_fraction.

.. versionadded:: 0.1.0
"""

import math

import pytest

from numdaplot.errors.measures.invalid_fraction_error import InvalidFractionError
from numdaplot.measures.fraction import require_fraction

ACCEPTED_FRACTIONS = [0.0, 0.25, 1.0]
REJECTED_FRACTIONS = [-0.1, 1.1, math.nan]


@pytest.mark.parametrize("fraction", ACCEPTED_FRACTIONS)
def test_require_fraction_accepts_values_from_zero_to_one_included(fraction: float) -> None:
	"""
	Check that 0, 1 and the values between them are accepted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fraction
		An accepted fraction.
	"""
	require_fraction(fraction)


@pytest.mark.parametrize("fraction", REJECTED_FRACTIONS)
def test_require_fraction_rejects_values_outside_zero_to_one_and_nan(fraction: float) -> None:
	"""
	Check that negative values, values above 1 and NaN are rejected.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fraction
		A rejected value.
	"""
	with pytest.raises(InvalidFractionError):
		require_fraction(fraction)
