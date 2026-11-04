"""
Drawing of a Plot on a matplotlib figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from collections.abc import Callable
from typing import Any, cast

import matplotlib
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.charts.bar_chart import BarChart
from numdaplot.plots.charts.chart import Chart
from numdaplot.plots.charts.line_chart import LineChart
from numdaplot.plots.charts.scatter_chart import ScatterChart
from numdaplot.plots.drawing.bar_drawing import draw_bar_chart
from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.line_drawing import draw_line_chart
from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR, THEME
from numdaplot.plots.drawing.scatter_drawing import draw_scatter_chart
from numdaplot.plots.drawing.style_drawing import apply_style
from numdaplot.plots.style.image_options import DEFAULT_DPI
from numdaplot.plots.style.style import Style

type ChartDrawer = Callable[[Axes, ChartLayer], DrawnChart]
"""A function drawing one kind of chart on matplotlib axes.

.. versionadded:: 0.1.0
"""

CHART_DRAWERS = dict[type[Chart], ChartDrawer](
	{
		LineChart: draw_line_chart,
		BarChart: draw_bar_chart,
		ScatterChart: draw_scatter_chart,
	}
)
FIGURE_LAYOUT = "constrained"


def build_figure(layers: list[ChartLayer], style: Style) -> Figure:
	"""
	Return a new matplotlib figure with a Plot drawn on it, which no matplotlib window or notebook shows on its own.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.
	style
		The look of the Plot.

	Returns
	-------
	matplotlib.figure.Figure
		The figure, of the size of the style at 100 dots per inch.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.plot_drawing import build_figure
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> layer = ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))
	>>> build_figure([layer], ndp.Style()).get_size_inches().tolist()
	[6.4, 4.8]
	"""
	figure_size = style.size.to_inches()
	figure = Figure(figsize=figure_size, dpi=DEFAULT_DPI, layout=FIGURE_LAYOUT)
	draw_plot(figure, layers, style)

	return figure


def draw_plot(figure: Figure, layers: list[ChartLayer], style: Style) -> None:
	"""
	Draw the charts of a Plot on new axes of a figure, then its style.

	The numdaplot look is applied while drawing only, so the global matplotlib settings never change.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		An empty matplotlib figure.
	layers
		The charts of the Plot and their values, the first one giving the default labels.
	style
		The look of the Plot.

	Raises
	------
	InvalidColorCountError
		When the colors of a chart are not one per series.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.drawing.plot_drawing import draw_plot
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> figure = Figure()
	>>> draw_plot(figure, [ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))], ndp.Style())
	>>> figure.axes[0].spines["top"].get_visible()
	False
	"""
	figure.set_facecolor(BACKGROUND_COLOR)
	drawn_charts = list[DrawnChart]()

	# Some versions of the matplotlib stubs only accept the names of known settings as keys.
	theme = cast(Any, THEME)

	with matplotlib.rc_context(theme):
		axes = figure.add_subplot()

		for layer in layers:
			chart_class = type(layer.chart)
			draw_chart = CHART_DRAWERS[chart_class]
			drawn_chart = draw_chart(axes, layer)
			drawn_charts.append(drawn_chart)

		apply_style(axes, drawn_charts[0], style)
