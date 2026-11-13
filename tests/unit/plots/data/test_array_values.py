"""
Unit tests of the values a chart draws from an Array.

.. versionadded:: 0.1.0
"""

from datetime import time

import numpy
import pytest

import numdaplot as ndp
from numdaplot.errors.positions.dimension_error import DimensionError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.array_values import read_array_numbers, read_array_values

CHART_NAME = "LineChart"
PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
GRID = ndp.Array.from_list([[1, 2], [3, 4], [5, 6]])
CUBE = ndp.Array.from_list([[[1, 2]], [[3, 4]]])
CITIES = ndp.Array.from_list(["Paris", "Lyon"])
EXPECTED_ROW_NUMBERS = [0.0, 1.0, 2.0]
EXPECTED_SECOND_COLUMN = [2.0, 4.0, 6.0]
TIME_CHART_NAME = "ScatterChart"
BAR_CHART_NAME = "BarChart"
MORNING_HOURS = ndp.Array.from_list([time(8, 30), time(9, 15)])
EXPECTED_MORNING_HOURS = [8.5, 9.25]
STORED_HALF_PAST_ONE = numpy.array([5400000000], dtype="timedelta64[us]")
EXPECTED_HALF_PAST_ONE = [1.5]
INTEGER_VALUES = numpy.array([3, 4])
EXPECTED_DECIMALS = [3.0, 4.0]


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
	assert chart_values.value_name == "Value"


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


def test_read_array_values_reads_times_in_hours_for_a_chart_measuring_them() -> None:
	"""
	Check that an Array of times of day gives hours and the TIME type.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_array_values(MORNING_HOURS, TIME_CHART_NAME)

	first_series = chart_values.series[0]
	hour_list = first_series.values.tolist()
	assert hour_list == EXPECTED_MORNING_HOURS
	assert chart_values.value_type == ndp.Type.TIME


def test_read_array_values_rejects_times_for_bars() -> None:
	"""
	Check that an Array of times of day drawn as bars raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_array_values(MORNING_HOURS, BAR_CHART_NAME)


def test_read_array_values_keeps_the_type_of_numbers() -> None:
	"""
	Check that an Array of decimals gives the FLOAT64 type.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_array_values(PRICES, CHART_NAME)

	assert chart_values.value_type == ndp.Type.FLOAT64


def test_read_array_numbers_counts_times_in_hours() -> None:
	"""
	Check that stored times of day become their hours since midnight.

	.. versionadded:: 0.1.0
	"""
	numbers = read_array_numbers(STORED_HALF_PAST_ONE, ndp.Type.TIME)

	number_list = numbers.tolist()
	assert number_list == EXPECTED_HALF_PAST_ONE


def test_read_array_numbers_reads_integers_as_decimals() -> None:
	"""
	Check that integers become float64 numbers.

	.. versionadded:: 0.1.0
	"""
	numbers = read_array_numbers(INTEGER_VALUES, ndp.Type.INT64)

	number_list = numbers.tolist()
	assert number_list == EXPECTED_DECIMALS
