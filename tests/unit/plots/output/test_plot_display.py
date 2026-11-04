"""
Unit tests of the display of a Plot or a Figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from types import SimpleNamespace
from typing import Any

import pytest
from matplotlib import pyplot
from matplotlib.figure import Figure, FigureBase

from numdaplot.plots.drawing.plot_drawing import FigureDrawing
from numdaplot.plots.output import plot_display
from numdaplot.plots.output.plot_display import show_drawing, show_drawing_in_window, show_figure_in_notebook

TITLE = "Prices"
DRAWING_SIZE = (6.4, 4.8)
PNG_SIGNATURE = b"\x89PNG"
IS_NOTEBOOK_NAME = "is_notebook"
IMPORT_MODULE_NAME = "import_module"
SHOW_IN_WINDOW_NAME = "show_drawing_in_window"
SHOW_IN_NOTEBOOK_NAME = "show_figure_in_notebook"


class DisplayModule:
	"""
	Fake ``IPython.display`` module keeping the images it displays.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without displayed object.

		.. versionadded:: 0.1.0
		"""
		self.displayed_objects = list[Any]()

	def Image(self, data: bytes) -> SimpleNamespace:  # noqa: N802
		"""
		Return a fake image holding its bytes, as ``IPython.display.Image`` does.

		.. versionadded:: 0.1.0

		Parameters
		----------
		data
			The bytes of the image.

		Returns
		-------
		SimpleNamespace
			An object whose ``data`` is the bytes.
		"""
		image = SimpleNamespace(data=data)

		return image

	def display(self, shown_object: Any) -> None:
		"""
		Keep a displayed object.

		.. versionadded:: 0.1.0

		Parameters
		----------
		shown_object
			The displayed object.
		"""
		self.displayed_objects.append(shown_object)


class Recorder:
	"""
	Fake function keeping the arguments of each call.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without call.

		.. versionadded:: 0.1.0
		"""
		self.calls = list[tuple[Any, ...]]()

	def __call__(self, *arguments: Any) -> None:
		"""
		Keep the arguments of a call.

		.. versionadded:: 0.1.0

		Parameters
		----------
		*arguments
			The arguments given.
		"""
		self.calls.append(arguments)


def draw_titled_axes(target: FigureBase) -> None:
	"""
	Draw axes titled Prices on a matplotlib figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target
		The figure drawn on.
	"""
	axes = target.add_subplot()
	axes.set_title(TITLE)


def describe_plot_drawing() -> FigureDrawing:
	"""
	Return a drawing of axes titled Prices.

	.. versionadded:: 0.1.0

	Returns
	-------
	FigureDrawing
		What is drawn, and its size.
	"""
	drawing = FigureDrawing(draw_titled_axes, DRAWING_SIZE)

	return drawing


def answer_value(answer: bool) -> Any:
	"""
	Return a fake notebook check giving one answer.

	.. versionadded:: 0.1.0

	Parameters
	----------
	answer
		The answer of the check.

	Returns
	-------
	Any
		A function without arguments returning the answer.
	"""

	def check() -> bool:
		"""
		Return the fixed answer.

		.. versionadded:: 0.1.0

		Returns
		-------
		bool
			The answer.
		"""
		return answer

	return check


def test_show_figure_in_notebook_displays_a_png_image(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a notebook receives the figure as PNG bytes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the import of IPython with a fake display module.
	"""
	display_module = DisplayModule()

	def give_display_module(module_name: str) -> DisplayModule:
		"""
		Return the fake display module whatever the name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		module_name
			The imported name, ignored.

		Returns
		-------
		DisplayModule
			The fake module.
		"""
		return display_module

	monkeypatch.setattr(plot_display, IMPORT_MODULE_NAME, give_display_module)

	show_figure_in_notebook(Figure())

	shown_image = display_module.displayed_objects[0]
	image_start = shown_image.data[:4]
	assert image_start == PNG_SIGNATURE


def test_show_drawing_opens_a_window_outside_a_notebook(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a script shows the drawing in a matplotlib window.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the window display with fakes.
	"""
	window_display = Recorder()
	monkeypatch.setattr(plot_display, IS_NOTEBOOK_NAME, answer_value(False))
	monkeypatch.setattr(plot_display, SHOW_IN_WINDOW_NAME, window_display)

	drawing = describe_plot_drawing()

	show_drawing(drawing)

	assert window_display.calls == [(drawing,)]


def test_show_drawing_displays_an_image_in_a_notebook(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a notebook receives the drawn figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the notebook check and the notebook display with fakes.
	"""
	notebook_display = Recorder()
	monkeypatch.setattr(plot_display, IS_NOTEBOOK_NAME, answer_value(True))
	monkeypatch.setattr(plot_display, SHOW_IN_NOTEBOOK_NAME, notebook_display)

	drawing = describe_plot_drawing()

	show_drawing(drawing)

	shown_figure = notebook_display.calls[0][0]
	assert shown_figure.axes[0].get_title() == "Prices"


def test_show_drawing_in_window_closes_the_figure_once_shown() -> None:
	"""
	Check that pyplot keeps no figure after a non-interactive display.

	.. versionadded:: 0.1.0
	"""
	figure_numbers = pyplot.get_fignums()
	drawing = describe_plot_drawing()

	show_drawing_in_window(drawing)

	assert pyplot.get_fignums() == figure_numbers
