"""
Creation of a Plot giving an overview of the values of a Table or an Array.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.data.heatmap_values import read_heatmap_values
from numdaplot.plots.data.missing_cells import read_missing_cells, read_missing_counts
from numdaplot.plots.plot_data import PlotData
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.table import Table


class PlotOverviewCreation(PlotData):
	"""
	Creation of a Plot giving an overview of the values of a Table or an Array.

	Use ``ndp.Plot.heatmap``, ``ndp.Plot.missing_by_column`` and ``ndp.Plot.missing_map``.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	@checked_arguments
	def heatmap(cls, data: Table | Array, chart: HeatmapChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot coloring each value of columns of numbers along a color scale.

		For a Table, ``HeatmapChart.columns`` names the columns drawn and ``HeatmapChart.labels`` the column labeling
		the rows.
		For an Array of one or two dimensions, each column is drawn and each row is labeled with its number.
		When there are more rows or columns than the image can show, each band shows the mean of its cells, without
		their values written, with a ``ReadabilityWarning``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn, the row labels, the color scale and the cell values.
			The default ``HeatmapChart`` when omitted, which draws an Array: a Table needs the columns named.
		style
			The look of the Plot, the default ``PlotStyle`` when omitted.

		Returns
		-------
		Self
			The Plot, which ``show`` displays and ``save`` writes as an image.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		InvalidChartDataError
			When a Table has no ``columns``, or an Array has ``columns`` or ``labels``.
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When ``labels`` holds booleans or durations, or a drawn column does not hold numbers.
		DimensionError
			When an Array has more than two dimensions.

		Warns
		-----
		ReadabilityWarning
			When the cells are merged into bands.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> days = ndp.Array.from_list(["Mon", "Tue", "Wed", "Thu", "Fri"])
		>>> morning = ndp.Array.from_list([12.0, 15.0, 9.0, 14.0, 20.0])
		>>> noon = ndp.Array.from_list([30.0, 28.0, 25.0, 33.0, 41.0])
		>>> evening = ndp.Array.from_list([18.0, 22.0, None, 19.0, 35.0])
		>>> orders = ndp.Table.from_arrays({"day": days, "morning": morning, "noon": noon, "evening": evening})
		>>> chart = ndp.HeatmapChart(columns=["morning", "noon", "evening"], labels="day", values=ndp.CellValues.SHOWN)
		>>> style = ndp.PlotStyle(title="Orders")
		>>> plot = ndp.Plot.heatmap(orders, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = HeatmapChart()

		values = read_heatmap_values(data, chart)
		layer = ChartLayer(chart, values)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def missing_by_column(cls, table: Table, chart: MissingChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot drawing one bar per column of a Table, as high as its missing values.

		Above each bar are its number of missing values and their share of the rows, written on one line going upwards
		when the bars are too narrow, and left out when they are too narrow for that.

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
		Self
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
		>>> plot = ndp.Plot.missing_by_column(flats, style=style)
		>>> plot.show()
		"""
		if chart is None:
			chart = MissingChart()

		values = read_missing_counts(table, chart.measure)
		layer = ChartLayer(chart, values)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def missing_map(cls, table: Table, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot drawing each value of a Table as a cell, light gray when present and dark when missing.

		The columns are side by side and the rows go down from the first one, which shows whether the missing
		values gather in some rows or columns. When there are more rows or columns than the image can show, each mark
		stands for at least one missing value among the cells it covers, so no missing value is lost. The legend gives
		the total of missing values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		table
			The Table whose missing values are drawn.
		style
			The look of the Plot, the default ``PlotStyle`` when omitted.

		Returns
		-------
		Self
			The Plot, which ``show`` displays and ``save`` writes as an image.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Nice", "Pau", "Lyon", "Nice", "Paris", "Pau"])
		>>> prices = ndp.Array.from_list([12.0, None, None, 15.5, None, 18.0, 11.0, 14.0])
		>>> surfaces = ndp.Array.from_list([30.0, 45.0, None, 60.0, 52.0, 41.0, None, 38.0])
		>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices, "surface": surfaces})
		>>> style = ndp.PlotStyle(legend=ndp.LegendPosition.OUTSIDE_RIGHT)
		>>> plot = ndp.Plot.missing_map(flats, style)
		>>> plot.show()
		"""
		values = read_missing_cells(table)
		layer = ChartLayer(MissingMapChart(), values)
		plot = cls._create_from_layer(layer, style)

		return plot
