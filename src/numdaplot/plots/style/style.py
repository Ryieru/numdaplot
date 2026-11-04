"""
Look of a whole Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.style.grid_lines import GridLines
from numdaplot.plots.style.legend_position import LegendPosition
from numdaplot.plots.style.size import Size


@dataclass(frozen=True)
class Style:
	"""
	Look of a whole Plot: title, axis labels, legend, grid lines and size.

	The look of the series, such as their colors, belongs to the chart drawing them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	title
		The title above the axes, none by default.
	x_label
		The label of the axis of the ``x`` values, the name of the ``x`` column by default. An empty text
		draws no label.
	y_label
		The label of the axis of the ``y`` values: by default the name of the ``y`` column when the chart
		draws a single one, no label otherwise, the legend naming the series. An empty text draws no label.
	right_label
		The label of the axis on the right, drawn when a chart is added with ``ValueAxis.RIGHT``: by default
		the name of the column of the first chart on the right when it draws a single one. An empty text draws
		no label.
	legend
		Where the legend is placed, ``LegendPosition.BEST`` by default. It is only drawn for several series.
	grid_lines
		Whether light grid lines are drawn behind the values, ``GridLines.SHOWN`` by default.
	size
		The width and the height, 6.4 by 4.8 inches by default. A Plot placed in a ``Figure`` takes the size of
		its cells instead.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, 10.0])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"])
	>>> style = ndp.Style(title="Sales", x_label="Day", y_label="Euros", legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""

	title: str | None = None
	x_label: str | None = None
	y_label: str | None = None
	right_label: str | None = None
	legend: LegendPosition = LegendPosition.BEST
	grid_lines: GridLines = GridLines.SHOWN
	size: Size = Size()
