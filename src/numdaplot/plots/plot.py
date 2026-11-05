"""
A drawn view of a Table or an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import replace
from typing import Never, Self

from matplotlib.figure import Figure, FigureBase

from numdaplot.arrays.array import Array
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.drawing.layer_alignment import align_layers
from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure, draw_plot
from numdaplot.plots.drawing.size_inches import convert_size_to_inches
from numdaplot.plots.layer_reading import read_bar_layer, read_line_layer, read_scatter_layer
from numdaplot.plots.output.image_saving import write_image
from numdaplot.plots.output.plot_display import show_drawing
from numdaplot.plots.overlay_checks import require_overlay_base, require_same_positions, require_vertical_bars
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.plots.style.plot_style import PlotStyle
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.file_paths import FilePath
from numdaplot.tables.table import Table

ADD_LINE_NAME = "add_line"
ADD_BAR_NAME = "add_bar"
ADD_SCATTER_NAME = "add_scatter"
CONSTRUCTOR_OPERATION = "Creating a Plot with ndp.Plot(...)"
CONSTRUCTOR_ALTERNATIVE = "a plot_* function such as ndp.plot_line"


class Plot:
	"""
	A drawn view of a Table or an Array, made by the ``plot_*`` functions such as ``plot_line``.

	A Plot is immutable: it keeps the values it was made from, so changing the data afterwards never changes it.
	It is only displayed by ``show``, never on its own in a notebook.

	Calling ``ndp.Plot(...)`` is refused with ``RefusedOperationError``, which names the functions to use instead.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> plot = ndp.plot_line(prices)
	>>> plot.show()
	"""

	_layers: list[ChartLayer]
	_style: PlotStyle

	def __init__(self, *arguments: Never, **keyword_arguments: Never) -> None:
		"""
		Refuse the creation of a Plot by its constructor: the ``plot_*`` functions create Plots.

		.. versionadded:: 0.1.0

		Parameters
		----------
		arguments
			Any value, refused.
		keyword_arguments
			Any named value, refused.

		Raises
		------
		RefusedOperationError
			Always, naming the ``plot_*`` functions.
		"""
		raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)

	@classmethod
	def _create(cls, layers: list[ChartLayer], style: PlotStyle) -> Self:
		"""
		Return a new Plot keeping the charts and the style.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layers
			The charts and their values, made by the ``plot_*`` functions, the first one giving the default labels.
			The Plot keeps its own copy of the list.
		style
			The look of the Plot.

		Returns
		-------
		Self
			The new Plot.
		"""
		created_plot = cls.__new__(cls)
		created_plot._layers = list(layers)
		created_plot._style = style

		return created_plot

	def to_matplotlib(self) -> Figure:
		"""
		Return a new matplotlib figure of the Plot, to change it with matplotlib.

		Changing the figure never changes the Plot. The figure is not managed by ``matplotlib.pyplot``, so
		a notebook does not display it on its own.

		.. versionadded:: 0.1.0

		Returns
		-------
		matplotlib.figure.Figure
			The figure, drawn on a single matplotlib ``Axes``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
		>>> style = ndp.PlotStyle(title="Prices")
		>>> figure = ndp.plot_line(prices, style=style).to_matplotlib()
		>>> figure.axes[0].get_title()
		'Prices'
		>>> figure.axes[0].lines[0].get_ydata()
		array([12. , 15.5, 14. ])
		"""
		drawing = self._describe_drawing()
		figure = build_figure(drawing)

		return figure

	@checked_arguments
	def save(self, path: FilePath, options: ImageOptions | None = None, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Save the Plot as an image, in the format named by the extension of the path.

		``.png`` gives an image made of pixels, ``.svg`` and ``.pdf`` images made of lines and texts that stay
		sharp at any zoom. The image has the size of the style, 640 by 480 pixels for a PNG image by default.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the image, a ``FilePath`` such as ``"chart.png"`` or ``Path("images/chart.svg")``, ending with
			``.png``, ``.svg`` or ``.pdf``.
		options
			The resolution of a PNG image, 100 dots per inch when omitted. SVG and PDF images take none.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		UnsupportedImageFormatError
			When the path does not end with ``.png``, ``.svg`` or ``.pdf``.
		RefusedSettingError
			When options are given for an SVG or PDF image.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "prices.svg"
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
		>>> plot = ndp.plot_line(prices)
		>>> plot.save(path)
		>>> path.read_text().startswith("<?xml")
		True
		"""
		drawing = self._describe_drawing()
		write_image(drawing, path, options, on_conflict)

	def show(self) -> None:
		"""
		Show the Plot: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

		In a script, the window stays open until it is closed. With a matplotlib backend that opens no window,
		such as the one of a server, matplotlib warns that the figure cannot be shown: save it instead.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
		>>> plot = ndp.plot_bar(prices)
		>>> plot.show()
		"""
		drawing = self._describe_drawing()
		show_drawing(drawing)

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
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates or texts.
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
		>>> plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["sales"]))
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
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates or texts.
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
		>>> plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["target"], colors=[ndp.CustomColor("#d9d9d9")]))
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
			When the ``x`` values are not of the kind of the ones of the Plot: numbers, dates or texts.
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
		>>> plot = ndp.plot_line(readings, ndp.LineChart(x="day", y=["trend"]))
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
			When the ``x`` values are not of the kind of the ones of the Plot.
		DuplicateLabelError
			When a label appears twice in the ``x`` values of one chart placed on labels.
		"""
		first_layer = self._layers[0]
		require_overlay_base(first_layer, method_name)
		require_same_positions(first_layer, layer)
		axis_layer = replace(layer, value_axis=axis)
		layers = [*self._layers, axis_layer]
		# Aligning the charts on their labels checks them, so a wrong chart is refused when it is added.
		align_layers(layers)
		plot_class = type(self)
		added_plot = plot_class._create(layers, self._style)

		return added_plot

	def _draw_on(self, target: FigureBase) -> None:
		"""
		Draw the Plot on an empty matplotlib figure or subfigure, as ``show``, ``save`` and ``Figure`` do.

		.. versionadded:: 0.1.0

		Parameters
		----------
		target
			The figure or subfigure drawn on.
		"""
		draw_plot(target, self._layers, self._style)

	def _describe_drawing(self) -> FigureDrawing:
		"""
		Return what the Plot draws, and the size of its style.

		.. versionadded:: 0.1.0

		Returns
		-------
		FigureDrawing
			The drawing of the Plot.
		"""
		size_inches = convert_size_to_inches(self._style.size)
		drawing = FigureDrawing(self._draw_on, size_inches)

		return drawing
