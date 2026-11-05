"""
Unit tests of require_chart_class.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.chart_requirement import require_chart_class
from numdaplot.plots.charts.line_chart import LineChart

FUNCTION_NAME = "plot_bar"
EXPECTED_MESSAGE = "The chart LineChart with plot_bar is not available, use a BarChart instead."


def test_require_chart_class_accepts_the_drawn_chart() -> None:
	"""
	Check that the chart class of the function passes.

	.. versionadded:: 0.1.0
	"""
	require_chart_class(BarChart(), BarChart, FUNCTION_NAME)


def test_require_chart_class_refuses_another_chart() -> None:
	"""
	Check that another chart class is refused with a message naming the expected class.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError) as error_info:
		require_chart_class(LineChart(), BarChart, FUNCTION_NAME)

	message = str(error_info.value)
	assert message == EXPECTED_MESSAGE
