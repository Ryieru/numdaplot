"""
Unit tests of the values a histogram or a box chart sums up.

.. versionadded:: 0.1.0
"""

from datetime import time

import numpy
import pandas
import pytest

import numdaplot as ndp
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.invalid_chart_data_error import InvalidChartDataError
from numdaplot.plots.data.sample_values import drop_missing_numbers, read_sample_values

CHART_NAME = "BoxChart"
FLATS_FRAME = pandas.DataFrame(
	{
		"city": ["Paris", None, "Lyon"],
		"price": [12.0, 9.5, None],
		"rooms": [2.0, 3.0, 1.0],
	}
)
FLATS = ndp.Table.from_pandas(FLATS_FRAME)
GRID = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
TWO_COLUMNS = ["price", "rooms"]
SINGLE_COLUMN = ["price"]
EXPECTED_GROUPS = ["Paris", None, "Lyon"]
EXPECTED_ARRAY_NAMES = ["0", "1"]
NUMBERS_WITH_GAPS = numpy.array([numpy.nan, 3.0, numpy.nan, 1.0])
EXPECTED_PRESENT_NUMBERS = [3.0, 1.0]
HOUR_SAMPLES = ndp.Array.from_list([time(8), time(20)])
HOUR_TABLE = ndp.Table.from_arrays({"hour": HOUR_SAMPLES})
HOUR_COLUMN = ["hour"]


def test_read_sample_values_reads_each_column_of_a_table() -> None:
	"""
	Check that each column is a series, missing values kept as NaN.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(FLATS, TWO_COLUMNS, None, CHART_NAME)

	names = [series.name for series in samples.series]
	price_missing = numpy.isnan(samples.series[0].values).tolist()
	assert names == TWO_COLUMNS
	assert price_missing == [False, False, True]
	assert samples.groups is None
	assert samples.value_name == "price, rooms"


def test_read_sample_values_names_the_axis_after_a_single_column() -> None:
	"""
	Check that a single column gives the default label of the values.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(FLATS, SINGLE_COLUMN, None, CHART_NAME)

	assert samples.value_name == "price"


def test_read_sample_values_reads_the_group_of_each_row() -> None:
	"""
	Check that group_by gives the text of each row, None where it is missing.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(FLATS, SINGLE_COLUMN, "city", CHART_NAME)

	groups = samples.groups
	assert groups is not None
	assert groups.tolist() == EXPECTED_GROUPS
	assert samples.group_name == "city"


def test_read_sample_values_reads_each_column_of_an_array() -> None:
	"""
	Check that each column of an Array is a series named after its number.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(GRID, None, None, CHART_NAME)

	names = [series.name for series in samples.series]
	assert names == EXPECTED_ARRAY_NAMES
	assert samples.value_name == "Value"


def test_read_sample_values_rejects_a_table_without_columns() -> None:
	"""
	Check that a Table needs columns.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError, match="needs columns"):
		read_sample_values(FLATS, None, None, CHART_NAME)


def test_read_sample_values_rejects_group_by_for_an_array() -> None:
	"""
	Check that an Array takes no group_by.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError, match="takes no group_by"):
		read_sample_values(GRID, None, "city", CHART_NAME)


def test_read_sample_values_rejects_an_unknown_group_column() -> None:
	"""
	Check that an unknown group_by raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		read_sample_values(FLATS, SINGLE_COLUMN, "country", CHART_NAME)


def test_read_sample_values_rejects_groups_of_numbers() -> None:
	"""
	Check that a group_by holding numbers raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_sample_values(FLATS, SINGLE_COLUMN, "rooms", CHART_NAME)


def test_drop_missing_numbers_keeps_the_present_numbers_in_order() -> None:
	"""
	Check that NaN values are removed and the others keep their order.

	.. versionadded:: 0.1.0
	"""
	present_numbers = drop_missing_numbers(NUMBERS_WITH_GAPS)

	assert present_numbers.tolist() == EXPECTED_PRESENT_NUMBERS


def test_read_sample_values_gives_the_type_of_the_columns() -> None:
	"""
	Check that a Table of times of day gives the TIME type.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(HOUR_TABLE, HOUR_COLUMN, None, CHART_NAME)

	assert samples.value_type == ndp.Type.TIME


def test_read_sample_values_gives_the_type_of_an_array() -> None:
	"""
	Check that an Array of times of day gives the TIME type.

	.. versionadded:: 0.1.0
	"""
	samples = read_sample_values(HOUR_SAMPLES, None, None, CHART_NAME)

	assert samples.value_type == ndp.Type.TIME
