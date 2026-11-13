"""
Creation of a Plot of lines, bars or points, the charts ``add_*`` can also draw over a Plot.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array import Array
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.layer_reading import read_bar_layer, read_line_layer, read_scatter_layer
from numdaplot.plots.plot_data import PlotData
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.tables.table import Table


class PlotSeriesCreation(PlotData):
	"""
	Creation of a Plot of lines, bars or points.

	Use ``ndp.Plot.line``, ``ndp.Plot.bar`` and ``ndp.Plot.scatter``.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	@checked_arguments
	def line(cls, data: Table | Array, chart: LineChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot drawing columns of numbers or times of day as lines.

		For a Table, ``LineChart.y`` names the columns drawn and ``LineChart.x`` the column of the positions. For an
		Array of one or two dimensions, each column is a line and each row is placed at its number.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn and the look of the lines.
			The default ``LineChart`` when omitted, which draws an Array: a Table needs the columns named.
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
			When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When ``x`` holds booleans or durations, or a drawn column holds neither numbers nor times of day, or the
			drawn columns mix them.
		DimensionError
			When an Array has more than two dimensions.
		InvalidColorCountError
			When the colors of the chart are not one per line.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> days = ndp.Array.from_list([1, 2, 3, 4, 5])
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 16.0])
		>>> costs = ndp.Array.from_list([8.0, 9.5, 9.0, None, 10.5])
		>>> sales = ndp.Table.from_arrays({"day": days, "price": prices, "cost": costs})
		>>> chart = ndp.LineChart(x="day", y=["price", "cost"], marker=ndp.MarkerShape.CIRCLE)
		>>> style = ndp.PlotStyle(title="Sales", y_label="Euros")
		>>> plot = ndp.Plot.line(sales, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = LineChart()

		layer = read_line_layer(data, chart)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def bar(cls, data: Table | Array, chart: BarChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot drawing columns of numbers as bars.

		For a Table, ``BarChart.y`` names the columns drawn and ``BarChart.x`` the column labeling the bars. For an
		Array of one or two dimensions, each column is a series of bars and each row is labeled with its number.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn and the look of the bars.
			The default ``BarChart`` when omitted, which draws an Array: a Table needs the columns named.
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
		>>> style = ndp.PlotStyle(title="Sales per city", y_label="Thousands of euros")
		>>> plot = ndp.Plot.bar(sales, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = BarChart()

		layer = read_bar_layer(data, chart)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def scatter(cls, data: Table | Array, chart: ScatterChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot drawing each row as a point.

		For a Table, ``ScatterChart.y`` names the column of the vertical positions and ``ScatterChart.x`` the column of
		the horizontal ones, and the points can be colored and sized by other columns. For an Array of one or two
		dimensions, each column is a series of points and each row is placed at its number.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn and the look of the points.
			The default ``ScatterChart`` when omitted, which draws an Array: a Table needs the columns named.
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
			When a Table has no ``y`` column, or an Array has a column setting.
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When ``x`` holds booleans or durations, ``y`` holds neither numbers nor times of day, ``size_by`` does
			not hold numbers, or ``color_by`` holds neither numbers, texts, booleans nor times of day.
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
		>>> style = ndp.PlotStyle(x_label="Surface (m2)", y_label="Price (thousands of euros)")
		>>> plot = ndp.Plot.scatter(flats, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = ScatterChart()

		layer = read_scatter_layer(data, chart)
		plot = cls._create_from_layer(layer, style)

		return plot
