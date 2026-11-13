"""
Unit tests of IncompatibleChartsError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.incompatible_charts_error import IncompatibleChartsError

CHART_NAME = "LineChart"
CHART_POSITIONS = "dates"
PLOT_POSITIONS = "texts"
EXPECTED_MESSAGE = "A LineChart with dates cannot be added to a Plot with texts."


def test_incompatible_charts_error_is_a_numdaplot_error() -> None:
	"""
	Check that IncompatibleChartsError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(IncompatibleChartsError, NumdaplotError)


def test_incompatible_charts_error_message_states_both_kinds_of_values() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleChartsError(CHART_NAME, CHART_POSITIONS, PLOT_POSITIONS)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_incompatible_charts_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleChartsError(CHART_NAME, CHART_POSITIONS, PLOT_POSITIONS)

	assert error.chart_name == CHART_NAME
	assert error.chart_positions == CHART_POSITIONS
	assert error.plot_positions == PLOT_POSITIONS
