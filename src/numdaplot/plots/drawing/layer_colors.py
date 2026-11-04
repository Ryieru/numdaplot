"""
Colors of the charts overlaid on a Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import replace
from typing import cast

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.drawing.series_colors import take_cycle_colors

SINGLE_SERIES = 1


def continue_color_cycle(layers: list[ChartLayer]) -> list[ChartLayer]:
	"""
	Return the charts of a Plot with the default colors following each other from one chart to the next.

	A chart without chosen colors takes the colors of the default cycle after the ones of the charts before it,
	so blue bars are followed by an orange line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.

	Returns
	-------
	list[ChartLayer]
		The same charts, the ones after the first given the colors of the cycle they take.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.layer_colors import continue_color_cycle
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> bars = ChartLayer(ndp.BarChart(), read_array_values(prices, "BarChart"))
	>>> line = ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))
	>>> continue_color_cycle([bars, line])[1].chart.colors
	[<Color.ORANGE: 2>]
	"""
	colored_layers = list[ChartLayer]()
	used_count = 0

	for layer in layers:
		values = cast(ChartValues, layer.values)
		series_count = len(values.series)
		colored_layer = give_cycle_colors(layer, used_count, series_count)
		colored_layers.append(colored_layer)
		used_count += series_count

	return colored_layers


def give_cycle_colors(layer: ChartLayer, start: int, series_count: int) -> ChartLayer:
	"""
	Return a chart given the colors of the default cycle from a start, when it has no chosen colors.

	A ScatterChart takes a color for a single series without ``color_by`` only.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layer
		A chart and its values.
	start
		The number of colors of the cycle used by the charts before it.
	series_count
		The number of series of the chart.

	Returns
	-------
	ChartLayer
		The chart with its colors, or the same chart when it keeps its own colors or comes first.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.layer_colors import give_cycle_colors
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> points = ChartLayer(ndp.ScatterChart(), read_array_values(prices, "ScatterChart"))
	>>> give_cycle_colors(points, 2, 1).chart.color
	<Color.GREEN: 3>
	"""
	if start == 0:
		return layer

	chart = layer.chart
	cycle_colors = take_cycle_colors(start, series_count)
	if isinstance(chart, LineChart | BarChart):
		if chart.colors is not None:
			return layer

		colored_chart = replace(chart, colors=cycle_colors)
		colored_layer = replace(layer, chart=colored_chart)
		return colored_layer

	if not isinstance(chart, ScatterChart):
		return layer

	is_single_series = series_count == SINGLE_SERIES
	has_no_color = chart.color is None
	has_no_color_by = chart.color_by is None
	takes_cycle_color = is_single_series and has_no_color and has_no_color_by
	if not takes_cycle_color:
		return layer

	scatter_chart = replace(chart, color=cycle_colors[0])
	scatter_layer = replace(layer, chart=scatter_chart)

	return scatter_layer
