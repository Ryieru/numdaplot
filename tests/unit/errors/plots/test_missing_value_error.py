"""
Unit tests of MissingValueError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.missing_value_error import MissingValueError

CHART_NAME = "PieChart"
COLUMN_NAME = "sales"
EXPECTED_MESSAGE = "PieChart cannot draw a missing value, found one in 'sales'."


def test_missing_value_error_is_a_numdaplot_error() -> None:
	"""
	Check that MissingValueError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(MissingValueError, NumdaplotError)


def test_missing_value_error_message_states_the_chart_and_the_column() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = MissingValueError(CHART_NAME, COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_missing_value_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = MissingValueError(CHART_NAME, COLUMN_NAME)

	assert error.chart_name == CHART_NAME
	assert error.column_name == COLUMN_NAME
