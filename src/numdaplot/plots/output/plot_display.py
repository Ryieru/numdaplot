"""
Display of a Plot or a Figure in a Jupyter notebook or in a matplotlib window.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings
from importlib import import_module
from io import BytesIO

from matplotlib.backends.registry import BackendFilter, backend_registry
from matplotlib.figure import Figure

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.display_warning import DisplayWarning
from numdaplot.plots.drawing.plot_drawing import FIGURE_LAYOUT, FigureDrawing, build_figure, draw_on_figure
from numdaplot.plots.output.shown_object import ShownObject
from numdaplot.plots.style.image_options import DEFAULT_DPI
from numdaplot.tables.preview.notebook_display import is_notebook

IPYTHON_DISPLAY_MODULE = "IPython.display"
PNG_FORMAT = "png"
NO_WINDOW_MESSAGE = (
	"No window can be opened, matplotlib has no graphical backend here. Install tkinter (python3-tk on Debian and "
	"Ubuntu) to see the {object_name}, or save it with {class_name}.save."
)


def show_drawing(drawing: FigureDrawing, shown_object: ShownObject) -> None:
	"""
	Show what a Plot or a Figure draws: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

	.. versionadded:: 0.1.0

	Parameters
	----------
	drawing
		What is drawn, and the size of the figure.
	shown_object
		Whether a Plot or a Figure is shown, named by the warning emitted when no window can be opened.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> from numdaplot.plots.output.plot_display import show_drawing
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> show_drawing(FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0)), ShownObject.PLOT)
	"""
	runs_in_notebook = is_notebook()
	if not runs_in_notebook:
		show_drawing_in_window(drawing, shown_object)
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


def show_drawing_in_window(drawing: FigureDrawing, shown_object: ShownObject) -> None:
	"""
	Show what a Plot or a Figure draws in a matplotlib window.

	The call waits until the window is closed, unless matplotlib runs interactively. With a matplotlib backend
	that opens no window, such as the one of a server, nothing is drawn and a ``DisplayWarning`` is emitted.

	.. versionadded:: 0.1.0

	.. versionchanged:: 0.2.0
		A ``BEST`` legend hiding a value is moved past the axes, as in an image or a notebook.

	Parameters
	----------
	drawing
		What is drawn, and the size of the figure.
	shown_object
		Whether a Plot or a Figure is shown, named by the warning emitted when no window can be opened.

	Examples
	--------
	>>> from numdaplot.plots.drawing.plot_drawing import FigureDrawing
	>>> from numdaplot.plots.output.plot_display import show_drawing_in_window
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> drawing = FigureDrawing(lambda target: target.suptitle("Sales"), (3.0, 2.0))
	>>> show_drawing_in_window(drawing, ShownObject.FIGURE)
	"""
	# pyplot chooses a matplotlib backend when imported, so it is only imported to open a window.
	from matplotlib import pyplot

	backend_name = pyplot.get_backend()
	can_open_window = is_window_backend(backend_name)
	if not can_open_window:
		warn_without_window(shown_object)
		return

	figure = pyplot.figure(figsize=drawing.size_inches, dpi=DEFAULT_DPI, layout=FIGURE_LAYOUT)
	draw_on_figure(drawing, figure)
	pyplot.show()
	is_interactive = pyplot.isinteractive()
	if not is_interactive:
		pyplot.close(figure)


def is_window_backend(backend_name: str) -> bool:
	"""
	Return whether a matplotlib backend opens windows.

	Only the backends matplotlib lists as non-interactive, such as ``agg`` chosen when no window can be opened,
	are refused: a backend added by another package is trusted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	backend_name
		The name matplotlib gives to its backend, such as ``tkagg`` or ``agg``, in any case.

	Returns
	-------
	bool
		False for a matplotlib backend without window, True otherwise.

	Examples
	--------
	>>> from numdaplot.plots.output.plot_display import is_window_backend
	>>> is_window_backend("Agg")
	False
	>>> is_window_backend("TkAgg")
	True
	"""
	lowered_name = backend_name.lower()
	non_interactive_names = backend_registry.list_builtin(BackendFilter.NON_INTERACTIVE)
	is_window = lowered_name not in non_interactive_names

	return is_window


def warn_without_window(shown_object: ShownObject) -> None:
	"""
	Emit a ``DisplayWarning`` pointing at the line of the calling code that asked to show a Plot or a Figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	shown_object
		Whether a Plot or a Figure could not be shown.

	Examples
	--------
	>>> import warnings
	>>> from numdaplot.plots.output.plot_display import warn_without_window
	>>> from numdaplot.plots.output.shown_object import ShownObject
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_without_window(ShownObject.FIGURE)
	>>> print(caught_warnings[0].message)
	No window can be opened, matplotlib has no graphical backend here. Install tkinter (python3-tk on Debian and
	Ubuntu) to see the figure, or save it with Figure.save.
	"""
	class_name = shown_object.value
	object_name = class_name.lower()
	message = NO_WINDOW_MESSAGE.format(object_name=object_name, class_name=class_name)
	warnings.warn(message, DisplayWarning, skip_file_prefixes=INTERNAL_FILES)
