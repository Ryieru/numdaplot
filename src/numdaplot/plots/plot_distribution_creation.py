"""
Creation of a Plot showing how values are spread or shared out.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.data.pie_values import read_pie_values
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.histogram_drawing import require_bins_on_values
from numdaplot.plots.drawing.series_colors import require_color_count
from numdaplot.plots.plot_data import PlotData
from numdaplot.plots.style.axis_settings import require_no_axis_settings
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.tables.table import Table

HISTOGRAM_CHART_NAME = "HistogramChart"
BOX_CHART_NAME = "BoxChart"


class PlotDistributionCreation(PlotData):
	"""
	Creation of a Plot showing how values are spread or shared out.

	Use ``ndp.Plot.histogram``, ``ndp.Plot.box`` and ``ndp.Plot.pie``.

	.. versionadded:: 0.1.0
	"""

	@classmethod
	@checked_arguments
	def histogram(
		cls, data: Table | Array, chart: HistogramChart | None = None, style: PlotStyle | None = None
	) -> Self:
		"""
		Return a Plot drawing how many values of columns of numbers or times of day fall in each bin.

		For a Table, ``HistogramChart.columns`` names the columns drawn. For an Array of one or two dimensions, each
		column is drawn. Several columns share the same bins.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn, the bins, the measure and the colors.
			The default ``HistogramChart`` when omitted, which draws an Array: a Table needs the columns named.
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
			When a Table has no ``columns``, or an Array has ``columns``.
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When a drawn column holds neither numbers nor times of day, the columns mix them, or the width of the bins
			is a number for times of day or a duration for numbers.
		DimensionError
			When an Array has more than two dimensions.
		InvalidColorCountError
			When the colors of the chart are not one per column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0, 13.5, 16.0, 14.5, 15.0, 18.5, 11.0])
		>>> flats = ndp.Table.from_arrays({"price": prices})
		>>> chart = ndp.HistogramChart(columns=["price"], bins=ndp.BinWidth(2.0), measure=ndp.Measure.RATIO)
		>>> style = ndp.PlotStyle(title="Prices", x_label="Price (euros)")
		>>> plot = ndp.Plot.histogram(flats, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = HistogramChart()

		values = read_sample_values(data, chart.columns, None, HISTOGRAM_CHART_NAME)
		require_bins_on_values(chart.bins, values.value_type)
		series_count = len(values.series)
		require_color_count(chart.colors, series_count)
		layer = ChartLayer(chart, values)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def box(cls, data: Table | Array, chart: BoxChart | None = None, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot summing up the spread of columns of numbers or times of day as boxes.

		For a Table, ``BoxChart.columns`` names the columns drawn, and ``BoxChart.group_by`` may split their rows into
		groups. For an Array of one or two dimensions, each column is a box.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array drawn.
		chart
			The columns drawn, their groups, the outliers and the colors.
			The default ``BoxChart`` when omitted, which draws an Array: a Table needs the columns named.
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
			When a Table has no ``columns``, or an Array has ``columns`` or ``group_by``.
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When a drawn column holds neither numbers nor times of day, the columns mix them, or ``group_by`` holds
			neither texts, booleans nor times of day.
		DimensionError
			When an Array has more than two dimensions.
		InvalidColorCountError
			When the colors of the chart are not one per column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau", "Paris", "Lyon", "Pau", "Paris", "Lyon", "Pau"])
		>>> prices = ndp.Array.from_list([14.0, 9.5, 7.0, 16.5, 10.0, 8.5, 15.0, 11.5, 6.0])
		>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices})
		>>> chart = ndp.BoxChart(columns=["price"], group_by="city")
		>>> style = ndp.PlotStyle(y_label="Price per night (euros)")
		>>> plot = ndp.Plot.box(flats, chart, style)
		>>> plot.show()
		"""
		if chart is None:
			chart = BoxChart()

		values = read_sample_values(data, chart.columns, chart.group_by, BOX_CHART_NAME)
		series_count = len(values.series)
		require_color_count(chart.colors, series_count)
		layer = ChartLayer(chart, values)
		plot = cls._create_from_layer(layer, style)

		return plot

	@classmethod
	@checked_arguments
	def pie(cls, table: Table, chart: PieChart, style: PlotStyle | None = None) -> Self:
		"""
		Return a Plot sharing out the values of a column of a Table as slices of a disc.

		``PieChart.labels`` names the column of texts labeling the slices and ``PieChart.values`` the column of numbers
		sizing them. A Plot of a pie has no axes, so its style takes no axis label.

		.. versionadded:: 0.1.0

		Parameters
		----------
		table
			The Table drawn.
		chart
			The labels, the values, the percentages and the colors.
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
		ColumnNotFoundError
			When a column does not exist.
		IncompatibleTypesError
			When ``labels`` does not hold texts, or ``values`` does not hold numbers.
		MissingValueError
			When a label or a value is missing.
		OutOfDomainError
			When a value is negative.
		EmptyTotalError
			When the values add up to 0.
		DuplicateLabelError
			When two slices have the same label.
		InvalidColorCountError
			When the colors of the chart are not one per slice.
		RefusedSettingError
			When the style has an axis setting: ``x_label``, ``y_label``, ``right_label``, ``x_tick_rotation`` or
			``y_tick_rotation``.

		Warns
		-----
		ReadabilityWarning
			When there are more than 5 slices.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> devices = ndp.Array.from_list(["Phone", "Computer", "Tablet"])
		>>> visits = ndp.Array.from_list([5400.0, 3100.0, 900.0])
		>>> traffic = ndp.Table.from_arrays({"device": devices, "visits": visits})
		>>> chart = ndp.PieChart(labels="device", values="visits")
		>>> style = ndp.PlotStyle(title="Visits per device")
		>>> plot = ndp.Plot.pie(traffic, chart, style)
		>>> plot.show()
		"""
		values = read_pie_values(table, chart)
		slice_count = len(values.rows)
		require_color_count(chart.colors, slice_count)
		require_no_axis_settings(style)
		layer = ChartLayer(chart, values)
		plot = cls._create_from_layer(layer, style)

		return plot
