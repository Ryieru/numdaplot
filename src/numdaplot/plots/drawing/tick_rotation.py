"""
Rotation of the labels of the ``x`` and ``y`` values of a Plot.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from typing import Literal

from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.dates import ConciseDateFormatter
from matplotlib.ticker import ScalarFormatter

from numdaplot.plots.drawing.drawn_chart import DrawnChart
from numdaplot.plots.drawing.position_axis import find_axis

TEXT_ROTATION = 45.0
NO_ROTATION = 0.0
ANCHOR_ROTATION_MODE = "anchor"
MINUS_SIGN = "\N{MINUS SIGN}"
HYPHEN_MINUS = "-"


def rotate_x_labels(axes: Axes, drawn_chart: DrawnChart, rotation: float | None) -> None:
	"""
	Rotate the labels of the ``x`` values, wherever the chart places them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		Which axis holds the ``x`` values.
	rotation
		The angle in degrees. When None, 45 degrees for texts and moments, and no rotation for numbers
		and for labels on the vertical axis.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.tick_rotation import rotate_x_labels
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 1.0], ["Paris", "Lyon"])  # doctest: +ELLIPSIS
	[...]
	>>> rotate_x_labels(axes, DrawnChart(None, None, False, GridAxes.NONE, None), None)
	>>> axes.get_xticklabels()[0].get_rotation()
	45.0
	"""
	if drawn_chart.x_on_vertical_axis:
		vertical_rotation = NO_ROTATION if rotation is None else rotation
		apply_rotation(axes, True, vertical_rotation)
		return

	horizontal_rotation = choose_rotation(axes.xaxis, rotation)
	apply_rotation(axes, False, horizontal_rotation)


def rotate_y_labels(axes: Axes, drawn_chart: DrawnChart, rotation: float | None) -> None:
	"""
	Rotate the labels of the ``y`` values, wherever the chart places them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	drawn_chart
		Which axis holds the ``x`` values: the ``y`` values are on the other one.
	rotation
		The angle in degrees. When None, the labels stay horizontal.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.drawn_chart import DrawnChart
	>>> from numdaplot.plots.drawing.grid_axes import GridAxes
	>>> from numdaplot.plots.drawing.tick_rotation import rotate_y_labels
	>>> axes = Figure().add_subplot()
	>>> rotate_y_labels(axes, DrawnChart(None, None, False, GridAxes.NONE, None), 30.0)
	>>> axes.get_yticklabels()[0].get_rotation()
	30.0
	"""
	if rotation is None:
		return

	y_on_vertical_axis = not drawn_chart.x_on_vertical_axis
	apply_rotation(axes, y_on_vertical_axis, rotation)


def apply_rotation(axes: Axes, on_vertical_axis: bool, rotation: float) -> None:
	"""
	Rotate the labels of an axis around their end closest to the axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The matplotlib axes of the Plot.
	on_vertical_axis
		True for the vertical axis, whose labels already end at their tick.
	rotation
		The angle in degrees.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.tick_rotation import apply_rotation
	>>> axes = Figure().add_subplot()
	>>> apply_rotation(axes, False, 45.0)
	>>> axes.get_xticklabels()[0].get_horizontalalignment()
	'right'
	"""
	axis = find_axis(axes, on_vertical_axis)
	axis.set_tick_params(labelrotation=rotation)
	alignment = choose_alignment(rotation)

	for label in axis.get_ticklabels():
		label.set_rotation_mode(ANCHOR_ROTATION_MODE)
		if not on_vertical_axis:
			label.set_horizontalalignment(alignment)


def choose_rotation(axis: Axis, rotation: float | None) -> float:
	"""
	Return the angle of the labels of a horizontal axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The horizontal axis, with its ticks.
	rotation
		The angle chosen in degrees, or None.

	Returns
	-------
	float
		The angle chosen, else 45 degrees for texts and moments, and no rotation for numbers.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.tick_rotation import choose_rotation
	>>> axes = Figure().add_subplot()
	>>> choose_rotation(axes.xaxis, None), choose_rotation(axes.xaxis, 30.0)
	(0.0, 30.0)
	"""
	if rotation is not None:
		return rotation

	has_text = has_text_labels(axis)
	if has_text:
		return TEXT_ROTATION

	return NO_ROTATION


def has_text_labels(axis: Axis) -> bool:
	"""
	Return whether the labels of an axis are moments, or texts that are not all numbers.

	Numbers can be written as texts, such as the years or the row numbers below bars: they stay numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		An axis, with its ticks.

	Returns
	-------
	bool
		True when at least one label is not a number. An axis without label holds no text.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.tick_rotation import has_text_labels
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 1.0], ["2025", "2026"])  # doctest: +ELLIPSIS
	[...]
	>>> has_text_labels(axes.xaxis)
	False
	"""
	formatter = axis.get_major_formatter()
	if isinstance(formatter, ScalarFormatter):
		return False

	if isinstance(formatter, ConciseDateFormatter):
		return True

	labels = axis.get_ticklabels()

	for label in labels:
		label_text = label.get_text()
		is_number = is_number_text(label_text)
		if not is_number:
			return True

	return False


def is_number_text(text: str) -> bool:
	"""
	Return whether a label is a number, as matplotlib or numdaplot writes it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of a label.

	Returns
	-------
	bool
		True for a number, with the minus sign matplotlib writes, or for an empty label.

	Examples
	--------
	>>> from numdaplot.plots.drawing.tick_rotation import is_number_text
	>>> is_number_text("2025"), is_number_text("-1.5"), is_number_text("Paris")
	(True, True, False)
	"""
	if text == "":
		return True

	python_text = text.replace(MINUS_SIGN, HYPHEN_MINUS)
	try:
		float(python_text)
	except ValueError:
		return False

	return True


def choose_alignment(rotation: float) -> Literal["left", "center", "right"]:
	"""
	Return the side of a rotated label that stays under its tick.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rotation
		The angle of the label in degrees.

	Returns
	-------
	Literal["left", "center", "right"]
		The end of the text for a positive angle, its start for a negative one, its middle without rotation.

	Examples
	--------
	>>> from numdaplot.plots.drawing.tick_rotation import choose_alignment
	>>> choose_alignment(45.0), choose_alignment(-45.0), choose_alignment(0.0)
	('right', 'left', 'center')
	"""
	if rotation > NO_ROTATION:
		return "right"

	if rotation < NO_ROTATION:
		return "left"

	return "center"
