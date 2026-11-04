"""
Display of a Plot in a Jupyter notebook or in a matplotlib window.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from importlib import import_module
from io import BytesIO

from matplotlib.figure import Figure

from numdaplot.plots.chart_layer import ChartLayer
from numdaplot.plots.drawing.plot_drawing import FIGURE_LAYOUT, build_figure, draw_plot
from numdaplot.plots.style.image_options import DEFAULT_DPI
from numdaplot.plots.style.style import Style
from numdaplot.tables.preview.notebook_display import is_notebook

IPYTHON_DISPLAY_MODULE = "IPython.display"
PNG_FORMAT = "png"


def show_plot(layers: list[ChartLayer], style: Style) -> None:
	"""
	Show a Plot: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.
	style
		The look of the Plot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.output.plot_display import show_plot
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> show_plot([ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))], ndp.Style())
	"""
	runs_in_notebook = is_notebook()
	if not runs_in_notebook:
		show_plot_in_window(layers, style)
		return

	figure = build_figure(layers, style)
	show_figure_in_notebook(figure)


def show_figure_in_notebook(figure: Figure) -> None:
	"""
	Show a matplotlib figure as a PNG image in the output of a Jupyter notebook cell.

	.. versionadded:: 0.1.0

	Parameters
	----------
	figure
		The figure to show.
	"""
	image_buffer = BytesIO()
	figure.savefig(image_buffer, format=PNG_FORMAT, dpi=DEFAULT_DPI)
	image_bytes = image_buffer.getvalue()
	display_module = import_module(IPYTHON_DISPLAY_MODULE)
	image = display_module.Image(data=image_bytes)
	display_module.display(image)


def show_plot_in_window(layers: list[ChartLayer], style: Style) -> None:
	"""
	Show a Plot in a matplotlib window, and wait until it is closed unless matplotlib runs interactively.

	With a matplotlib backend that opens no window, such as the one of a server, matplotlib warns that the
	figure cannot be shown.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layers
		The charts of the Plot and their values.
	style
		The look of the Plot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.chart_layer import ChartLayer
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> from numdaplot.plots.output.plot_display import show_plot_in_window
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> show_plot_in_window([ChartLayer(ndp.LineChart(), read_array_values(prices, "LineChart"))], ndp.Style())
	"""
	# pyplot chooses a matplotlib backend when imported, so it is only imported to open a window.
	from matplotlib import pyplot

	figure_size = style.size.to_inches()
	figure = pyplot.figure(figsize=figure_size, dpi=DEFAULT_DPI, layout=FIGURE_LAYOUT)
	draw_plot(figure, layers, style)
	pyplot.show()
	is_interactive = pyplot.isinteractive()
	if not is_interactive:
		pyplot.close(figure)
