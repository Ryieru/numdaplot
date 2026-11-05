"""
Histograms of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.table import Table

CHART_NAME = "HistogramChart"
FUNCTION_NAME = "plot_histogram"


@checked_arguments
def plot_histogram(data: Table | Array, chart: HistogramChart | None = None, style: PlotStyle | None = None) -> Plot:
	"""
	Return a Plot drawing how many values of columns of numbers fall in each bin.

	For a Table, ``HistogramChart.columns`` names the columns drawn. For an Array of one or two dimensions, each column
	is drawn. Several columns share the same bins.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn, the bins, the measure and the colors.
		The default ``HistogramChart`` when omitted, which draws an Array: a Table needs the columns named.
	style
		The look of the Plot, the default ``PlotStyle`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	InvalidTypeError
		When an argument is not of the type its annotation names.
	InvalidChartDataError
		When a Table has no ``columns``, or an Array has ``columns``.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When a drawn column does not hold numbers.
	DimensionError
		When an Array has more than two dimensions.
	InvalidColorCountError
		When the colors of the chart are not one per column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 15.0, 18.5, 11.0])
	>>> flats = ndp.Table.from_arrays({"price": prices})
	>>> chart = ndp.HistogramChart(columns=["price"], bins=ndp.BinWidth(2.0), measure=ndp.Measure.RATIO)
	>>> style = ndp.PlotStyle(title="Prices", x_label="Price (euros)")
	>>> plot = ndp.plot_histogram(flats, chart, style)
	>>> plot.show()
	"""
	if chart is None:
		chart = HistogramChart()

	values = read_sample_values(data, chart.columns, None, CHART_NAME)
	series_count = len(values.series)
	require_color_count(chart.colors, series_count)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot
