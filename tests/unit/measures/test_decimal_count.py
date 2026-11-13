"""
Unit tests of the check of the number of decimals written in a file.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.measures.decimal_count import require_decimal_count

NEGATIVE_DECIMALS = -1


@pytest.mark.parametrize("decimals", [None, 0, 2])
def test_require_decimal_count_accepts_no_count_or_a_count_from_zero(decimals: int | None) -> None:
	"""
	Check that an omitted count, 0 and more raise nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	decimals
		An accepted number of decimals.
	"""
	require_decimal_count(decimals)


def test_require_decimal_count_rejects_a_negative_count() -> None:
	"""
	Check that a negative number of decimals raises InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		require_decimal_count(NEGATIVE_DECIMALS)
