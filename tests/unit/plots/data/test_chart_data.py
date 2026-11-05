"""
Unit tests of the checks of the column settings of a chart against the data it draws.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.errors.invalid_chart_data_error import InvalidChartDataError
from numdaplot.plots.data.chart_data import (
	read_chart_values,
	require_column_setting,
	require_no_column_settings,
)

CHART_NAME = "BarChart"
PRICES = ndp.Array.from_list([12.0, 15.5])
SALES = ndp.Table.from_arrays({"price": PRICES})
ARRAY_SETTINGS = dict[str, object]({"x": None, "y": None})
SETTINGS_WITH_X = dict[str, object]({"x": "day", "y": None})


def test_require_no_column_settings_accepts_settings_left_out() -> None:
	"""
	Check that settings all None raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_no_column_settings(CHART_NAME, ARRAY_SETTINGS)


def test_require_no_column_settings_rejects_a_given_setting() -> None:
	"""
	Check that a column name given for an Array raises InvalidChartDataError, naming the setting.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError) as error_info:
		require_no_column_settings(CHART_NAME, SETTINGS_WITH_X)

	error = error_info.value
	assert error.setting_name == "x"
	assert not error.needs_setting


def test_require_column_setting_returns_a_given_setting() -> None:
	"""
	Check that a given setting is returned as it is.

	.. versionadded:: 0.1.0
	"""
	setting_value = require_column_setting(CHART_NAME, "y", ["price"])

	assert setting_value == ["price"]


def test_require_column_setting_rejects_a_missing_setting() -> None:
	"""
	Check that a missing setting raises InvalidChartDataError for a Table.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError) as error_info:
		require_column_setting(CHART_NAME, "y", None)

	assert error_info.value.needs_setting


def test_read_chart_values_reads_an_array_without_settings() -> None:
	"""
	Check that an Array is read with each column as a series.

	.. versionadded:: 0.1.0
	"""
	chart_values = read_chart_values(PRICES, None, None, CHART_NAME)

	series_count = len(chart_values.series)
	assert series_count == 1


def test_read_chart_values_rejects_y_for_an_array() -> None:
	"""
	Check that y given for an Array raises InvalidChartDataError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError):
		read_chart_values(PRICES, None, ["price"], CHART_NAME)


def test_read_chart_values_rejects_a_table_without_y() -> None:
	"""
	Check that a Table without y raises InvalidChartDataError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidChartDataError):
		read_chart_values(SALES, None, None, CHART_NAME)
