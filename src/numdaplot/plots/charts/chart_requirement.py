"""
Check that a plot function receives the chart it draws.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.plots.charts.chart import Chart
from numdaplot.settings.setting_types import require_object_not_class

WRONG_CHART_OPERATION = "The chart {chart_name} with {function_name}"
WRONG_CHART_ALTERNATIVE = "a {expected_name}"
CHART_SETTING = "plot chart"
CHART_EXPECTED = "a chart such as ndp.LineChart()"


def require_chart_class(chart: Chart, chart_class: type[Chart], function_name: str) -> None:
	"""
	Check that a chart is an instance of the chart class a plot function draws.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The chart given to the plot function.
	chart_class
		The chart class the function draws, such as ``BarChart`` for ``plot_bar``.
	function_name
		Name of the plot function, shown in the error message.

	Raises
	------
	InvalidSettingTypeError
		When ``chart`` is a class, written without its parentheses.
	RefusedOperationError
		When the chart is not an instance of ``chart_class``, such as a chart class written outside numdaplot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.charts.chart_requirement import require_chart_class
	>>> try:
	... 	require_chart_class(ndp.LineChart(), ndp.BarChart, "plot_bar")
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	The chart LineChart with plot_bar is not available, use a BarChart instead.
	"""
	require_object_not_class(CHART_SETTING, CHART_EXPECTED, chart)

	is_expected_chart = isinstance(chart, chart_class)
	if is_expected_chart:
		return

	given_class = type(chart)
	operation = WRONG_CHART_OPERATION.format(chart_name=given_class.__name__, function_name=function_name)
	alternative = WRONG_CHART_ALTERNATIVE.format(expected_name=chart_class.__name__)
	raise RefusedOperationError(operation, alternative)
