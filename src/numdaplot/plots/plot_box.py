"""
Box plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.chart_requirement import require_chart_class
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.tables.table import Table

CHART_NAME = "BoxChart"
FUNCTION_NAME = "plot_box"


def plot_box(data: Table | Array, chart: BoxChart | None = None, style: PlotStyle | None = None) -> Plot:
	"""
	Return a Plot summing up the spread of columns of numbers as boxes.

	For a Table, ``BoxChart.columns`` names the columns drawn, and ``BoxChart.group_by`` may split their rows into
	groups. For an Array of one or two dimensions, each column is a box.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn, their groups, the outliers and the colors.
		The default ``BoxChart`` when omitted, which draws an Array: a Table needs the columns named.
	style
		The look of the Plot, the default ``PlotStyle`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``columns``, or an Array has ``columns`` or ``group_by``.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When a drawn column does not hold numbers, or ``group_by`` does not hold texts.
	DimensionError
		When an Array has more than two dimensions.
	InvalidColorCountError
		When the colors of the chart are not one per column.
	RefusedOperationError
		When ``chart`` is not a ``BoxChart``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau", "Paris", "Lyon", "Pau", "Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([14.0, 9.5, 7.0, 16.5, 10.0, 8.5, 15.0, 11.5, 6.0])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> chart = ndp.BoxChart(columns=["price"], group_by="city")
	>>> style = ndp.PlotStyle(y_label="Price per night (euros)")
	>>> plot = ndp.plot_box(flats, chart, style)
	>>> plot.show()
	"""
	if chart is None:
		chart = BoxChart()

	require_chart_class(chart, BoxChart, FUNCTION_NAME)
	values = read_sample_values(data, chart.columns, chart.group_by, CHART_NAME)
	series_count = len(values.series)
	require_color_count(chart.colors, series_count)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot
