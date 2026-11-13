"""
Unit tests of the check of the number of positions taken from the start or the end of a dimension.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.positions.position_count import MINIMUM_POSITION_COUNT, require_position_count

NO_COUNT = 0


def test_require_position_count_accepts_one_position() -> None:
	"""
	Check that a single position is accepted.

	.. versionadded:: 0.2.0
	"""
	require_position_count(MINIMUM_POSITION_COUNT)


def test_require_position_count_rejects_no_position() -> None:
	"""
	Check that 0 positions raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		require_position_count(NO_COUNT)
