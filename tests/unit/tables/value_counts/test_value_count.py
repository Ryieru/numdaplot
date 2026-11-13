"""
Unit tests of ValueCount.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.types.invalid_type_error import InvalidTypeError
from numdaplot.measures.measure import Measure
from numdaplot.tables.value_counts.value_count import ValueCount

COUNTED_COLUMN = "sex"
EMPTY_COLUMN_NAME = ""
COLUMN_POSITION = 0


def test_value_count_counts_rows_by_default() -> None:
	"""
	Check the default measure.

	.. versionadded:: 0.2.0
	"""
	value_count = ValueCount(column=COUNTED_COLUMN)

	assert value_count.measure == Measure.COUNT


def test_value_count_rejects_an_empty_column_name() -> None:
	"""
	Check that an empty column name raises InvalidColumnNameError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidColumnNameError):
		ValueCount(column=EMPTY_COLUMN_NAME)


def test_value_count_rejects_a_column_that_is_not_a_name() -> None:
	"""
	Check that a column given by position raises InvalidTypeError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidTypeError):
		ValueCount(column=COLUMN_POSITION)  # pyright: ignore[reportArgumentType]


def test_value_count_counts_every_row_once_by_default() -> None:
	"""
	Check that no column of weights is set by default.

	.. versionadded:: 0.2.0
	"""
	value_count = ValueCount(column=COUNTED_COLUMN)

	assert value_count.weights is None


def test_value_count_rejects_an_empty_weights_name() -> None:
	"""
	Check that an empty name of weights raises InvalidColumnNameError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidColumnNameError):
		ValueCount(column=COUNTED_COLUMN, weights=EMPTY_COLUMN_NAME)
