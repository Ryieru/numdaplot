"""
Room between the labels of an axis, and the room these labels need.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import heapq
import math
from typing import cast

import numpy
from matplotlib.axis import Axis
from matplotlib.figure import Figure, SubFigure
from matplotlib.ticker import FixedFormatter
from numpy.typing import NDArray

MEASURED_LABEL_COUNT = 200
LABEL_GAP_RATIO = 0.5
POINTS_PER_INCH = 72.0
RIGHT_ANGLE = 90.0
# What the layout usually leaves around the axes for the numbers and the name of the other axis.
LAYOUT_MARGIN_PIXELS = 60.0


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
	>>> from numdaplot.plots.drawing.labels.label_room import find_tick_locations
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 2.0])  # doctest: +ELLIPSIS
	[...]
	>>> find_tick_locations(axes.xaxis)
	array([0., 2.])
	"""
	tick_locations = numpy.asarray(axis.get_ticklocs(), dtype=numpy.float64)

	return tick_locations


def read_label_texts(axis: Axis) -> list[str]:
	"""
	Return the text of each label of an axis, without creating the ticks of labels placed by ``set_fixed_labels``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		The axis.

	Returns
	-------
	list[str]
		One text per label.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.labels.label_room import read_label_texts
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 1.0], ["Paris", "Lyon"])  # doctest: +ELLIPSIS
	[...]
	>>> read_label_texts(axes.xaxis)
	['Paris', 'Lyon']
	"""
	formatter = axis.get_major_formatter()
	if isinstance(formatter, FixedFormatter):
		fixed_texts = list(formatter.seq)
		return fixed_texts

	labels = axis.get_ticklabels()
	label_texts = [label.get_text() for label in labels]

	return label_texts


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
	>>> from numdaplot.plots.drawing.labels.label_room import find_current_length
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
	>>> from numdaplot.plots.drawing.labels.label_room import estimate_final_length
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
	>>> from numdaplot.plots.drawing.labels.label_room import find_tick_room
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
	>>> from numdaplot.plots.drawing.labels.label_room import find_font_pixels
	>>> axes = Figure(dpi=72).add_subplot()
	>>> axes.tick_params(labelsize=12.0)
	>>> find_font_pixels(axes.xaxis)
	12.0
	"""
	first_tick = axis.get_major_ticks(1)[0]
	font_size = cast(float, first_tick.label1.get_fontsize())
	figure = cast(Figure, axis.axes.get_figure(root=True))
	font_pixels = font_size * figure.dpi / POINTS_PER_INCH

	return font_pixels


def find_widest_label(axis: Axis) -> float:
	"""
	Return the width of the widest label of an axis, as written horizontally.

	Measuring a text is slow, so only the labels with the most characters are measured, the widest one being among
	them in practice.

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
	>>> from numdaplot.plots.drawing.labels.label_room import find_widest_label
	>>> axes = Figure().add_subplot()
	>>> axes.xaxis.set_ticks([0.0, 1.0], ["a", "a long label"])  # doctest: +ELLIPSIS
	[...]
	>>> bool(find_widest_label(axes.xaxis) > 50.0)
	True
	"""
	label_texts = read_label_texts(axis)
	measured_texts = heapq.nlargest(MEASURED_LABEL_COUNT, label_texts, key=len)
	measuring_label = axis.get_major_ticks(1)[0].label1
	first_text = measuring_label.get_text()
	label_widths = list[float]()

	for measured_text in measured_texts:
		measuring_label.set_text(measured_text)
		label_box = measuring_label.get_window_extent()
		label_widths.append(label_box.width)

	measuring_label.set_text(first_text)
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
	>>> from numdaplot.plots.drawing.labels.label_room import find_needed_room
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
