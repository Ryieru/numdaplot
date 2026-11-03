"""
Functional tests of the layout of an Array: shape, order and distinct values.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

LINE = [1, 2, 3, 4, 5, 6]
GRID_SHAPE = ndp.Shape((2, 3))
EXPECTED_GRID = [[1, 2, 3], [4, 5, 6]]
EXPECTED_TRANSPOSED = [[1, 4], [2, 5], [3, 6]]
WRONG_SHAPE = ndp.Shape((4, 2))
SCORES = [[3, 1, 2], [9, 7, 8]]
EXPECTED_ROWS_SORTED = [[1, 2, 3], [7, 8, 9]]
EXPECTED_COLUMNS_DESCENDING = [[9, 7, 8], [3, 1, 2]]
COUNTRIES = ["FR", "DE", "FR", "IT"]
EXPECTED_UNIQUE_COUNTRIES = ["DE", "FR", "IT"]
TEMPERATURES = [12.0, None, 18.0]
EXPECTED_PRESENT_FIRST = [18.0, 12.0]
LINE_SORTING = ndp.ArraySorting(axis=ndp.Axis.EACH_ROW)
LAST_VALUE = ndp.Region(rows=ndp.Index(-1))


def test_a_line_is_reshaped_into_a_grid() -> None:
	"""
	Check that six values become two rows of three.

	.. versionadded:: 0.1.0
	"""
	line = ndp.Array.from_list(LINE)

	grid = line.reshape(GRID_SHAPE)

	grid_rows = grid.to_list()
	assert grid_rows == EXPECTED_GRID


def test_a_grid_is_transposed_and_flattened_back() -> None:
	"""
	Check transpose, then flatten of the original grid.

	.. versionadded:: 0.1.0
	"""
	line = ndp.Array.from_list(LINE)
	grid = line.reshape(GRID_SHAPE)

	transposed = grid.transpose()
	flattened = grid.flatten()

	transposed_rows = transposed.to_list()
	flat_list = flattened.to_list()
	assert transposed_rows == EXPECTED_TRANSPOSED
	assert flat_list == LINE


def test_a_reshape_to_another_size_is_rejected() -> None:
	"""
	Check that six values cannot fill eight positions.

	.. versionadded:: 0.1.0
	"""
	line = ndp.Array.from_list(LINE)

	with pytest.raises(ndp.ShapeMismatchError):
		line.reshape(WRONG_SHAPE)


def test_each_row_is_sorted_by_default() -> None:
	"""
	Check that sorting without axis sorts each row.

	.. versionadded:: 0.1.0
	"""
	scores = ndp.Array.from_list(SCORES)

	sorted_scores = scores.sort(ndp.ArraySorting())

	sorted_rows = sorted_scores.to_list()
	assert sorted_rows == EXPECTED_ROWS_SORTED


def test_each_column_is_sorted_downwards() -> None:
	"""
	Check a descending sort inside each column.

	.. versionadded:: 0.1.0
	"""
	scores = ndp.Array.from_list(SCORES)
	sorting = ndp.ArraySorting(order=ndp.Order.DESCENDING, axis=ndp.Axis.EACH_COLUMN)

	sorted_scores = scores.sort(sorting)

	sorted_rows = sorted_scores.to_list()
	assert sorted_rows == EXPECTED_COLUMNS_DESCENDING


def test_missing_values_stay_last_in_a_descending_sort() -> None:
	"""
	Check that the missing temperature comes last when sorting downwards.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)
	sorting = ndp.ArraySorting(order=ndp.Order.DESCENDING)

	sorted_temperatures = temperatures.sort(sorting)

	present_temperatures = sorted_temperatures.select(ndp.IsPresent())
	present_list = present_temperatures.to_list()
	last_temperature = sorted_temperatures.take(LAST_VALUE)
	last_mask = last_temperature.check(ndp.IsMissing())
	last_is_missing = last_mask.to_value()
	assert present_list == EXPECTED_PRESENT_FIRST
	assert last_is_missing


def test_an_axis_on_a_line_is_rejected() -> None:
	"""
	Check that sorting a one-dimensional Array along an axis raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	line = ndp.Array.from_list(LINE)

	with pytest.raises(ndp.DimensionError):
		line.sort(LINE_SORTING)


def test_distinct_values_are_listed_once_and_sorted() -> None:
	"""
	Check unique on countries.

	.. versionadded:: 0.1.0
	"""
	countries = ndp.Array.from_list(COUNTRIES)

	unique_countries = countries.unique()

	unique_list = unique_countries.to_list()
	assert unique_list == EXPECTED_UNIQUE_COUNTRIES
