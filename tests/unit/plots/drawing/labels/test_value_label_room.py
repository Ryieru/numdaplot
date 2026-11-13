"""
Unit tests of the room along the axis of the values for the values written past the end of bars.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
from numdaplot.plots.drawing.labels.value_label_room import (
	HIGHEST_ROOM_SHARE,
	ValueLimits,
	find_anchor_pixel,
	find_length_after,
	find_length_before,
	make_label_room,
	read_anchor_value,
	read_value_limits,
	widen_for_label,
)

SMALL_FIGURE_SIZE = (2.0, 2.0)
TWO_POSITIONS = [0.0, 1.0]
TWO_LENGTHS = [1.0, 2.0]
TWO_TEXTS = ["1.00", "2.00"]
LOWER_LIMIT = 0.0
UPPER_LIMIT = 2.0
NEGATIVE_LENGTH = -2.0
NEGATIVE_TEXT = "-2.00"
TALL_TEXT = "1.00"
ANCHOR_VALUE = 2.0
ANCHOR_POINT = (0.0, ANCHOR_VALUE)
HORIZONTAL_ANCHOR_POINT = (ANCHOR_VALUE, 0.0)
TEXT_BOX_ABOVE = Bbox.from_extents(0.0, 100.0, 30.0, 112.0)
TEXT_BOX_BELOW = Bbox.from_extents(0.0, 80.0, 30.0, 92.0)
ANCHOR_BELOW_TEXT = 97.0
ANCHOR_ABOVE_TEXT = 95.0
EXPECTED_LENGTH = 15.0
TEXT_BOX_RIGHT = Bbox.from_extents(100.0, 0.0, 130.0, 12.0)
ANCHOR_LEFT_OF_TEXT = 97.0
EXPECTED_HORIZONTAL_LENGTH = 33.0
LIMIT_TOLERANCE = 1e-9
LONG_TEXT = "1234567890.123456"


def build_figure(figure_size: tuple[float, float] | None = None) -> tuple[Figure, Axes]:
	"""
	Return a figure and its axes, to draw bars on.

	.. versionadded:: 0.2.0

	Parameters
	----------
	figure_size
		The size of the figure in inches, the matplotlib default when omitted.

	Returns
	-------
	tuple[Figure, Axes]
		The figure and its single axes.
	"""
	figure = Figure(figsize=figure_size)
	axes = figure.add_subplot()

	return figure, axes


def test_make_label_room_raises_the_top_above_vertical_bars() -> None:
	"""
	Check that the top of the axis rises so that the value of the highest bar stays inside the axes.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	axes.set_ylim(LOWER_LIMIT, UPPER_LIMIT)
	write_value_labels(axes, bars, TWO_TEXTS, LabelPlace.VERTICAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	make_label_room(axes, bar_labels)

	figure.draw_without_rendering()
	highest_text = axes.texts[1]
	text_box = highest_text.get_window_extent()
	assert text_box.y1 <= axes.bbox.y1


def test_make_label_room_lowers_the_left_of_negative_horizontal_bars() -> None:
	"""
	Check that the left of the axis goes lower so that the value of a negative horizontal bar stays inside the axes.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.barh([0.0], [NEGATIVE_LENGTH])
	axes.set_xlim(NEGATIVE_LENGTH, LOWER_LIMIT)
	write_value_labels(axes, bars, [NEGATIVE_TEXT], LabelPlace.HORIZONTAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	make_label_room(axes, bar_labels)

	figure.draw_without_rendering()
	text_box = axes.texts[0].get_window_extent()
	assert text_box.x0 >= axes.bbox.x0


def test_make_label_room_ignores_middle_and_hidden_values() -> None:
	"""
	Check that values in the middle of bars or hidden leave the axis unchanged.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	axes.set_ylim(LOWER_LIMIT, UPPER_LIMIT)
	write_value_labels(axes, bars, TWO_TEXTS, LabelPlace.VERTICAL_MIDDLE)
	other_bars = axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	write_value_labels(axes, other_bars, TWO_TEXTS, LabelPlace.VERTICAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)
	for bar_label in bar_labels:
		bar_label.text.set_visible(bar_label.place == LabelPlace.VERTICAL_MIDDLE)

	make_label_room(axes, bar_labels)

	limits = axes.get_ylim()
	assert limits == (LOWER_LIMIT, UPPER_LIMIT)


def test_read_value_limits_reads_the_vertical_axis_of_vertical_bars() -> None:
	"""
	Check that vertical bars read the limits of the vertical axis.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_figure()
	axes.set_ylim(LOWER_LIMIT, UPPER_LIMIT)

	value_limits = read_value_limits(axes, False)

	assert value_limits == ValueLimits(LOWER_LIMIT, UPPER_LIMIT)


def test_widen_for_label_gives_the_label_at_most_half_the_axis() -> None:
	"""
	Check that a value longer than half the axis widens the axis only as much as half of it.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure(SMALL_FIGURE_SIZE)
	bars = axes.barh([0.0], [UPPER_LIMIT])
	axes.set_xlim(LOWER_LIMIT, UPPER_LIMIT)
	write_value_labels(axes, bars, [LONG_TEXT], LabelPlace.HORIZONTAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)
	bar_label = bar_labels[0]

	widened_limits = widen_for_label(axes, ValueLimits(LOWER_LIMIT, UPPER_LIMIT), bar_label)

	kept_share = 1 - HIGHEST_ROOM_SHARE
	highest_upper = UPPER_LIMIT / kept_share
	upper_gap = abs(widened_limits.upper - highest_upper)
	assert upper_gap < LIMIT_TOLERANCE


def test_read_anchor_value_reads_the_end_of_a_horizontal_bar() -> None:
	"""
	Check that a horizontal bar ends at the horizontal coordinate of the text anchor.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_figure()
	text = axes.annotate(TALL_TEXT, HORIZONTAL_ANCHOR_POINT)

	anchor_value = read_anchor_value(text, True)

	assert anchor_value == ANCHOR_VALUE


def test_find_anchor_pixel_places_the_top_of_the_axis_at_the_top_of_the_axes() -> None:
	"""
	Check that an anchor at the top limit lies at the top of the axes.

	.. versionadded:: 0.2.0
	"""
	_, axes = build_figure()
	axes.set_ylim(LOWER_LIMIT, UPPER_LIMIT)
	text = axes.annotate(TALL_TEXT, ANCHOR_POINT)

	anchor_pixel = find_anchor_pixel(axes, text, False)

	assert anchor_pixel == axes.bbox.y1


def test_find_length_after_measures_a_text_above_its_anchor() -> None:
	"""
	Check the length of a text past its anchor toward the higher values.

	.. versionadded:: 0.2.0
	"""
	length_after = find_length_after(TEXT_BOX_ABOVE, ANCHOR_BELOW_TEXT, False)

	assert length_after == EXPECTED_LENGTH


def test_find_length_after_measures_a_text_right_of_its_anchor() -> None:
	"""
	Check the length of a text past its anchor along a horizontal axis.

	.. versionadded:: 0.2.0
	"""
	length_after = find_length_after(TEXT_BOX_RIGHT, ANCHOR_LEFT_OF_TEXT, True)

	assert length_after == EXPECTED_HORIZONTAL_LENGTH


def test_find_length_after_is_zero_for_a_text_below_its_anchor() -> None:
	"""
	Check that a text on the lower side has no length toward the higher values.

	.. versionadded:: 0.2.0
	"""
	length_after = find_length_after(TEXT_BOX_BELOW, ANCHOR_ABOVE_TEXT, False)

	assert length_after == 0.0


def test_find_length_before_measures_a_text_below_its_anchor() -> None:
	"""
	Check the length of a text past its anchor toward the lower values.

	.. versionadded:: 0.2.0
	"""
	length_before = find_length_before(TEXT_BOX_BELOW, ANCHOR_ABOVE_TEXT, False)

	assert length_before == EXPECTED_LENGTH
