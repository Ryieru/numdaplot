"""
Charts drawn over the charts of a Plot.

.. versionadded:: 0.1.0
"""

from dataclasses import replace
from typing import Self

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array import Array
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.drawing.layer_alignment import align_layers
from numdaplot.plots.layer_reading import read_bar_layer, read_line_layer, read_scatter_layer
from numdaplot.plots.overlay_checks import (
	require_overlay_base,
	require_same_positions,
	require_same_values,
	require_vertical_bars,
)
from numdaplot.plots.plot_data import PlotData
from numdaplot.tables.table import Table

ADD_LINE_NAME = "add_line"
ADD_BAR_NAME = "add_bar"
ADD_SCATTER_NAME = "add_scatter"


class PlotOverlays(PlotData):
	"""
	Charts drawn over the charts of a Plot.

	Use ``ndp.Plot``; this group only adds the ``add_*`` methods.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def add_line(self, data: Table | Array, chart: LineChart | None = None, axis: ValueAxis = ValueAxis.LEFT) -> Self:
		"""
		Return a new Plot with lines added over the charts of this one.

		The lines take the colors of the default cycle after the ones already used. Over bars or texts, their
		``x`` values are placed on the labels of the Plot, new labels following the others.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array of the lines, which may differ from the one of the Plot.
		chart
			The columns drawn and the look of the lines.
			The default ``LineChart`` when omitted, which draws an Array: a Table needs the columns named.
		axis
			``ValueAxis.LEFT`` by default to share the scale of the Plot, ``ValueAxis.RIGHT`` for a scale of
			their own on the right.

		Returns
		-------
		Self
			A new Plot; this one is left unchanged.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		RefusedSettingError
			When the Plot does not draw lines, vertical bars or points.
		IncompatibleChartsError
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates, texts or times of day;
			or when one measures numbers and the other times of day on the same axis.
		DuplicateLabelError
			When a label appears twice in the ``x`` values of one chart placed on labels.
		InvalidChartDataError
			When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
		InvalidColorCountError
			When the colors of the chart are not one per line.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
		>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
		>>> targets = ndp.Array.from_list([130.0, 130.0, 140.0, 140.0])
		>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "target": targets})
		>>> plot = ndp.Plot.bar(shop, ndp.BarChart(x="month", y=["sales"]))
		>>> line = ndp.LineChart(x="month", y=["target"], marker=ndp.MarkerShape.CIRCLE)
		>>> both = plot.add_line(shop, line)
		>>> both.show()
		"""
		if chart is None:
			chart = LineChart()

		layer = read_line_layer(data, chart)
		added_plot = self._add_layer(layer, axis, ADD_LINE_NAME)

		return added_plot

	@checked_arguments
	def add_bar(self, data: Table | Array, chart: BarChart | None = None, axis: ValueAxis = ValueAxis.LEFT) -> Self:
		"""
		Return a new Plot with vertical bars added over the charts of this one.

		The bars are drawn over the ones already there, at the same positions: to draw bars side by side, give
		several columns to a single ``BarChart``. Their ``x`` values are placed on the labels of the Plot, new
		labels following the others.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array of the bars, which may differ from the one of the Plot.
		chart
			The columns drawn and the look of the bars, which must be vertical.
			The default ``BarChart`` when omitted, which draws an Array: a Table needs the columns named.
		axis
			``ValueAxis.LEFT`` by default to share the scale of the Plot, ``ValueAxis.RIGHT`` for a scale of
			their own on the right.

		Returns
		-------
		Self
			A new Plot; this one is left unchanged.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		RefusedSettingError
			When the bars are horizontal, or the Plot does not draw lines, vertical bars or points.
		IncompatibleChartsError
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates, texts or times of day;
			or when one measures numbers and the other times of day on the same axis.
		DuplicateLabelError
			When a label appears twice in the ``x`` values of one chart.
		InvalidChartDataError
			When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.
		InvalidColorCountError
			When the colors of the chart are not one per series.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
		>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
		>>> targets = ndp.Array.from_list([130.0, 130.0, 140.0, 160.0])
		>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "target": targets})
		>>> plot = ndp.Plot.bar(shop, ndp.BarChart(x="month", y=["target"], colors=[ndp.CustomColor("#d9d9d9")]))
		>>> bars = ndp.BarChart(x="month", y=["sales"], colors=[ndp.Color.BLUE])
		>>> both = plot.add_bar(shop, bars)
		>>> both.show()
		"""
		if chart is None:
			chart = BarChart()

		require_vertical_bars(chart, ADD_BAR_NAME)
		layer = read_bar_layer(data, chart)
		added_plot = self._add_layer(layer, axis, ADD_BAR_NAME)

		return added_plot

	@checked_arguments
	def add_scatter(
		self, data: Table | Array, chart: ScatterChart | None = None, axis: ValueAxis = ValueAxis.LEFT
	) -> Self:
		"""
		Return a new Plot with points added over the charts of this one.

		The points take the color of the default cycle after the ones already used, unless ``color`` or
		``color_by`` is given. Over bars or texts, their ``x`` values are placed on the labels of the Plot.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The Table or the Array of the points, which may differ from the one of the Plot.
		chart
			The columns drawn and the look of the points.
			The default ``ScatterChart`` when omitted, which draws an Array: a Table needs the columns named.
		axis
			``ValueAxis.LEFT`` by default to share the scale of the Plot, ``ValueAxis.RIGHT`` for a scale of
			their own on the right.

		Returns
		-------
		Self
			A new Plot; this one is left unchanged.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		RefusedSettingError
			When the Plot does not draw lines, vertical bars or points.
		IncompatibleChartsError
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates, texts or times of day;
			or when one measures numbers and the other times of day on the same axis.
		DuplicateLabelError
			When a label appears twice in the ``x`` values of one chart placed on labels.
		InvalidChartDataError
			When a Table has no ``y`` column, or an Array has a column setting.
		InvalidColorCountError
			When ``color`` is given for an Array of several columns.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> days = ndp.Array.from_list([1, 2, 3, 4, 5, 6])
		>>> trend = ndp.Array.from_list([10.0, 12.0, 14.0, 16.0, 18.0, 20.0])
		>>> measures = ndp.Array.from_list([10.5, 11.2, 14.8, 15.1, 18.9, 19.4])
		>>> readings = ndp.Table.from_arrays({"day": days, "trend": trend, "measure": measures})
		>>> plot = ndp.Plot.line(readings, ndp.LineChart(x="day", y=["trend"]))
		>>> points = ndp.ScatterChart(x="day", y="measure")
		>>> both = plot.add_scatter(readings, points)
		>>> both.show()
		"""
		if chart is None:
			chart = ScatterChart()

		layer = read_scatter_layer(data, chart)
		added_plot = self._add_layer(layer, axis, ADD_SCATTER_NAME)

		return added_plot

	def _add_layer(self, layer: ChartLayer, axis: ValueAxis, method_name: str) -> Self:
		"""
		Return a new Plot with a chart added after the ones of this one, once checked against them.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layer
			The chart added and its values.
		axis
			The vertical axis the chart is measured on.
		method_name
			The method adding the chart, shown in error messages.

		Returns
		-------
		Self
			The new Plot, with the style of this one.

		Raises
		------
		RefusedSettingError
			When the Plot does not draw lines, vertical bars or points.
		IncompatibleChartsError
			When the ``x`` values are not of the kind of the ones of the Plot, or when one measures numbers and the
			other times of day on the same axis.
		DuplicateLabelError
			When a label appears twice in the ``x`` values of one chart placed on labels.
		"""
		first_layer = self._layers[0]
		require_overlay_base(first_layer, method_name)
		require_same_positions(first_layer, layer)
		require_same_values(self._layers, layer, axis)
		axis_layer = replace(layer, value_axis=axis)
		layers = [*self._layers, axis_layer]
		# Aligning the charts on their labels checks them, so a wrong chart is refused when it is added.
		align_layers(layers)
		plot_class = type(self)
		added_plot = plot_class._create(layers, self._style)

		return added_plot
