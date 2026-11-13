"""
Checks of a chart added to a Plot with ``add_line``, ``add_bar`` or ``add_scatter``.

.. versionadded:: 0.1.0
"""

from typing import cast

from numdaplot.errors.incompatible_charts_error import IncompatibleChartsError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.orientation import Orientation
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.types.value_family import ValueFamily, find_family

OVERLAID_CHARTS = (LineChart, BarChart, ScatterChart)
POSITION_NAMES = {
	PositionKind.NUMBERS: "numbers",
	PositionKind.MOMENTS: "dates",
	PositionKind.TEXTS: "texts",
	PositionKind.TIMES: "times of day",
}
VALUE_NAMES = {
	ValueFamily.NUMBER: "numbers",
	ValueFamily.TIME: "times of day",
}
AXIS_NAMES = {
	ValueAxis.LEFT: "left",
	ValueAxis.RIGHT: "right",
}
VALUE_DESCRIPTION = "{value_name} on the {axis_name} axis"
PLOT_NAME = "a Plot of {chart_name}"
HORIZONTAL_BARS_NAME = "a Plot of horizontal bars"
HORIZONTAL_SETTING = "Orientation.HORIZONTAL"


def require_overlay_base(first_layer: ChartLayer, method_name: str) -> None:
	"""
	Check that a Plot accepts added charts: its first chart draws lines, vertical bars or points.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_layer
		The first chart of the Plot and its values.
	method_name
		The method adding a chart, such as ``add_line``, shown in the error message.

	Raises
	------
	RefusedSettingError
		When the first chart is not a LineChart, a BarChart or a ScatterChart, or draws horizontal bars.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.sample_values import read_sample_values
	>>> from numdaplot.plots.overlay_checks import require_overlay_base
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = ChartLayer(ndp.BoxChart(), read_sample_values(prices, None, None, "BoxChart"))
	>>> try:
	... 	require_overlay_base(layer, "add_line")
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	add_line does not accept a Plot of BoxChart.
	"""
	chart = first_layer.chart
	if not isinstance(chart, OVERLAID_CHARTS):
		chart_class = type(chart)
		plot_name = PLOT_NAME.format(chart_name=chart_class.__name__)
		raise RefusedSettingError(plot_name, method_name)

	draws_horizontal_bars = is_horizontal_bar_chart(chart)
	if draws_horizontal_bars:
		raise RefusedSettingError(HORIZONTAL_BARS_NAME, method_name)


def require_vertical_bars(chart: BarChart, method_name: str) -> None:
	"""
	Check that bars added to a Plot are vertical, their ``x`` values sharing the horizontal axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		The bars added.
	method_name
		The method adding them, shown in the error message.

	Raises
	------
	RefusedSettingError
		When the bars are horizontal.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.overlay_checks import require_vertical_bars
	>>> try:
	... 	require_vertical_bars(ndp.BarChart(orientation=ndp.Orientation.HORIZONTAL), "add_bar")
	... except ndp.RefusedSettingError as error:
	... 	print(error)
	add_bar does not accept Orientation.HORIZONTAL.
	"""
	if chart.orientation == Orientation.HORIZONTAL:
		raise RefusedSettingError(HORIZONTAL_SETTING, method_name)


def require_same_positions(first_layer: ChartLayer, added_layer: ChartLayer) -> None:
	"""
	Check that a chart added to a Plot has the same kind of ``x`` values as its first chart.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_layer
		The first chart of the Plot and its values.
	added_layer
		The chart added and its values.

	Raises
	------
	IncompatibleChartsError
		When one has numbers, dates or texts and the other another kind.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.overlay_checks import require_same_positions
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))
	>>> require_same_positions(layer, layer)
	"""
	first_values = cast(ChartValues, first_layer.values)
	added_values = cast(ChartValues, added_layer.values)
	plot_kind = first_values.positions.kind
	added_kind = added_values.positions.kind
	if added_kind == plot_kind:
		return

	added_class = type(added_layer.chart)
	added_name = POSITION_NAMES[added_kind]
	plot_name = POSITION_NAMES[plot_kind]
	raise IncompatibleChartsError(added_class.__name__, added_name, plot_name)


def require_same_values(layers: list[ChartLayer], added_layer: ChartLayer, axis: ValueAxis) -> None:
	"""
	Check that a chart added to a Plot measures the same kind of values as the charts already on its axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.
	added_layer
		The chart added and its values.
	axis
		The vertical axis the added chart is measured on.

	Raises
	------
	IncompatibleChartsError
		When one measures numbers and the other times of day on the same axis.

	Examples
	--------
	>>> from datetime import time
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.overlay_checks import require_same_values
	>>> counts = ndp.Array.from_list([3.0, 5.0])
	>>> hours = ndp.Array.from_list([time(8), time(9)])
	>>> count_line = ChartLayer(ndp.LineChart(), read_array_values(counts, "LineChart"))
	>>> hour_line = ChartLayer(ndp.LineChart(), read_array_values(hours, "LineChart"))
	>>> try:
	... 	require_same_values([count_line], hour_line, ndp.ValueAxis.LEFT)
	... except ndp.IncompatibleChartsError as error:
	... 	print(error)
	A LineChart with times of day on the left axis cannot be added to a Plot with numbers on the left axis.
	"""
	added_values = cast(ChartValues, added_layer.values)
	added_family = find_family(added_values.value_type)
	axis_name = AXIS_NAMES[axis]

	for layer in layers:
		if layer.value_axis != axis:
			continue

		values = cast(ChartValues, layer.values)
		plot_family = find_family(values.value_type)
		if plot_family == added_family:
			return

		added_class = type(added_layer.chart)
		added_value_name = VALUE_NAMES[added_family]
		plot_value_name = VALUE_NAMES[plot_family]
		added_name = VALUE_DESCRIPTION.format(value_name=added_value_name, axis_name=axis_name)
		plot_name = VALUE_DESCRIPTION.format(value_name=plot_value_name, axis_name=axis_name)
		raise IncompatibleChartsError(added_class.__name__, added_name, plot_name)


def is_horizontal_bar_chart(chart: Chart) -> bool:
	"""
	Return whether a chart draws horizontal bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart
		Any chart.

	Returns
	-------
	bool
		True for a BarChart of horizontal bars.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.overlay_checks import is_horizontal_bar_chart
	>>> is_horizontal_bar_chart(ndp.BarChart(orientation=ndp.Orientation.HORIZONTAL))
	True
	"""
	if not isinstance(chart, BarChart):
		return False

	is_horizontal = chart.orientation == Orientation.HORIZONTAL

	return is_horizontal
