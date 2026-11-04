"""
Unit tests of InvalidChartDataError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_chart_data_error import InvalidChartDataError
from numdaplot.errors.numdaplot_error import NumdaplotError

CHART_NAME = "LineChart"
SETTING_NAME = "y"
DATA_NAME = "an Array"
NEEDS_SETTING = False
EXPECTED_MESSAGE = "LineChart takes no y for an Array."
TABLE_NAME = "a Table"
EXPECTED_MISSING_MESSAGE = "LineChart needs y for a Table."


def test_invalid_chart_data_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidChartDataError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidChartDataError, NumdaplotError)


def test_invalid_chart_data_error_message_states_the_extra_setting() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidChartDataError(CHART_NAME, SETTING_NAME, DATA_NAME, NEEDS_SETTING)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_chart_data_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidChartDataError(CHART_NAME, SETTING_NAME, DATA_NAME, NEEDS_SETTING)

	assert error.chart_name == CHART_NAME
	assert error.setting_name == SETTING_NAME
	assert error.data_name == DATA_NAME
	assert error.needs_setting == NEEDS_SETTING


def test_invalid_chart_data_error_message_states_the_missing_setting() -> None:
	"""
	Check the message of a setting a Table needs.

	.. versionadded:: 0.1.0
	"""
	error = InvalidChartDataError(CHART_NAME, SETTING_NAME, TABLE_NAME, True)

	error_text = str(error)
	assert error_text == EXPECTED_MISSING_MESSAGE
