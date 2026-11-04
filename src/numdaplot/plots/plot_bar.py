"""
Bar plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.data.chart_data import read_chart_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

CHART_NAME = "BarChart"


def plot_bar(data: Table | Array, chart: BarChart, style: Style | None = None) -> Plot:
	"""
	Return a Plot drawing columns of numbers as bars.

	For a Table, ``chart.y`` names the columns drawn and ``chart.x`` the column labeling the bars. For an Array
	of one or two dimensions, each column is a series of bars and each row is labeled with its number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the bars.
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
		When the colors of the chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau", "Nice"])
	>>> sales_2025 = ndp.Array.from_list([120.0, 80.0, 45.0, 60.0])
	>>> sales_2026 = ndp.Array.from_list([150.0, 95.0, 40.0, 70.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "2025": sales_2025, "2026": sales_2026})
	>>> chart = ndp.BarChart(x="city", y=["2025", "2026"], layout=ndp.BarLayout.STACKED)
	>>> style = ndp.Style(title="Sales per city", y_label="Thousands of euros")
	>>> plot = ndp.plot_bar(sales, chart, style)
	>>> plot.show()
	"""
	values = read_chart_values(data, chart.x, chart.y, CHART_NAME)
	series_count = len(values.series)
	require_color_count(chart.colors, series_count)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot
