"""
Unit tests of First.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.positions.first import First

COUNT = 10
NO_COUNT = 0
NEGATIVE_COUNT = -2
DECIMAL_COUNT = 2.5


def test_first_keeps_its_count() -> None:
	"""
	Check that the count is available as an attribute.

	.. versionadded:: 0.2.0
	"""
	positions = First(COUNT)

	assert positions.count == COUNT


def test_first_rejects_no_position() -> None:
	"""
	Check that a count of 0 raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		First(NO_COUNT)


def test_first_rejects_a_negative_count() -> None:
	"""
	Check that a negative count raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		First(NEGATIVE_COUNT)


def test_first_rejects_a_decimal_count() -> None:
	"""
	Check that a decimal count raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	untyped_positions = cast(Any, First)

	with pytest.raises(InvalidTypeError):
		untyped_positions(DECIMAL_COUNT)
