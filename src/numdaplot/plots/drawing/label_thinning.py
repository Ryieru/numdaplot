"""
Choice of the labels of an axis that fit, the others being left out so that they stay readable.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import math
import warnings
from typing import cast

import numpy
from matplotlib.axis import Axis
from matplotlib.figure import Figure, SubFigure
from matplotlib.ticker import FixedLocator
from numpy.typing import NDArray

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.readability_warning import ReadabilityWarning

MINIMUM_TICKS = 2
LABEL_GAP_RATIO = 0.5
POINTS_PER_INCH = 72.0
RIGHT_ANGLE = 90.0
EVERY_LABEL = 1
# What the layout usually leaves around the axes for the numbers and the name of the other axis.
LAYOUT_MARGIN_PIXELS = 60.0
MINUS_SIGN = "\N{MINUS SIGN}"
HYPHEN_MINUS = "-"
WIDER_SIZE = "wider"
TALLER_SIZE = "taller"
HIDDEN_LABELS_MESSAGE = (
	"The chart shows {shown_count} of its {label_count} labels so that they stay readable. "
	"Give a {size_word} ndp.Size to show more of them."
)


def find_tick_locations(axis: Axis) -> NDArray[numpy.float64]:
	"""
	Return the coordinates of the ticks of an axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis.

	Returns
	-------
	NDArray[numpy.float64]
		One coordinate per tick.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_tick_locations
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 2.0])  # doctest: +ELLIPSIS
	[...]
	>>> find_tick_locations(axes.xaxis)
	array([0., 2.])
	"""
	tick_locations = numpy.asarray(axis.get_ticklocs(), dtype=numpy.float64)

	return tick_locations


def find_current_length(axis: Axis, on_vertical_axis: bool) -> float:
	"""
	Return the current length of the axes along an axis.

	The axes do not have their final size yet: the layout will make them a little longer.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis.
	on_vertical_axis
		True for the vertical axis.

	Returns
	-------
	float
		The length, in pixels.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_current_length
	>>> axes = Figure(figsize=(6.4, 4.8), dpi=100).add_subplot()
	>>> round(find_current_length(axes.xaxis, False), 1)
	496.0
	"""
	axes_box = axis.axes.get_window_extent()
	axes_length = axes_box.height if on_vertical_axis else axes_box.width

	return float(axes_length)


def estimate_final_length(axis: Axis, on_vertical_axis: bool) -> float:
	"""
	Return the length the axes will have along an axis, once the layout has given them their room.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis.
	on_vertical_axis
		True for the vertical axis.

	Returns
	-------
	float
		The size of the figure or subfigure less a usual margin, and at least the current length.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import estimate_final_length
	>>> axes = Figure(figsize=(6.4, 4.8), dpi=100).add_subplot()
	>>> estimate_final_length(axes.xaxis, False)
	580.0
	"""
	current_length = find_current_length(axis, on_vertical_axis)
	container = cast(Figure | SubFigure, axis.axes.get_figure())
	container_length = container.bbox.width
	if on_vertical_axis:
		container_length = container.bbox.height

	free_length = container_length - LAYOUT_MARGIN_PIXELS
	final_length = max(free_length, current_length)

	return float(final_length)


def find_tick_room(axis: Axis, on_vertical_axis: bool, axes_length: float) -> float:
	"""
	Return the pixels between the closest ticks of an axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with at least two ticks.
	on_vertical_axis
		True for the vertical axis.
	axes_length
		The length of the axes along this axis, in pixels.

	Returns
	-------
	float
		The room, in pixels.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_tick_room
	>>> axes = Figure().add_subplot()
	>>> axes.set_xlim(0.0, 10.0)
	(0.0, 10.0)
	>>> axes.xaxis.set_ticks([0.0, 1.0, 3.0], ["a", "b", "c"])  # doctest: +ELLIPSIS
	[...]
	>>> find_tick_room(axes.xaxis, False, 500.0)
	50.0
	"""
	view_start, view_stop = axis.axes.get_xbound()
	if on_vertical_axis:
		view_start, view_stop = axis.axes.get_ybound()

	pixels_per_unit = axes_length / (view_stop - view_start)
	ticks = find_tick_locations(axis)
	sorted_ticks = numpy.sort(ticks)
	tick_gaps = numpy.diff(sorted_ticks)
	smallest_tick_gap = tick_gaps.min()
	room = smallest_tick_gap * pixels_per_unit

	return float(room)


def find_font_pixels(axis: Axis) -> float:
	"""
	Return the font size of the labels of an axis, in pixels.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with at least one tick.

	Returns
	-------
	float
		The font size.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_font_pixels
	>>> axes = Figure(dpi=72).add_subplot()
	>>> axes.tick_params(labelsize=12.0)
	>>> find_font_pixels(axes.xaxis)
	12.0
	"""
	labels = axis.get_ticklabels()
	font_size = cast(float, labels[0].get_fontsize())
	figure = cast(Figure, axis.axes.get_figure(root=True))
	font_pixels = font_size * figure.dpi / POINTS_PER_INCH

	return font_pixels


def find_widest_label(axis: Axis) -> float:
	"""
	Return the width of the widest label of an axis, as written horizontally.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with labels that are not rotated yet.

	Returns
	-------
	float
		The width, in pixels.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_widest_label
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 1.0], ["a", "a long label"])  # doctest: +ELLIPSIS
	[...]
	>>> bool(find_widest_label(axes.xaxis) > 50.0)
	True
	"""
	labels = axis.get_ticklabels()
	label_boxes = [label.get_window_extent() for label in labels]
	label_widths = [label_box.width for label_box in label_boxes]
	widest_label = max(label_widths)

	return widest_label


def find_needed_room(axis: Axis, on_vertical_axis: bool, rotation: float) -> float:
	"""
	Return the pixels two neighbor labels of an axis need between their ticks.

	Labels along the axis need their width. Slanted labels sit side by side, so they need their font size divided
	by the sine of the angle with the axis, unless the whole label fits in less.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with labels that are not rotated yet.
	on_vertical_axis
		True for the vertical axis.
	rotation
		The angle of the labels in degrees, from the horizontal.

	Returns
	-------
	float
		The room needed, in pixels.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_needed_room
	>>> axes = Figure(dpi=72).add_subplot()
	>>> axes.tick_params(labelsize=10.0)
	>>> axes.yaxis.set_ticks([0.0, 1.0], ["Paris", "Lyon"])  # doctest: +ELLIPSIS
	[...]
	>>> find_needed_room(axes.yaxis, True, 0.0)
	10.0
	"""
	font_pixels = find_font_pixels(axis)
	widest_label = find_widest_label(axis)
	angle_with_axis = abs(rotation)
	if on_vertical_axis:
		angle_with_axis = RIGHT_ANGLE - angle_with_axis

	if angle_with_axis == 0:
		along_axis_room = widest_label + font_pixels * LABEL_GAP_RATIO
		return along_axis_room

	angle_radians = math.radians(angle_with_axis)
	sine = math.sin(angle_radians)
	cosine = math.cos(angle_radians)
	side_by_side_room = font_pixels / sine
	whole_label_room = widest_label * cosine + font_pixels * sine
	needed_room = min(side_by_side_room, whole_label_room)

	return needed_room


def find_label_step(axis: Axis, on_vertical_axis: bool, rotation: float) -> int:
	"""
	Return how often a label of an axis can be shown: 1 for each one, 3 for one out of three.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with labels that are not rotated yet.
	on_vertical_axis
		True for the vertical axis.
	rotation
		The angle the labels will take, in degrees.

	Returns
	-------
	int
		The step, 1 when the ticks are not fixed on each value, as matplotlib then chooses labels that fit.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import find_label_step
	>>> axes = Figure(figsize=(6.4, 4.8), dpi=100).add_subplot()
	>>> ticks = [float(tick) for tick in range(60)]
	>>> axes.xaxis.set_ticks(ticks, [str(tick) for tick in ticks])  # doctest: +ELLIPSIS
	[...]
	>>> find_label_step(axes.xaxis, False, 45.0)
	2
	"""
	locator = axis.get_major_locator()
	if not isinstance(locator, FixedLocator):
		return EVERY_LABEL

	tick_locations = find_tick_locations(axis)
	tick_count = len(tick_locations)
	if tick_count < MINIMUM_TICKS:
		return EVERY_LABEL

	final_length = estimate_final_length(axis, on_vertical_axis)
	room = find_tick_room(axis, on_vertical_axis, final_length)
	if room <= 0:
		return EVERY_LABEL

	needed_room = find_needed_room(axis, on_vertical_axis, rotation)
	room_ratio = needed_room / room
	label_step = math.ceil(room_ratio)

	return label_step


def is_ordered_text(text: str) -> bool:
	"""
	Return whether a label is a number or a date, which a reader can find from its neighbors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of a label.

	Returns
	-------
	bool
		True for a number, a date, a datetime or an empty label, False for another text.

	Examples
	--------
	>>> from numdaplot.plots.drawing.label_thinning import is_ordered_text
	>>> is_ordered_text("2025"), is_ordered_text("2026-01-31"), is_ordered_text("Paris")
	(True, True, False)
	"""
	if text == "":
		return True

	python_text = text.replace(MINUS_SIGN, HYPHEN_MINUS)
	try:
		float(python_text)
	except ValueError:
		pass
	else:
		return True

	try:
		numpy.datetime64(python_text)
	except ValueError:
		return False

	return True


def warn_hidden_labels(label_texts: list[str], shown_count: int, on_vertical_axis: bool) -> None:
	"""
	Warn that labels naming the values of a chart are left out, numbers and dates being found from their neighbors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	label_texts
		Every label of the axis.
	shown_count
		The number of labels kept.
	on_vertical_axis
		True for the vertical axis, which needs a taller size to show more labels.

	Warns
	-----
	ReadabilityWarning
		When a left out label may be a text.

	Examples
	--------
	>>> import warnings
	>>> from numdaplot.plots.drawing.label_thinning import warn_hidden_labels
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_hidden_labels(["Paris", "Lyon", "Nice"], 2, False)
	>>> print(caught_warnings[0].message)
	The chart shows 2 of its 3 labels so that they stay readable. Give a wider ndp.Size to show more of them.
	"""
	ordered_labels = [is_ordered_text(label_text) for label_text in label_texts]
	if all(ordered_labels):
		return

	label_count = len(label_texts)
	size_word = TALLER_SIZE if on_vertical_axis else WIDER_SIZE
	message = HIDDEN_LABELS_MESSAGE.format(shown_count=shown_count, label_count=label_count, size_word=size_word)
	warnings.warn(message, ReadabilityWarning, skip_file_prefixes=INTERNAL_FILES)


def thin_labels(axis: Axis, on_vertical_axis: bool, rotation: float) -> None:
	"""
	Keep one label out of as many as needed for the labels of an axis to stay readable, from the first one.

	The tick marks of the labels left out are removed too, so each mark left has its label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis, with labels that are not rotated yet.
	on_vertical_axis
		True for the vertical axis.
	rotation
		The angle the labels will take, in degrees.

	Warns
	-----
	ReadabilityWarning
		When a left out label may be a text.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.label_thinning import thin_labels
	>>> axes = Figure(figsize=(6.4, 4.8), dpi=100).add_subplot()
	>>> ticks = [float(tick) for tick in range(60)]
	>>> axes.xaxis.set_ticks(ticks, [str(int(tick)) for tick in ticks])  # doctest: +ELLIPSIS
	[...]
	>>> thin_labels(axes.xaxis, False, 45.0)
	>>> [label.get_text() for label in axes.get_xticklabels()][:3]
	['0', '2', '4']
	"""
	label_step = find_label_step(axis, on_vertical_axis, rotation)
	if label_step == EVERY_LABEL:
		return

	labels = axis.get_ticklabels()
	label_texts = [label.get_text() for label in labels]
	ticks = find_tick_locations(axis)
	kept_ticks = ticks[::label_step]
	kept_texts = label_texts[::label_step]
	axis.set_ticks(kept_ticks, kept_texts)
	shown_count = len(kept_texts)
	warn_hidden_labels(label_texts, shown_count, on_vertical_axis)
