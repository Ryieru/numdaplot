"""
Map of the missing values of a Table.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.data.chart_data import require_table
from numdaplot.plots.data.missing_cells import read_missing_cells
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.tables.table import Table

FUNCTION_NAME = "plot_missing_map"


def plot_missing_map(table: Table, style: PlotStyle | None = None) -> Plot:
	"""
	Return a Plot drawing each value of a Table as a cell, light gray when present and dark when missing.

	The columns are side by side and the rows go down from the first one, which shows whether the missing
	values gather in some rows or columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table whose missing values are drawn.
	style
		The look of the Plot, the default ``PlotStyle`` when omitted.

	Returns
	-------
	Plot
		The Plot, which ``show`` displays and ``save`` writes as an image.

	Raises
	------
	UnsupportedDataError
		When the data is an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Nice", "Pau", "Lyon", "Nice", "Paris", "Pau"])
	>>> prices = ndp.Array.from_list([12.0, None, None, 15.5, None, 18.0, 11.0, 14.0])
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, None, 60.0, 52.0, 41.0, None, 38.0])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices, "surface": surfaces})
	>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.OUTSIDE_RIGHT)
	>>> plot = ndp.plot_missing_map(flats, style)
	>>> plot.show()
	"""
	checked_table = require_table(table, FUNCTION_NAME)
	values = read_missing_cells(checked_table)
	layer = ChartLayer(MissingMapChart(), values)
	plot = create_plot(layer, style)

	return plot
