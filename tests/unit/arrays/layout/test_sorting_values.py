"""
Unit tests of sort_values and sort_slice.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.arrays.layout.sorting_values import sort_slice, sort_values
from numdaplot.errors.positions.dimension_error import DimensionError
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.positions.axis import Axis

GRID = [[3, 1], [2, 4]]
EXPECTED_ROWS_SORTED = [[1, 3], [2, 4]]
EXPECTED_COLUMNS_SORTED = [[2, 1], [3, 4]]
DECIMALS = [1.0, numpy.nan, 3.0]
DESCENDING = ArraySorting(order=Order.DESCENDING)
EXPECTED_DESCENDING_PRESENT_VALUES = [3.0, 1.0]
MISSING_FIRST = ArraySorting(missing=MissingPosition.FIRST)
TEXT_DTYPE = "T"
TEXTS = ["b", "a", "c"]
EXPECTED_DESCENDING_TEXTS = ["c", "b", "a"]
LINE = [3, 1, 2]
DEFAULT_SORTING = ArraySorting()


def test_sort_values_sorts_each_row_by_default() -> None:
	"""
	Check that rows are sorted on their own without axis.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	sorted_values = sort_values(values, DEFAULT_SORTING, None)

	sorted_rows = sorted_values.tolist()
	assert sorted_rows == EXPECTED_ROWS_SORTED


def test_sort_values_sorts_each_column() -> None:
	"""
	Check that EACH_COLUMN sorts the values inside each column.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	sorted_values = sort_values(values, DEFAULT_SORTING, Axis.EACH_COLUMN)

	sorted_rows = sorted_values.tolist()
	assert sorted_rows == EXPECTED_COLUMNS_SORTED


def test_sort_values_rejects_an_axis_on_one_dimension() -> None:
	"""
	Check that an axis on a one-dimensional Array raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LINE)

	with pytest.raises(DimensionError):
		sort_values(values, DEFAULT_SORTING, Axis.EACH_ROW)


def test_sort_slice_keeps_missing_values_last_in_descending_order() -> None:
	"""
	Check that NaN stays last when sorting downwards.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	sorted_values = sort_slice(values, DESCENDING)

	present_values = sorted_values[:-1]
	present_list = present_values.tolist()
	last_value = sorted_values[-1]
	is_missing_last = numpy.isnan(last_value)
	assert present_list == EXPECTED_DESCENDING_PRESENT_VALUES
	assert is_missing_last


def test_sort_slice_can_put_missing_values_first() -> None:
	"""
	Check that MissingPosition.FIRST puts NaN before the values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	sorted_values = sort_slice(values, MISSING_FIRST)

	first_value = sorted_values[0]
	is_missing_first = numpy.isnan(first_value)
	assert is_missing_first


def test_sort_slice_orders_texts_alphabetically() -> None:
	"""
	Check that texts are sorted downwards in reverse alphabetical order.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	sorted_values = sort_slice(values, DESCENDING)

	sorted_list = sorted_values.tolist()
	assert sorted_list == EXPECTED_DESCENDING_TEXTS
