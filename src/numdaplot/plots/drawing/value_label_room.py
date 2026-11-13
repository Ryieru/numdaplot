"""
Room along the axis of the values for the values written past the end of bars.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from dataclasses import dataclass
from typing import cast

import numpy
from matplotlib.axes import Axes
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox
from numpy.typing import NDArray

from numdaplot.plots.drawing.bar_label_reading import BarLabel
from numdaplot.plots.drawing.bar_value_labels import BAR_LABEL_PADDING, MIDDLE_PLACES, LabelPlace

HIGHEST_ROOM_SHARE = 0.5


@dataclass(frozen=True)
class ValueLimits:
	"""
	The lowest and highest value an axis shows.

	.. versionadded:: 0.2.0

	Parameters
	----------
	lower
		The lowest value.
	upper
		The highest value.

	Examples
	--------
	>>> from numdaplot.plots.drawing.value_label_room import ValueLimits
	>>> ValueLimits(0.0, 2.0).upper
	2.0
	"""

	lower: float
	upper: float


def make_label_room(axes: Axes, bar_labels: list[BarLabel]) -> None:
	"""
	Widen the axis of the values so that every shown value past the end of a bar stays inside the axes.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bars, laid out.
	bar_labels
		The values written on its bars.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.value_label_room import make_label_room
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.barh([0.0], [-2.0])
	>>> axes.set_xlim(-2.0, 0.0)
	(-2.0, 0.0)
	>>> write_value_labels(axes, bars, ["-2.00"], LabelPlace.HORIZONTAL_END)
	>>> figure.draw_without_rendering()
	>>> make_label_room(axes, read_bar_labels(axes))
	>>> bool(axes.get_xlim()[0] < -2.0)
	True
	"""
	shown_end_labels = [
		bar_label for bar_label in bar_labels if bar_label.place not in MIDDLE_PLACES and bar_label.text.get_visible()
	]
	if not shown_end_labels:
		return

	is_horizontal = shown_end_labels[0].place == LabelPlace.HORIZONTAL_END
	value_limits = read_value_limits(axes, is_horizontal)

	for bar_label in shown_end_labels:
		value_limits = widen_for_label(axes, value_limits, bar_label)

	if is_horizontal:
		axes.set_xlim(value_limits.lower, value_limits.upper)
		return

	axes.set_ylim(value_limits.lower, value_limits.upper)


def read_value_limits(axes: Axes, is_horizontal: bool) -> ValueLimits:
	"""
	Return the lowest and highest value shown along the axis of the values.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bars.
	is_horizontal
		True for horizontal bars, whose values are along the horizontal axis.

	Returns
	-------
	ValueLimits
		The limits of the axis of the values.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.value_label_room import read_value_limits
	>>> axes = Figure().add_subplot()
	>>> axes.set_xlim(-1.0, 3.0)
	(-1.0, 3.0)
	>>> read_value_limits(axes, True)
	ValueLimits(lower=-1.0, upper=3.0)
	"""
	if is_horizontal:
		lower_x, upper_x = axes.get_xlim()
		horizontal_limits = ValueLimits(float(lower_x), float(upper_x))
		return horizontal_limits

	lower_y, upper_y = axes.get_ylim()
	vertical_limits = ValueLimits(float(lower_y), float(upper_y))

	return vertical_limits


def widen_for_label(axes: Axes, value_limits: ValueLimits, bar_label: BarLabel) -> ValueLimits:
	"""
	Return the limits of the axis of the values, widened so that a value past the end of its bar fits.

	The value keeps its size in pixels, so the axis must hold the end of the bar plus the length of the value and a
	small gap before the edge of the axes. That length counts for at most half the axis.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bar, laid out.
	value_limits
		The current limits.
	bar_label
		A value written past the end of a bar, laid out.

	Returns
	-------
	ValueLimits
		The widened limits, or the same limits when the value already fits.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.bar_value_labels import LabelPlace, write_value_labels
	>>> from numdaplot.plots.drawing.bar_label_reading import read_bar_labels
	>>> from numdaplot.plots.drawing.value_label_room import ValueLimits, widen_for_label
	>>> figure = Figure()
	>>> axes = figure.add_subplot()
	>>> bars = axes.bar([0.0], [2.0])
	>>> axes.set_ylim(0.0, 2.0)
	(0.0, 2.0)
	>>> write_value_labels(axes, bars, ["2.00"], LabelPlace.VERTICAL_END)
	>>> figure.draw_without_rendering()
	>>> widened_limits = widen_for_label(axes, ValueLimits(0.0, 2.0), read_bar_labels(axes)[0])
	>>> bool(widened_limits.upper > 2.0)
	True
	"""
	is_horizontal = bar_label.place == LabelPlace.HORIZONTAL_END
	axes_box = axes.get_window_extent()
	axis_pixels = axes_box.width if is_horizontal else axes_box.height
	text_box = bar_label.text.get_window_extent()
	anchor_value = read_anchor_value(bar_label.text, is_horizontal)
	anchor_pixel = find_anchor_pixel(axes, bar_label.text, is_horizontal)
	length_after = find_length_after(text_box, anchor_pixel, is_horizontal)
	length_before = find_length_before(text_box, anchor_pixel, is_horizontal)
	highest_length = axis_pixels * HIGHEST_ROOM_SHARE
	upper = value_limits.upper
	lower = value_limits.lower
	if length_after > 0:
		gapped_length = length_after + BAR_LABEL_PADDING
		kept_length = min(gapped_length, highest_length)
		needed_upper = lower + (anchor_value - lower) * axis_pixels / (axis_pixels - kept_length)
		upper = max(upper, needed_upper)

	if length_before > 0:
		gapped_length = length_before + BAR_LABEL_PADDING
		kept_length = min(gapped_length, highest_length)
		needed_lower = upper - (upper - anchor_value) * axis_pixels / (axis_pixels - kept_length)
		lower = min(lower, needed_lower)

	widened_limits = ValueLimits(lower, upper)

	return widened_limits


def read_anchor_value(text: Annotation, is_horizontal: bool) -> float:
	"""
	Return the value of the end of the bar a text is written from.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text
		A value written past the end of a bar.
	is_horizontal
		True for a horizontal bar, whose values are along the horizontal axis.

	Returns
	-------
	float
		The end of the bar, in the unit of the values.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.value_label_room import read_anchor_value
	>>> axes = Figure().add_subplot()
	>>> read_anchor_value(axes.annotate("2.00", (0.0, 2.0)), False)
	2.0
	"""
	anchor_x, anchor_y = text.xy
	anchor_coordinate = anchor_x if is_horizontal else anchor_y
	anchor_value = float(anchor_coordinate)

	return anchor_value


def find_anchor_pixel(axes: Axes, text: Annotation, is_horizontal: bool) -> float:
	"""
	Return where the end of the bar a text is written from lies on the figure, along the axis of the values.

	.. versionadded:: 0.2.0

	Parameters
	----------
	axes
		The matplotlib axes holding the bar.
	text
		A value written past the end of a bar, laid out.
	is_horizontal
		True for a horizontal bar.

	Returns
	-------
	float
		The position of the end of the bar, in pixels.

	Examples
	--------
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.value_label_room import find_anchor_pixel
	>>> axes = Figure().add_subplot()
	>>> axes.set_ylim(0.0, 2.0)
	(0.0, 2.0)
	>>> bool(find_anchor_pixel(axes, axes.annotate("2.00", (0.0, 2.0)), False) == axes.bbox.y1)
	True
	"""
	# Some versions of the matplotlib stubs leave the points given by transform untyped.
	anchor_point = cast(NDArray[numpy.float64], axes.transData.transform(text.xy))
	anchor_x, anchor_y = anchor_point
	anchor_coordinate = anchor_x if is_horizontal else anchor_y
	anchor_pixel = float(anchor_coordinate)

	return anchor_pixel


def find_length_after(text_box: Bbox, anchor_pixel: float, is_horizontal: bool) -> float:
	"""
	Return how far a text goes past the end of its bar toward the higher values, in pixels.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text_box
		The box of the text on the figure.
	anchor_pixel
		The end of the bar, in pixels.
	is_horizontal
		True for a horizontal bar.

	Returns
	-------
	float
		The length beyond the end of the bar, 0 when the text is on the other side.

	Examples
	--------
	>>> from matplotlib.transforms import Bbox
	>>> from numdaplot.plots.drawing.value_label_room import find_length_after
	>>> find_length_after(Bbox.from_extents(0.0, 100.0, 30.0, 112.0), 97.0, False)
	15.0
	"""
	far_edge = text_box.x1 if is_horizontal else text_box.y1
	edge_distance = float(far_edge - anchor_pixel)
	length_after = max(edge_distance, 0.0)

	return length_after


def find_length_before(text_box: Bbox, anchor_pixel: float, is_horizontal: bool) -> float:
	"""
	Return how far a text goes past the end of its bar toward the lower values, in pixels.

	.. versionadded:: 0.2.0

	Parameters
	----------
	text_box
		The box of the text on the figure.
	anchor_pixel
		The end of the bar, in pixels.
	is_horizontal
		True for a horizontal bar.

	Returns
	-------
	float
		The length beyond the end of the bar, 0 when the text is on the other side.

	Examples
	--------
	>>> from matplotlib.transforms import Bbox
	>>> from numdaplot.plots.drawing.value_label_room import find_length_before
	>>> find_length_before(Bbox.from_extents(0.0, 80.0, 30.0, 92.0), 95.0, False)
	15.0
	"""
	near_edge = text_box.x0 if is_horizontal else text_box.y0
	edge_distance = float(anchor_pixel - near_edge)
	length_before = max(edge_distance, 0.0)

	return length_before
