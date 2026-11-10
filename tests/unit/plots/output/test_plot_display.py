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

from numdaplot.errors.display_warning import DisplayWarning
from numdaplot.plots.drawing.plot_drawing import FigureDrawing
from numdaplot.plots.output import plot_display
from numdaplot.plots.output.plot_display import (
	is_window_backend,
	show_drawing,
	show_drawing_in_window,
	show_figure_in_notebook,
	warn_without_window,
)
from numdaplot.plots.output.shown_object import ShownObject

TITLE = "Prices"
DRAWING_SIZE = (6.4, 4.8)
PNG_SIGNATURE = b"\x89PNG"
IS_NOTEBOOK_NAME = "is_notebook"
IMPORT_MODULE_NAME = "import_module"
SHOW_IN_WINDOW_NAME = "show_drawing_in_window"
SHOW_IN_NOTEBOOK_NAME = "show_figure_in_notebook"
IS_WINDOW_BACKEND_NAME = "is_window_backend"
SHOW_NAME = "show"
IS_INTERACTIVE_NAME = "isinteractive"
PLOT_ADVICE = "to see the plot, or save it with Plot.save"
FIGURE_ADVICE = "to see the figure, or save it with Figure.save"
NO_WINDOW_BACKENDS = ["agg", "Agg", "pdf", "svg"]
WINDOW_BACKENDS = ["TkAgg", "qtagg", "module://some_package.backend"]


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


def answer_backend(answer: bool) -> Any:
	"""
	Return a fake backend check giving one answer.

	.. versionadded:: 0.1.0

	Parameters
	----------
	answer
		Whether the backend opens windows.

	Returns
	-------
	Any
		A function taking a backend name and returning the answer.
	"""

	def check(backend_name: str) -> bool:
		"""
		Return the fixed answer.

		.. versionadded:: 0.1.0

		Parameters
		----------
		backend_name
			The backend name, ignored.

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

	show_drawing(drawing, ShownObject.PLOT)

	assert window_display.calls == [(drawing, ShownObject.PLOT)]


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

	show_drawing(drawing, ShownObject.PLOT)

	shown_figure = notebook_display.calls[0][0]
	assert shown_figure.axes[0].get_title() == "Prices"


def test_show_drawing_in_window_closes_the_figure_once_shown(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that pyplot keeps no figure after a non-interactive display.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the backend check and the pyplot display with fakes.
	"""
	figure_numbers = pyplot.get_fignums()
	monkeypatch.setattr(plot_display, IS_WINDOW_BACKEND_NAME, answer_backend(True))
	monkeypatch.setattr(pyplot, SHOW_NAME, Recorder())
	drawing = describe_plot_drawing()

	show_drawing_in_window(drawing, ShownObject.PLOT)

	assert pyplot.get_fignums() == figure_numbers


@pytest.mark.parametrize(
	("shown_object", "expected_text"),
	[(ShownObject.PLOT, PLOT_ADVICE), (ShownObject.FIGURE, FIGURE_ADVICE)],
)
def test_show_drawing_in_window_warns_without_window_backend(
	monkeypatch: pytest.MonkeyPatch,
	shown_object: ShownObject,
	expected_text: str,
) -> None:
	"""
	Check that a backend without window emits a DisplayWarning naming the save method of the shown object.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the backend check and the pyplot display with fakes.
	shown_object
		The kind of object shown.
	expected_text
		The advice the message gives.
	"""
	window_display = Recorder()
	monkeypatch.setattr(plot_display, IS_WINDOW_BACKEND_NAME, answer_backend(False))
	monkeypatch.setattr(pyplot, SHOW_NAME, window_display)
	figure_numbers = pyplot.get_fignums()
	drawing = describe_plot_drawing()

	with pytest.warns(DisplayWarning, match=expected_text):
		show_drawing_in_window(drawing, shown_object)

	assert window_display.calls == []
	assert pyplot.get_fignums() == figure_numbers


def test_warn_without_window_points_at_the_caller() -> None:
	"""
	Check that the warning names the file of the calling code, not a numdaplot file.

	.. versionadded:: 0.1.0
	"""
	with pytest.warns(DisplayWarning) as caught_warnings:
		warn_without_window(ShownObject.PLOT)

	warning_file = caught_warnings[0].filename
	assert warning_file == __file__


@pytest.mark.parametrize("backend_name", NO_WINDOW_BACKENDS)
def test_is_window_backend_refuses_a_backend_without_window(backend_name: str) -> None:
	"""
	Check that the matplotlib backends without window are refused, whatever their case.

	.. versionadded:: 0.1.0

	Parameters
	----------
	backend_name
		A backend without window.
	"""
	is_window = is_window_backend(backend_name)

	assert not is_window


@pytest.mark.parametrize("backend_name", WINDOW_BACKENDS)
def test_is_window_backend_accepts_a_window_backend(backend_name: str) -> None:
	"""
	Check that window backends, and a backend added by another package, are accepted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	backend_name
		A backend opening windows.
	"""
	is_window = is_window_backend(backend_name)

	assert is_window


def test_show_drawing_in_window_keeps_the_figure_when_matplotlib_runs_interactively(
	monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""
	Check that an interactive matplotlib keeps the shown figure open.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the backend check, the pyplot display and the interactive check with fakes.
	"""
	monkeypatch.setattr(plot_display, IS_WINDOW_BACKEND_NAME, answer_backend(True))
	monkeypatch.setattr(pyplot, SHOW_NAME, Recorder())
	monkeypatch.setattr(pyplot, IS_INTERACTIVE_NAME, answer_value(True))
	figure_numbers = pyplot.get_fignums()
	drawing = describe_plot_drawing()

	show_drawing_in_window(drawing, ShownObject.PLOT)

	shown_figure_numbers = pyplot.get_fignums()
	shown_figure_count = len(shown_figure_numbers)
	previous_figure_count = len(figure_numbers)
	new_figure_count = shown_figure_count - previous_figure_count
	pyplot.close(shown_figure_numbers[-1])
	assert new_figure_count == 1
