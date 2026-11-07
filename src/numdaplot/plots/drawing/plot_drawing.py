"""
Drawing of a Plot on a matplotlib figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

import matplotlib
from matplotlib.axes import Axes
from matplotlib.figure import Figure, FigureBase

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.box_chart import BoxChart
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.heatmap_chart import HeatmapChart
from numdaplot.plots.charts.histogram_chart import HistogramChart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.missing_chart import MissingChart
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.charts.pie_chart import PieChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.charts.value_axis import ValueAxis
from numdaplot.plots.data.renamed_layers import rename_layers
from numdaplot.plots.data.shown_columns import require_renamed_columns_shown
from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
from numdaplot.plots.drawing.box_drawing import draw_box_chart
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.heatmap_drawing import draw_heatmap_chart
from numdaplot.plots.drawing.histogram_drawing import draw_histogram_chart
from numdaplot.plots.drawing.layer_alignment import align_layers
from numdaplot.plots.drawing.layer_colors import continue_color_cycle
from numdaplot.plots.drawing.line_drawing import draw_line_chart
from numdaplot.plots.drawing.missing_drawing import draw_missing_chart, draw_missing_map
from numdaplot.plots.drawing.pie_drawing import draw_pie_chart
from numdaplot.plots.drawing.plot_axes import PlotAxes
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR, THEME
from numdaplot.plots.drawing.scatter_drawing import draw_scatter_chart
from numdaplot.plots.drawing.style_drawing import apply_style
from numdaplot.plots.drawing.time_axis import place_value_hours
from numdaplot.plots.style.image_options import DEFAULT_DPI
from numdaplot.plots.style.plot_style import PlotStyle

type ChartDrawer = Callable[[Axes, ChartLayer], DrawnChart]
"""A function drawing one kind of chart on matplotlib axes.

