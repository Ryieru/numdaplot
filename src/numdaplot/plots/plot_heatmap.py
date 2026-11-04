"""
Heatmaps of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_data import require_column_setting, require_no_column_settings
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

CHART_NAME = "HeatmapChart"
COLUMNS_SETTING = "columns"
LABELS_SETTING = "labels"


def plot_heatmap(data: Table | Array, chart: HeatmapChart, style: Style | None = None) -> Plot:
	"""
	Return a Plot coloring each value of columns of numbers along a color scale.

	For a Table, ``chart.columns`` names the columns drawn and ``chart.labels`` the column labeling the rows.
	For an Array of one or two dimensions, each column is drawn and each row is labeled with its number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn, the row labels, the color scale and the cell values.
	style
		The look of the Plot, the default ``Style`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``columns``, or an Array has ``columns`` or ``labels``.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``labels`` holds booleans or durations, or a drawn column does not hold numbers.
	DimensionError
		When an Array has more than two dimensions.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list(["Mon", "Tue", "Wed", "Thu", "Fri"])
	>>> morning = ndp.Array.from_list([12.0, 15.0, 9.0, 14.0, 20.0])
	>>> noon = ndp.Array.from_list([30.0, 28.0, 25.0, 33.0, 41.0])
	>>> evening = ndp.Array.from_list([18.0, 22.0, None, 19.0, 35.0])
	>>> orders = ndp.Table.from_arrays({"day": days, "morning": morning, "noon": noon, "evening": evening})
	>>> chart = ndp.HeatmapChart(columns=["morning", "noon", "evening"], labels="day", values=ndp.CellValues.SHOWN)
	>>> style = ndp.Style(title="Orders")
	>>> plot = ndp.plot_heatmap(orders, chart, style)
	>>> plot.show()
	"""
	values = read_heatmap_values(data, chart)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot


def read_heatmap_values(data: Table | Array, chart: HeatmapChart) -> ChartValues:
	"""
	Return the row labels and the columns a HeatmapChart draws.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The ``columns`` and the ``labels`` of a Table.

	Returns
	-------
	ChartValues
		The row labels as positions, and one series per column.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``columns``, or an Array has ``columns`` or ``labels``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.plot_heatmap import read_heatmap_values
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> try:
	... 	read_heatmap_values(grid, ndp.HeatmapChart(labels="city"))
	... except ndp.InvalidChartDataError as error:
	... 	print(error)
	HeatmapChart takes no labels for an Array.
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object]({COLUMNS_SETTING: chart.columns, LABELS_SETTING: chart.labels})
		require_no_column_settings(CHART_NAME, column_settings)
		array_values = read_array_values(data, CHART_NAME)
		return array_values

	column_names = require_column_setting(CHART_NAME, COLUMNS_SETTING, chart.columns)
	table_values = read_table_values(data, chart.labels, column_names, CHART_NAME)

	return table_values
