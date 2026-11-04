"""
Unit tests of the values a chart draws from a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

import numdaplot as ndp
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.data.table_values import read_table_values

CHART_NAME = "LineChart"
SALES_FRAME = pandas.DataFrame(
	{
		"day": [1.0, None, 3.0],
		"city": ["Paris", None, "Pau"],
		"price": [12.0, 15.5, 14.0],
		"cost": [8.0, 9.0, None],
		"open": [True, False, True],
	}
)
SALES = ndp.Table.from_pandas(SALES_FRAME)
EXPECTED_ROW_NUMBERS = [0.0, 1.0, 2.0]
EXPECTED_CITIES = ["Paris", "Pau"]
EXPECTED_KEPT_ROWS = [0, 2]
EXPECTED_CITY_PRICES = [12.0, 14.0]


def test_read_table_values_numbers_the_rows_without_x() -> None:
	"""
	Check that a chart without x places the rows at their numbers, with no x label.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(SALES, None, ["price"], CHART_NAME)

	positions = chart_values.positions
	assert positions.kind == PositionKind.NUMBERS
	assert positions.values.tolist() == EXPECTED_ROW_NUMBERS
	assert positions.name is None


def test_read_table_values_names_a_single_series_as_value_name() -> None:
	"""
	Check that a single y column gives the default label of the values.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(SALES, None, ["price"], CHART_NAME)

	assert chart_values.value_name == "price"


def test_read_table_values_gives_no_value_name_for_several_series() -> None:
	"""
	Check that several y columns give no default label of the values.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(SALES, None, ["price", "cost"], CHART_NAME)

	series_names = [series.name for series in chart_values.series]
	assert chart_values.value_name is None
	assert series_names == ["price", "cost"]


def test_read_table_values_hides_the_values_of_a_missing_number_x() -> None:
	"""
	Check that a row with a missing x number keeps its place, without value, so a line breaks.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(SALES, "day", ["price"], CHART_NAME)

	prices = chart_values.series[0].values
	missing = numpy.isnan(prices).tolist()
	assert missing == [False, True, False]


def test_read_table_values_leaves_out_a_row_with_a_missing_x_text() -> None:
	"""
	Check that a row whose x text is missing is removed, and the kept rows are listed.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_table_values(SALES, "city", ["price"], CHART_NAME)

	cities = chart_values.positions.values.tolist()
	prices = chart_values.series[0].values.tolist()
	rows = chart_values.rows.tolist()
	assert cities == EXPECTED_CITIES
	assert prices == EXPECTED_CITY_PRICES
	assert rows == EXPECTED_KEPT_ROWS


def test_read_table_values_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown y column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		read_table_values(SALES, None, ["prise"], CHART_NAME)


def test_read_table_values_rejects_an_unknown_x_column() -> None:
	"""
	Check that an unknown x column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		read_table_values(SALES, "dya", ["price"], CHART_NAME)


def test_read_table_values_rejects_a_y_column_of_booleans() -> None:
	"""
	Check that a boolean y column raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		read_table_values(SALES, None, ["open"], CHART_NAME)
