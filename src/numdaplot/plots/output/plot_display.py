"""
Display of a Plot or a Figure in a Jupyter notebook or in a matplotlib window.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from importlib import import_module
from io import BytesIO

from matplotlib.figure import Figure

from numdaplot.plots.drawing.plot_drawing import FIGURE_LAYOUT, FigureDrawing, build_figure
from numdaplot.plots.style.image_options import DEFAULT_DPI
from numdaplot.tables.preview.notebook_display import is_notebook

IPYTHON_DISPLAY_MODULE = "IPython.display"
PNG_FORMAT = "png"


def show_drawing(drawing: FigureDrawing) -> None:
	"""
	Show what a Plot or a Figure draws: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

	.. versionadded:: 0.1.0

	Parameters
	----------
	drawing
		What is drawn, and the size of the figure.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> from numdaplot.plots.output.plot_display import show_drawing
	>>> show_drawing(FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0)))
	"""
	runs_in_notebook = is_notebook()
	if not runs_in_notebook:
		show_drawing_in_window(drawing)
		return

	figure = build_figure(drawing)
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


def show_drawing_in_window(drawing: FigureDrawing) -> None:
	"""
	Show what a Plot or a Figure draws in a matplotlib window.

	The call waits until the window is closed, unless matplotlib runs interactively. With a matplotlib backend
	that opens no window, such as the one of a server, matplotlib warns that the figure cannot be shown.

	.. versionadded:: 0.1.0

	Parameters
	----------
	drawing
		What is drawn, and the size of the figure.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> from numdaplot.plots.output.plot_display import show_drawing_in_window
	>>> show_drawing_in_window(FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0)))
	"""
	# pyplot chooses a matplotlib backend when imported, so it is only imported to open a window.
	from matplotlib import pyplot

	figure = pyplot.figure(figsize=drawing.size_inches, dpi=DEFAULT_DPI, layout=FIGURE_LAYOUT)
	drawing.draw_on(figure)
	pyplot.show()
	is_interactive = pyplot.isinteractive()
	if not is_interactive:
		pyplot.close(figure)
