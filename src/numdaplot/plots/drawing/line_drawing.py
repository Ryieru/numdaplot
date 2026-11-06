"""
Drawing of a LineChart.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import cast

from matplotlib.axes import Axes

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.line_type import LineType
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.drawing.default_labels import find_position_label
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.grid_axes import GridAxes
from numdaplot.plots.drawing.marker_codes import MARKER_CODES
from numdaplot.plots.drawing.position_axis import place_positions
from numdaplot.plots.drawing.series_colors import choose_series_colors

LINE_STYLES = {
	LineType.SOLID: "-",
	LineType.DASHED: "--",
	LineType.DOTTED: ":",
	LineType.DASH_DOT: "-.",
}


def draw_line_chart(axes: Axes, layer: ChartLayer) -> DrawnChart:
	"""
	Draw each series of a LineChart as a line.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes drawn on.
	layer
		A LineChart and its values.

	Returns
	-------
	DrawnChart
		The default labels, the ``x`` values on the horizontal axis, and grid lines across both axes.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.line_drawing import draw_line_chart
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> axes = Figure().add_subplot()
	>>> drawn_chart = draw_line_chart(axes, ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart")))
	>>> axes.lines[0].get_ydata()
	array([12. , 15.5])
	"""
	chart = cast(LineChart, layer.chart)
	values = cast(ChartValues, layer.values)
	series_count = len(values.series)
	color_codes = choose_series_colors(chart.colors, series_count)
	coordinates = place_positions(axes, values.positions, False)
	line_style = LINE_STYLES[chart.line]
	marker_code = MARKER_CODES[chart.marker]

	for series, color_code in zip(values.series, color_codes, strict=True):
		axes.plot(
			coordinates, series.values, color=color_code, linestyle=line_style, marker=marker_code, label=series.name
		)

	x_label = find_position_label(values.positions)
	drawn_chart = DrawnChart(x_label, values.value_name, False, GridAxes.BOTH, None)

	return drawn_chart
