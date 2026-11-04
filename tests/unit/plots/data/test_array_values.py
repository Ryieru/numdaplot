"""
Unit tests of the values a chart draws from an Array.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.array_values import read_array_values

CHART_NAME = "LineChart"
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
GRID = ndp.Array.from_list([[1, 2], [3, 4], [5, 6]])
CUBE = ndp.Array.from_list([[[1, 2]], [[3, 4]]])
CITIES = ndp.Array.from_list(["Paris", "Lyon"])
EXPECTED_ROW_NUMBERS = [0.0, 1.0, 2.0]
EXPECTED_SECOND_COLUMN = [2.0, 4.0, 6.0]


def test_read_array_values_draws_a_one_dimensional_array_as_one_series() -> None:
	"""
	Check that a one-dimensional Array is a single series placed at its row numbers.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_array_values(PRICES, CHART_NAME)

	positions = chart_values.positions.values.tolist()
	series_count = len(chart_values.series)
	assert positions == EXPECTED_ROW_NUMBERS
	assert series_count == 1
	assert chart_values.value_name is None


def test_read_array_values_draws_each_column_as_a_series_named_by_its_number() -> None:
	"""
	Check that each column of a two-dimensional Array is a series named 0, 1 and so on.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_array_values(GRID, CHART_NAME)

	names = [series.name for series in chart_values.series]
	second_column = chart_values.series[1].values.tolist()
	assert names == ["0", "1"]
	assert second_column == EXPECTED_SECOND_COLUMN


def test_read_array_values_rejects_three_dimensions() -> None:
	"""
	Check that an Array of three dimensions raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DimensionError):
		read_array_values(CUBE, CHART_NAME)


def test_read_array_values_rejects_texts() -> None:
	"""
	Check that an Array of texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_array_values(CITIES, CHART_NAME)
