"""
Unit tests of Last.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import pytest

from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.positions.last import Last

COUNT = 10
NO_COUNT = 0
NEGATIVE_COUNT = -2
DECIMAL_COUNT = 2.5


def test_last_keeps_its_count() -> None:
	"""
	Check that the count is available as an attribute.

	.. versionadded:: 0.2.0
	"""
	positions = Last(COUNT)

	assert positions.count == COUNT


def test_last_rejects_no_position() -> None:
	"""
	Check that a count of 0 raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		Last(NO_COUNT)


def test_last_rejects_a_negative_count() -> None:
	"""
	Check that a negative count raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		Last(NEGATIVE_COUNT)


def test_last_rejects_a_decimal_count() -> None:
	"""
	Check that a decimal count raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	untyped_positions = cast(Any, Last)

	with pytest.raises(InvalidTypeError):
		untyped_positions(DECIMAL_COUNT)
