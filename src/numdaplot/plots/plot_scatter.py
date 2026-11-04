"""
Scatter plots of a Table or an Array.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.layer_reading import read_scatter_layer
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.style import Style
from numdaplot.tables.table import Table


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
	plot = create_plot(layer, style)

	return plot
