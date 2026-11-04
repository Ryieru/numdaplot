"""
Scatter plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_data import require_column_setting, require_no_column_settings
from numdaplot.plots.data.point_values import hide_missing_points, read_point_values
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot import Plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table

CHART_NAME = "ScatterChart"
X_SETTING = "x"
Y_SETTING = "y"
COLOR_BY_SETTING = "color_by"
SIZE_BY_SETTING = "size_by"


def plot_scatter(data: Table | Array, chart: ScatterChart, style: Style | None = None) -> Plot:
	"""
	Return a Plot drawing each row as a point.

	For a Table, ``chart.y`` names the column of the vertical positions and ``chart.x`` the column of the
	horizontal ones, and the points can be colored and sized by other columns. For an Array of one or two
	dimensions, each column is a series of points and each row is placed at its number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	chart
		The columns drawn and the look of the points.
	style
		The look of the Plot, the default ``Style`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` column, or an Array has a column setting.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``x`` holds booleans or durations, ``y`` or ``size_by`` does not hold numbers, or ``color_by``
		holds neither numbers nor texts.
	DimensionError
		When an Array has more than two dimensions.
	InvalidColorCountError
		When ``color`` is given for an Array of several columns.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, 60.0, 80.0, 52.0, 38.0])
	>>> prices = ndp.Array.from_list([150.0, 210.0, 260.0, 330.0, 190.0, 160.0])
	>>> rooms = ndp.Array.from_list([1, 2, 3, 4, 3, 2])
	>>> flats = ndp.Table.from_arrays({"surface": surfaces, "price": prices, "rooms": rooms})
	>>> chart = ndp.ScatterChart(x="surface", y="price", color_by="rooms")
	>>> style = ndp.Style(x_label="Surface (m2)", y_label="Price (thousands of euros)")
	>>> plot = ndp.plot_scatter(flats, chart, style)
	>>> plot.show()
	"""
	layer = read_scatter_layer(data, chart)
	chosen_style = style
	if chosen_style is None:
		chosen_style = Style()

	plot = Plot([layer], chosen_style)

	return plot


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
	>>> from numdaplot.plots.plot_scatter import read_scatter_layer
	>>> grid = ndp.Array.from_list([[1.0, 2.0], [3.0, 4.0]])
	>>> len(read_scatter_layer(grid, ndp.ScatterChart()).values.series)
	2
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object](
			{X_SETTING: chart.x, Y_SETTING: chart.y, COLOR_BY_SETTING: chart.color_by, SIZE_BY_SETTING: chart.size_by}
		)
		require_no_column_settings(CHART_NAME, column_settings)
		array_values = read_array_values(data, CHART_NAME)
		series_count = len(array_values.series)
		if chart.color is not None:
			require_color_count([chart.color], series_count)

		array_layer = ChartLayer(chart, array_values)
		return array_layer

	y_name = require_column_setting(CHART_NAME, Y_SETTING, chart.y)
	table_values = read_table_values(data, chart.x, [y_name], CHART_NAME)
	point_values = read_point_values(data, chart.color_by, chart.size_by, table_values.rows)
	shown_values = hide_missing_points(table_values, point_values)
	table_layer = ChartLayer(chart, shown_values, point_values)

	return table_layer
