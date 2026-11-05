"""
Unit tests of require_whole_position.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.errors.invalid_position_error import InvalidPositionError
from numdaplot.positions.whole_positions import require_whole_position

FIRST_POSITION = 0
WHOLE_POSITIONS = [0, -1, 3, numpy.int64(2)]
REJECTED_POSITIONS = [1.5, True, "1"]
NEGATIVE_POSITION = -1


@pytest.mark.parametrize("position", WHOLE_POSITIONS)
def test_require_whole_position_accepts_whole_numbers(position: object) -> None:
	"""
	Check that Python and numpy integers pass, negative ones included without lowest position.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		A whole number.
	"""
	require_whole_position(position, None)


@pytest.mark.parametrize("position", REJECTED_POSITIONS)
def test_require_whole_position_rejects_other_values(position: object) -> None:
	"""
	Check that a decimal, a boolean or a text raises InvalidPositionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		A value that is not a whole number.
	"""
	with pytest.raises(InvalidPositionError):
		require_whole_position(position, None)


def test_require_whole_position_rejects_a_position_below_the_lowest() -> None:
	"""
	Check that a position below the lowest accepted one raises InvalidPositionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidPositionError):
		require_whole_position(NEGATIVE_POSITION, FIRST_POSITION)
