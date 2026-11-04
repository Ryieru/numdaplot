"""
Unit tests of the drawing of a Plot on a matplotlib figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import matplotlib
from matplotlib.colors import to_hex
from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.drawing.plot_drawing import build_figure, draw_plot
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0])
LAYER = ChartLayer(ndp.LineChart(), read_array_values(PRICES, "LineChart"))
PIXEL_STYLE = ndp.Style(size=ndp.Size(width=300, height=200, unit=ndp.SizeUnit.PIXEL))
EXPECTED_PIXEL_INCHES = [3.0, 2.0]
FONT_SIZE_SETTING = "font.size"


def test_build_figure_has_the_size_of_the_style() -> None:
	"""
	Check that the figure has the size of the style, in inches.

	.. versionadded:: 0.1.0
	"""
	figure = build_figure([LAYER], PIXEL_STYLE)

	inches = figure.get_size_inches().tolist()
	assert inches == EXPECTED_PIXEL_INCHES


def test_build_figure_gives_a_new_figure_each_time() -> None:
	"""
	Check that two calls give two figures.

	.. versionadded:: 0.1.0
	"""
	first_figure = build_figure([LAYER], ndp.Style())
	second_figure = build_figure([LAYER], ndp.Style())

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
