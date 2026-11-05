"""
Line plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.charts.chart_requirement import require_chart_class
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.layer_reading import read_line_layer
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

FUNCTION_NAME = "plot_line"


def plot_line(data: Table | Array, chart: LineChart | None = None, style: Style | None = None) -> Plot:
	"""
	Return a Plot drawing columns of numbers as lines.

	For a Table, ``LineChart.y`` names the columns drawn and ``LineChart.x`` the column of the positions. For an Array
	of one or two dimensions, each column is a line and each row is placed at its number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the lines.
		The default ``LineChart`` when omitted, which draws an Array: a Table needs the columns named.
	style
		The look of the Plot, the default ``Style`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``x`` holds booleans or durations, or a drawn column does not hold numbers.
	DimensionError
		When an Array has more than two dimensions.
	InvalidColorCountError
		When the colors of the chart are not one per line.
	RefusedOperationError
		When ``chart`` is not a ``LineChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([1, 2, 3, 4, 5])
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 16.0])
	>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, None, 10.5])
	>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
	>>> chart = ndp.LineChart(x="day", y=["price", "cost"], marker=ndp.MarkerShape.CIRCLE)
	>>> style = ndp.Style(title="Sales", y_label="Euros")
	>>> plot = ndp.plot_line(sales, chart, style)
	>>> plot.show()
	"""
	if chart is None:
		chart = LineChart()

	require_chart_class(chart, LineChart, FUNCTION_NAME)
	layer = read_line_layer(data, chart)
	plot = create_plot(layer, style)

	return plot
