"""
Unit tests of ValueLabels.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.plots.charts.value_labels import ValueLabels

DEFAULT_DECIMALS = 2
NO_DECIMALS = 0
NEGATIVE_DECIMALS = -1
DECIMAL_TEXT = "2"


def test_value_labels_write_two_decimals_by_default() -> None:
	"""
	Check the default number of decimals.

	.. versionadded:: 0.2.0
	"""
	value_labels = ValueLabels()

	assert value_labels.decimals == DEFAULT_DECIMALS


def test_value_labels_accept_no_decimals() -> None:
	"""
	Check that 0 decimals is accepted.

	.. versionadded:: 0.2.0
	"""
	value_labels = ValueLabels(decimals=NO_DECIMALS)

	assert value_labels.decimals == NO_DECIMALS


def test_value_labels_reject_negative_decimals() -> None:
	"""
	Check that a negative number of decimals raises InvalidCountError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidCountError):
		ValueLabels(decimals=NEGATIVE_DECIMALS)


def test_value_labels_reject_decimals_given_as_text() -> None:
	"""
	Check that a number of decimals written as a text raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidTypeError):
		ValueLabels(decimals=DECIMAL_TEXT)  # pyright: ignore[reportArgumentType]