.. versionadded:: 0.1.0
"""

CHART_DRAWERS = dict[type[Chart], ChartDrawer](
	{
		LineChart: draw_line_chart,
		BarChart: draw_bar_chart,
		ScatterChart: draw_scatter_chart,
		HistogramChart: draw_histogram_chart,
		BoxChart: draw_box_chart,
		PieChart: draw_pie_chart,
		HeatmapChart: draw_heatmap_chart,
		MissingChart: draw_missing_chart,
		MissingMapChart: draw_missing_map,
	}
)
FIGURE_LAYOUT = "constrained"


@dataclass(frozen=True, eq=False)
class FigureDrawing:
	"""
	What a Plot or a Figure draws, and the size of the figure it needs.

	.. versionadded:: 0.1.0

	Parameters
	----------
	draw_on
		The function drawing on an empty matplotlib figure or subfigure.
	size_inches
		The width and the height of the figure, in inches.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> FigureDrawing(print, (6.4, 4.8)).size_inches
	(6.4, 4.8)
	"""

	draw_on: Callable[[FigureBase], None]
	size_inches: tuple[float, float]


def build_figure(drawing: FigureDrawing) -> Figure:
	"""
	Return a new matplotlib figure with a Plot or a Figure drawn on it.

	No matplotlib window or notebook shows the figure on its own.

	.. versionadded:: 0.1.0

	Parameters
	----------
	drawing
		What is drawn, and the size of the figure.

	Returns
	-------
	matplotlib.figure.Figure
		The figure, at 100 dots per inch.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure
	>>> figure = build_figure(FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0)))
	>>> figure.get_size_inches().tolist()
	[3.0, 2.0]
	"""
	figure = Figure(figsize=drawing.size_inches, dpi=DEFAULT_DPI, layout=FIGURE_LAYOUT)
	drawing.draw_on(figure)

	return figure


def draw_plot(figure: FigureBase, layers: list[ChartLayer], style: PlotStyle) -> None:
	"""
	Draw the charts of a Plot on new axes of a figure, then its style.

	The charts after the first one continue the default colors and share the ``x`` labels of the others.
	The numdaplot look is applied while drawing only, so the global matplotlib settings never change.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		An empty matplotlib figure or subfigure.
	layers
		The charts of the Plot and their values, the first one giving the default labels.
	style
		The look of the Plot.

	Raises
	------
	InvalidColorCountError
		When the colors of a chart are not one per series.
	ColumnNotFoundError
		When the style renames a column that no chart shows.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure, FigureBase
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.plot_drawing import draw_plot
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> figure = Figure()
	>>> draw_plot(figure, [ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))], ndp.PlotStyle())
	>>> figure.axes[0].spines["top"].get_visible()
	False
	"""
	require_renamed_columns_shown(layers, style.renaming)
	shown_layers = rename_layers(layers, style.renaming)
	figure.set_facecolor(BACKGROUND_COLOR)
	colored_layers = continue_color_cycle(shown_layers)
	aligned_layers = align_layers(colored_layers)

	# Some versions of the matplotlib stubs only accept the names of known settings as keys.
	theme = cast(Any, THEME)

	with matplotlib.rc_context(theme):
		left_axes = figure.add_subplot()
		plot_axes, first_chart = draw_layers(left_axes, aligned_layers)
		apply_style(plot_axes, first_chart, style)


def draw_layers(left_axes: Axes, layers: list[ChartLayer]) -> tuple[PlotAxes, DrawnChart]:
	"""
	Draw each chart of a Plot in order, on the left axes or on axes measured on the right.

	The axis of the values of each axes is labeled ``HH:MM`` when its lines or points measure times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_axes
		The main matplotlib axes of the Plot.
	layers
		The charts of the Plot and their values, the first one on the left.

	Returns
	-------
	tuple[PlotAxes, DrawnChart]
		The axes drawn on, with the default label of the axis on the right, and what the first chart tells the
		style.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from dataclasses import replace
	>>> from matplotlib.figure import Figure, FigureBase
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> from numdaplot.plots.drawing.plot_drawing import draw_layers
	>>> sales = ndp.Table.from_arrays(
	... 	{"sales": ndp.Array.from_list([120.0, 80.0]), "price": ndp.Array.from_list([12.5, 11.0])}
	... )
	>>> bars = ChartLayer(ndp.BarChart(), read_table_values(sales, None, ["sales"], "BarChart"))
	>>> line = ChartLayer(ndp.LineChart(), read_table_values(sales, None, ["price"], "LineChart"))
	>>> right_line = replace(line, value_axis=ndp.ValueAxis.RIGHT)
	>>> plot_axes, first_chart = draw_layers(Figure().add_subplot(), [bars, right_line])
	>>> plot_axes.right_label, first_chart.y_label
	('price', 'sales')
	"""
	right_axes = None
	left_charts = list[DrawnChart]()
	right_charts = list[DrawnChart]()
	left_layers = list[ChartLayer]()
	right_layers = list[ChartLayer]()

	for layer in layers:
		target_axes = left_axes
		target_charts = left_charts
		target_layers = left_layers
		if layer.value_axis == ValueAxis.RIGHT:
			right_axes = find_right_axes(left_axes, right_axes)
			target_axes = right_axes
			target_charts = right_charts
			target_layers = right_layers

		chart_class = type(layer.chart)
		draw_chart = CHART_DRAWERS[chart_class]
		drawn_chart = draw_chart(target_axes, layer)
		target_charts.append(drawn_chart)
		target_layers.append(layer)

	place_value_hours(left_axes, left_layers)
	right_label = None
	if right_axes is not None:
		place_value_hours(right_axes, right_layers)
		right_label = right_charts[0].y_label

	plot_axes = PlotAxes(left_axes, right_axes, right_label)

	return plot_axes, left_charts[0]


def find_right_axes(left_axes: Axes, right_axes: Axes | None) -> Axes:
	"""
	Return the axes measured on the right, created the first time a chart is drawn on them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_axes
		The main matplotlib axes of the Plot.
	right_axes
		The axes on the right already created, or None.

	Returns
	-------
	matplotlib.axes.Axes
		Axes sharing the ``x`` values of the main ones, with their scale drawn on the right.

	Examples
	--------
	>>> from matplotlib.figure import Figure, FigureBase
	>>> from numdaplot.plots.drawing.plot_drawing import find_right_axes
	>>> left_axes = Figure().add_subplot()
	>>> right_axes = find_right_axes(left_axes, None)
	>>> find_right_axes(left_axes, right_axes) is right_axes
	True
	"""
	if right_axes is not None:
		return right_axes

	new_axes = left_axes.twinx()
	# The numdaplot look hides the line on the right, which the scale on the right needs.
	right_spine = new_axes.spines["right"]
	right_spine.set_visible(True)

	return new_axes
