"""
Unit tests of the drawing of a Plot on a matplotlib figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import replace

import matplotlib
import pytest
from matplotlib.colors import to_hex
from matplotlib.figure import Figure, FigureBase

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.missing_map_chart import MissingMapChart
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.plots.drawing.plot_drawing import (
	CHART_DRAWERS,
	FigureDrawing,
	build_figure,
	draw_layers,
	draw_plot,
	find_right_axes,
)
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR
from numdaplot.plots.drawing.series_colors import COLOR_CODES

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
LAYER = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
SMALL_INCHES = (3.0, 2.0)
SALES = ndp.Table.from_arrays(
	{
		"city": ndp.Array.from_list(["Paris", "Lyon"]),
		"sales": ndp.Array.from_list([120.0, 80.0]),
		"price": ndp.Array.from_list([12.5, 11.0]),
	}
)
BARS = ChartLayer(ndp.BarChart(), read_table_values(SALES, "city", ["sales"], "BarChart"))
PRICE_LINE = ChartLayer(ndp.LineChart(), read_table_values(SALES, "city", ["price"], "LineChart"))
RIGHT_PRICE_LINE = replace(PRICE_LINE, value_axis=ndp.ValueAxis.RIGHT)
ORANGE_CODE = COLOR_CODES[ndp.Color.ORANGE]


def draw_title(target: FigureBase) -> None:
	"""
	Draw a title on a matplotlib figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target
		The figure drawn on.
	"""
	target.suptitle("Sales")


FONT_SIZE_SETTING = "font.size"
CHART_CLASSES = [
	ndp.LineChart,
	ndp.BarChart,
	ndp.ScatterChart,
	ndp.HistogramChart,
	ndp.BoxChart,
	ndp.PieChart,
	ndp.HeatmapChart,
	ndp.MissingChart,
	MissingMapChart,
]


def test_build_figure_draws_at_the_size_of_the_drawing() -> None:
	"""
	Check that the figure has the size of the drawing, in inches, and what it draws.

	.. versionadded:: 0.1.0
	"""
	drawing = FigureDrawing(draw_title, SMALL_INCHES)

	figure = build_figure(drawing)

	inches = figure.get_size_inches().tolist()
	assert inches == list(SMALL_INCHES)
	assert figure.get_suptitle() == "Sales"


def test_build_figure_gives_a_new_figure_each_time() -> None:
	"""
	Check that two calls give two figures.

	.. versionadded:: 0.1.0
	"""
	drawing = FigureDrawing(draw_title, SMALL_INCHES)

	first_figure = build_figure(drawing)
	second_figure = build_figure(drawing)

	assert first_figure is not second_figure


def test_draw_plot_hides_the_top_and_right_borders() -> None:
	"""
	Check the numdaplot look: no border at the top and on the right, white background.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()

	draw_plot(figure, [LAYER], ndp.Style())

	axes = figure.axes[0]
	assert not axes.spines["top"].get_visible()
	assert not axes.spines["right"].get_visible()
	assert to_hex(figure.get_facecolor()) == BACKGROUND_COLOR


def test_draw_plot_leaves_the_global_matplotlib_settings_unchanged() -> None:
	"""
	Check that the look is only applied while drawing.

	.. versionadded:: 0.1.0
	"""
	font_size = matplotlib.rcParams[FONT_SIZE_SETTING]

	draw_plot(Figure(), [LAYER], ndp.Style())

	assert matplotlib.rcParams[FONT_SIZE_SETTING] == font_size


@pytest.mark.parametrize("chart_class", CHART_CLASSES)
def test_every_chart_has_a_drawer(chart_class: type[Chart]) -> None:
	"""
	Check that each kind of chart is drawn by its own function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_class
		A chart class.
	"""
	assert chart_class in CHART_DRAWERS


def test_draw_plot_continues_the_colors_on_added_charts() -> None:
	"""
	Check that a line added over blue bars is orange.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()

	draw_plot(figure, [BARS, PRICE_LINE], ndp.Style())

	line_color = figure.axes[0].lines[0].get_color()
	assert line_color == ORANGE_CODE


def test_draw_layers_draws_a_right_chart_on_axes_of_its_own() -> None:
	"""
	Check that a chart on the right gets its own axes, which name its column by default.

	.. versionadded:: 0.1.0
	"""
	left_axes = Figure().add_subplot()

	plot_axes, first_chart = draw_layers(left_axes, [BARS, RIGHT_PRICE_LINE])

	right_axes = plot_axes.right
	assert right_axes is not None
	assert len(right_axes.lines) == 1
	assert len(left_axes.lines) == 0
	assert plot_axes.right_label == "price"
	assert first_chart.y_label == "sales"


def test_draw_layers_keeps_every_chart_on_the_left_by_default() -> None:
	"""
	Check that charts without right axis share the main axes.

	.. versionadded:: 0.1.0
	"""
	left_axes = Figure().add_subplot()

	plot_axes, _ = draw_layers(left_axes, [BARS, PRICE_LINE])

	assert plot_axes.right is None
	assert plot_axes.right_label is None


def test_find_right_axes_shows_the_right_border_once() -> None:
	"""
	Check that the right axes are created once, with their border on the right visible.

	.. versionadded:: 0.1.0
	"""
	left_axes = Figure().add_subplot()

	right_axes = find_right_axes(left_axes, None)
	same_axes = find_right_axes(left_axes, right_axes)

	assert same_axes is right_axes
	assert right_axes.spines["right"].get_visible()
