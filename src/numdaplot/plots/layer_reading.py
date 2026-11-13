"""
Reading of the charts a Plot draws on its axes: lines, bars and points.

``Plot.line``, ``Plot.bar`` and ``Plot.scatter`` read their first chart with these functions, and
``Plot.add_line``, ``Plot.add_bar`` and ``Plot.add_scatter`` the charts they add.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_data import read_chart_values, require_column_setting, require_no_column_settings
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.point_values import hide_missing_points, read_point_values, require_scale_on_numbers
from numdaplot.plots.data.sample_values import SampleValues
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.colors.series_colors import require_color_count
from numdaplot.tables.table import Table

LINE_NAME = "LineChart"
BAR_NAME = "BarChart"
SCATTER_NAME = "ScatterChart"
X_SETTING = "x"
Y_SETTING = "y"
COLOR_BY_SETTING = "color_by"
SIZE_BY_SETTING = "size_by"


type SeriesChart = LineChart | BarChart | HistogramChart | BoxChart


def build_series_layer(chart: SeriesChart, values: ChartValues | SampleValues) -> ChartLayer:
	"""
	Return a chart drawing one series per column with its values, once its colors are checked against its series.

	.. versionadded:: 0.2.0

	Parameters
	----------
	chart
		A ``LineChart``, ``BarChart``, ``HistogramChart`` or ``BoxChart``.
	values
		The series the chart draws.

	Returns
	-------
	ChartLayer
		The chart and its values.

	Raises
	------
	InvalidColorCountError
		When the colors of the chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.layer_reading import build_series_layer
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = build_series_layer(ndp.BarChart(), read_array_values(prices, "BarChart"))
	>>> len(layer.values.series)
	1
	"""
	series_count = len(values.series)
	require_color_count(chart.colors, series_count)
	layer = ChartLayer(chart, values)

	return layer


def read_line_layer(data: Table | Array, chart: LineChart) -> ChartLayer:
	"""
	Return a LineChart with the values it draws from a Table or an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the lines.

	Returns
	-------
	ChartLayer
		The chart and its values.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
	InvalidColorCountError
		When the colors of the chart are not one per line.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layer_reading import read_line_layer
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> len(read_line_layer(grid, ndp.LineChart()).values.series)
	2
	"""
	values = read_chart_values(data, chart.x, chart.y, LINE_NAME)
	layer = build_series_layer(chart, values)

	return layer


def read_bar_layer(data: Table | Array, chart: BarChart) -> ChartLayer:
	"""
	Return a BarChart with the values it draws from a Table or an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the bars.

	Returns
	-------
	ChartLayer
		The chart and its values.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
	InvalidColorCountError
		When the colors of the chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layer_reading import read_bar_layer
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> read_bar_layer(prices, ndp.BarChart()).values.series[0].values
	array([12. , 15.5])
	"""
	values = read_chart_values(data, chart.x, chart.y, BAR_NAME)
	layer = build_series_layer(chart, values)

	return layer


def read_scatter_layer(data: Table | Array, chart: ScatterChart) -> ChartLayer:
	"""
	Return a ScatterChart with the values it draws from a Table or an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the points.

	Returns
	-------
	ChartLayer
		The chart, its values, and for a Table the values coloring and sizing its points.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` column, or an Array has a column setting.
	InvalidColorCountError
		When ``color`` is given for an Array of several columns.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.layer_reading import read_scatter_layer
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> len(read_scatter_layer(grid, ndp.ScatterChart()).values.series)
	2
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object](
			{X_SETTING: chart.x, Y_SETTING: chart.y, COLOR_BY_SETTING: chart.color_by, SIZE_BY_SETTING: chart.size_by}
		)
		require_no_column_settings(SCATTER_NAME, column_settings)
		array_values = read_array_values(data, SCATTER_NAME)
		series_count = len(array_values.series)
		if chart.color is not None:
			require_color_count([chart.color], series_count)

		array_layer = ChartLayer(chart, array_values)
		return array_layer

	y_name = require_column_setting(SCATTER_NAME, Y_SETTING, chart.y)
	table_values = read_table_values(data, chart.x, [y_name], SCATTER_NAME)
	point_values = read_point_values(data, chart.color_by, chart.size_by, table_values.rows)
	require_scale_on_numbers(chart.scale, point_values.colors)
	shown_values = hide_missing_points(table_values, point_values)
	table_layer = ChartLayer(chart, shown_values, point_values)

	return table_layer
