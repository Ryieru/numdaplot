"""
Bar plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.chart_requirement import require_chart_class
from numdaplot.plots.layer_reading import read_bar_layer
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

FUNCTION_NAME = "plot_bar"


def plot_bar(data: Table | Array, chart: BarChart | None = None, style: Style | None = None) -> Plot:
	"""
	Return a Plot drawing columns of numbers as bars.

	For a Table, ``BarChart.y`` names the columns drawn and ``BarChart.x`` the column labeling the bars. For an Array
	of one or two dimensions, each column is a series of bars and each row is labeled with its number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the bars.
		The default ``BarChart`` when omitted, which draws an Array: a Table needs the columns named.
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
	RefusedOperationError
		When ``chart`` is not a ``BarChart``.

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
	if chart is None:
		chart = BarChart()

	require_chart_class(chart, BarChart, FUNCTION_NAME)
	layer = read_bar_layer(data, chart)
	plot = create_plot(layer, style)

	return plot
