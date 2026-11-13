"""
Choice of the labels of an axis that fit, the others being left out so that they stay readable.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import math
import warnings

import numpy
from matplotlib.axis import Axis
from matplotlib.ticker import FixedLocator

from numdaplot.arrays.operations.float_errors import INTERNAL_FILES
from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.labels.label_room import (
	estimate_final_length,
	find_needed_room,
	find_tick_locations,
	find_tick_room,
	read_label_texts,
)

MINIMUM_TICKS = 2
EVERY_LABEL = 1
MINUS_SIGN = "\N{MINUS SIGN}"
HYPHEN_MINUS = "-"
WIDER_SIZE = "wider"
TALLER_SIZE = "taller"
HIDDEN_LABELS_MESSAGE = (
	"The chart shows {shown_count} of its {label_count} labels so that they stay readable. "
	"Give a {size_word} ndp.Size to show more of them."
)


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
	>>> from numdaplot.plots.drawing.labels.label_thinning import find_label_step
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
	>>> from numdaplot.plots.drawing.labels.label_thinning import is_ordered_text
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
	>>> from numdaplot.plots.drawing.labels.label_thinning import warn_hidden_labels
	>>> with warnings.catch_warnings(record=True) as caught_warnings:
	... 	warnings.simplefilter("always")
	... 	warn_hidden_labels(["Paris", "Lyon", "Nice"], 2, False)
	>>> print(caught_warnings[0].message)
	The chart shows 2 of its 3 labels so that they stay readable. Give a wider ndp.Size to show more of them.
	"""
	ordered_labels = (is_ordered_text(label_text) for label_text in label_texts)
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
	>>> from numdaplot.plots.drawing.labels.label_thinning import thin_labels
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

	label_texts = read_label_texts(axis)
	ticks = find_tick_locations(axis)
	kept_ticks = ticks[::label_step]
	kept_texts = label_texts[::label_step]
	axis.set_ticks(kept_ticks, kept_texts)
	shown_count = len(kept_texts)
	warn_hidden_labels(label_texts, shown_count, on_vertical_axis)
