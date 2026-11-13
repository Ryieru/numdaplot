"""
Unit tests of Logarithm.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_base_error import InvalidBaseError
from numdaplot.math_functions.logarithm import Logarithm

DECIMAL_BASE = 10
REJECTED_BASES = [0, -2, 1]


def test_logarithm_is_natural_by_default() -> None:
	"""
	Check that the base is omitted, meaning e, by default.

	.. versionadded:: 0.1.0
	"""
	logarithm = Logarithm()

	assert logarithm.base is None


def test_logarithm_keeps_its_base() -> None:
	"""
	Check that a given base is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	logarithm = Logarithm(base=DECIMAL_BASE)

	assert logarithm.base == DECIMAL_BASE


@pytest.mark.parametrize("base", REJECTED_BASES)
def test_logarithm_rejects_an_unusable_base(base: float) -> None:
	"""
	Check that a base lower than or equal to 0, or equal to 1, is rejected.

	.. versionadded:: 0.1.0

	Parameters
	----------
	base
		A rejected base.
	"""
	with pytest.raises(InvalidBaseError):
		Logarithm(base=base)
