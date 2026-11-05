"""
Bars of the missing values of each column of a Table.

.. versionadded:: 0.1.0
"""

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.data.missing_cells import read_missing_counts
from numdaplot.plots.plot import Plot
from numdaplot.plots.plot_creation import create_plot
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.table import Table


@checked_arguments
def plot_missing_by_column(table: Table, chart: MissingChart | None = None, style: PlotStyle | None = None) -> Plot:
	"""
	Return a Plot drawing one bar per column of a Table, as high as its missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table whose missing values are counted.
	chart
		The measure, the number of missing values of each column when omitted.
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

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Nice", "Pau", "Lyon"])
	>>> prices = ndp.Array.from_list([12.0, None, None, 15.5, None])
	>>> surfaces = ndp.Array.from_list([30.0, 45.0, None, 60.0, 52.0])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices, "surface": surfaces})
	>>> style = ndp.PlotStyle(title="Missing values")
	>>> plot = ndp.plot_missing_by_column(flats, style=style)
	>>> plot.show()
	"""
	if chart is None:
		chart = MissingChart()

	values = read_missing_counts(table, chart.measure)
	layer = ChartLayer(chart, values)
	plot = create_plot(layer, style)

	return plot
