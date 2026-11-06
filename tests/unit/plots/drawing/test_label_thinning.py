"""
Unit tests of the choice of the labels of an axis that fit.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings

import pytest
from matplotlib.axes import Axes
from matplotlib.dates import AutoDateLocator
from matplotlib.figure import Figure

from numdaplot.errors.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.label_thinning import (
	LAYOUT_MARGIN_PIXELS,
	estimate_final_length,
	find_current_length,
	find_font_pixels,
	find_label_step,
	find_needed_room,
	find_tick_locations,
	find_tick_room,
	find_widest_label,
	is_ordered_text,
	thin_labels,
	warn_hidden_labels,
)

WIDTH_INCHES = 6.4
HEIGHT_INCHES = 4.8
TINY_INCHES = 0.5
DPI = 100
EXPECTED_WIDTH = 640.0
EXPECTED_HEIGHT = 480.0
FONT_POINTS = 10.0
POINTS_DPI = 72
SIDE_BY_SIDE_AT_45 = 14.142
SIDE_BY_SIDE_TOLERANCE = 0.01
RIGHT_ANGLE = 90.0
SLANTED = 45.0
FLAT = 0.0
MANY_TICKS = 60
FEW_TICKS = 5
STEP_AT_45 = 2
LONG_LABEL = "a very long label of the axis"
SHORT_LABEL = "a"
AXES_LENGTH = 500.0
EXPECTED_ROOM = 50.0
VIEW_STOP = 10.0
TEXTS = ["Paris", "Lyon", "Nice"]
ORDERED_TEXTS = ["2025", "\N{MINUS SIGN}1.5", "2026-01-31", "2026-01-31 10:00:00", ""]
OTHER_TEXTS = ["Paris", "Z001", "12 h"]
EXPECTED_MESSAGE = (
	"The chart shows 2 of its 3 labels so that they stay readable. Give a wider ndp.Size to show more of them."
)
EXPECTED_TALL_MESSAGE = (
	"The chart shows 2 of its 3 labels so that they stay readable. Give a taller ndp.Size to show more of them."
)


def build_axes(tick_count: int) -> Axes:
	"""
	Return axes with text labels fixed on the horizontal and the vertical axes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tick_count
		The number of ticks of each axis.

	Returns
	-------
	Axes
		The axes.
	"""
	figure = Figure(figsize=(WIDTH_INCHES, HEIGHT_INCHES), dpi=DPI)
	axes = figure.add_subplot()
	ticks = [float(tick) for tick in range(tick_count)]
	labels = [f"Z{tick:03d}" for tick in range(tick_count)]
	axes.xaxis.set_ticks(ticks, labels)
	axes.yaxis.set_ticks(ticks, labels)

	return axes


def read_labels(axes: Axes) -> list[str]:
	"""
	Return the labels of the horizontal axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axes
		The axes.

	Returns
	-------
	list[str]
		The texts.
	"""
	labels = axes.get_xticklabels()
	texts = [label.get_text() for label in labels]

	return texts


def test_estimate_final_length_removes_the_margin_of_the_layout() -> None:
	"""
	Check the width expected once the layout has given the axes their room.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(FEW_TICKS)

	final_length = estimate_final_length(axes.xaxis, False)

	assert final_length == EXPECTED_WIDTH - LAYOUT_MARGIN_PIXELS


def test_estimate_final_length_reads_the_height_for_the_vertical_axis() -> None:
	"""
	Check the height expected on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(FEW_TICKS)

	final_length = estimate_final_length(axes.yaxis, True)

	assert final_length == EXPECTED_HEIGHT - LAYOUT_MARGIN_PIXELS


def test_estimate_final_length_keeps_at_least_the_current_length() -> None:
	"""
	Check a figure smaller than the usual margin.

	.. versionadded:: 0.1.0
	"""
	figure = Figure(figsize=(TINY_INCHES, TINY_INCHES), dpi=DPI)
	axes = figure.add_subplot()
	current_length = find_current_length(axes.xaxis, False)

	final_length = estimate_final_length(axes.xaxis, False)

	assert final_length == current_length


def test_find_tick_room_uses_the_closest_ticks() -> None:
	"""
	Check uneven ticks.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	axes.set_xlim(0.0, VIEW_STOP)
	axes.xaxis.set_ticks([0.0, 1.0, 3.0], TEXTS)

	room = find_tick_room(axes.xaxis, False, AXES_LENGTH)

	assert room == EXPECTED_ROOM


def test_find_font_pixels_follows_the_resolution() -> None:
	"""
	Check a font size given in points.

	.. versionadded:: 0.1.0
	"""
	figure = Figure(dpi=POINTS_DPI)
	axes = figure.add_subplot()
	axes.tick_params(labelsize=FONT_POINTS)

	font_pixels = find_font_pixels(axes.xaxis)

	assert font_pixels == FONT_POINTS


def test_find_widest_label_measures_the_longest_text() -> None:
	"""
	Check that the longest label gives the width.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	short_axes = figure.add_subplot()
	short_axes.xaxis.set_ticks([0.0, 1.0], [SHORT_LABEL, SHORT_LABEL])
	short_width = find_widest_label(short_axes.xaxis)
	short_axes.xaxis.set_ticks([0.0, 1.0], [SHORT_LABEL, LONG_LABEL])

	long_width = find_widest_label(short_axes.xaxis)

	assert long_width > short_width


def build_font_axes() -> Axes:
	"""
	Return axes whose labels have a font of 10 pixels, with a long label.

	.. versionadded:: 0.1.0

	Returns
	-------
	Axes
		The axes.
	"""
	figure = Figure(dpi=POINTS_DPI)
	axes = figure.add_subplot()
	axes.tick_params(labelsize=FONT_POINTS)
	axes.xaxis.set_ticks([0.0, 1.0], [SHORT_LABEL, LONG_LABEL])
	axes.yaxis.set_ticks([0.0, 1.0], [SHORT_LABEL, LONG_LABEL])

	return axes


def test_find_needed_room_is_the_width_along_the_axis() -> None:
	"""
	Check flat labels on the horizontal axis: their width and half their font size.

	.. versionadded:: 0.1.0
	"""
	axes = build_font_axes()
	widest_label = find_widest_label(axes.xaxis)

	needed_room = find_needed_room(axes.xaxis, False, FLAT)

	assert needed_room == widest_label + FONT_POINTS / 2


def test_find_needed_room_is_the_font_size_across_the_axis() -> None:
	"""
	Check labels perpendicular to the axis: flat on the vertical one, at 90 degrees on the horizontal one.

	.. versionadded:: 0.1.0
	"""
	axes = build_font_axes()

	flat_room = find_needed_room(axes.yaxis, True, FLAT)
	upright_room = find_needed_room(axes.xaxis, False, RIGHT_ANGLE)

	assert flat_room == FONT_POINTS
	assert upright_room == FONT_POINTS


def test_find_needed_room_grows_when_slanted_labels_lean_on_each_other() -> None:
	"""
	Check long labels at 45 degrees, on both signs of the angle.

	.. versionadded:: 0.1.0
	"""
	axes = build_font_axes()

	positive_room = find_needed_room(axes.xaxis, False, SLANTED)
	negative_room = find_needed_room(axes.xaxis, False, -SLANTED)

	assert abs(positive_room - SIDE_BY_SIDE_AT_45) < SIDE_BY_SIDE_TOLERANCE
	assert negative_room == positive_room


def test_find_needed_room_stops_at_the_whole_label() -> None:
	"""
	Check a short label barely slanted, which needs less than two slanted lines side by side.

	.. versionadded:: 0.1.0
	"""
	figure = Figure(dpi=POINTS_DPI)
	axes = figure.add_subplot()
	axes.tick_params(labelsize=FONT_POINTS)
	axes.xaxis.set_ticks([0.0, 1.0], [SHORT_LABEL, SHORT_LABEL])
	widest_label = find_widest_label(axes.xaxis)

	needed_room = find_needed_room(axes.xaxis, False, 1.0)

	assert needed_room < widest_label + FONT_POINTS


def test_find_label_step_keeps_each_label_with_enough_room() -> None:
	"""
	Check a few ticks.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(FEW_TICKS)

	label_step = find_label_step(axes.xaxis, False, SLANTED)

	assert label_step == 1


def test_find_label_step_grows_with_the_ticks() -> None:
	"""
	Check many ticks at 45 degrees.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(MANY_TICKS)

	label_step = find_label_step(axes.xaxis, False, SLANTED)

	assert label_step == STEP_AT_45


def test_find_label_step_leaves_labels_chosen_by_matplotlib() -> None:
	"""
	Check an axis whose ticks are not fixed on each value.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	locator = AutoDateLocator()
	axes.xaxis.set_major_locator(locator)

	label_step = find_label_step(axes.xaxis, False, SLANTED)

	assert label_step == 1


def test_find_label_step_leaves_a_single_tick() -> None:
	"""
	Check an axis without room to compute.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(1)

	label_step = find_label_step(axes.xaxis, False, SLANTED)

	assert label_step == 1


@pytest.mark.parametrize("text", ORDERED_TEXTS)
def test_is_ordered_text_accepts_numbers_and_dates(text: str) -> None:
	"""
	Check labels a reader can find from their neighbors.

	.. versionadded:: 0.1.0
	"""
	is_ordered = is_ordered_text(text)

	assert is_ordered is True


@pytest.mark.parametrize("text", OTHER_TEXTS)
def test_is_ordered_text_refuses_other_texts(text: str) -> None:
	"""
	Check labels naming their values.

	.. versionadded:: 0.1.0
	"""
	is_ordered = is_ordered_text(text)

	assert is_ordered is False


def test_warn_hidden_labels_names_the_counts_and_the_wider_size() -> None:
	"""
	Check the message on the horizontal axis.

	.. versionadded:: 0.1.0
	"""
	with pytest.warns(ReadabilityWarning) as caught_warnings:
		warn_hidden_labels(TEXTS, 2, False)

	warning_text = str(caught_warnings[0].message)
	assert warning_text == EXPECTED_MESSAGE


def test_warn_hidden_labels_asks_for_a_taller_size_on_the_vertical_axis() -> None:
	"""
	Check the message on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	with pytest.warns(ReadabilityWarning) as caught_warnings:
		warn_hidden_labels(TEXTS, 2, True)

	warning_text = str(caught_warnings[0].message)
	assert warning_text == EXPECTED_TALL_MESSAGE


def test_warn_hidden_labels_stays_silent_for_numbers_and_dates() -> None:
	"""
	Check labels a reader can find from their neighbors.

	.. versionadded:: 0.1.0
	"""
	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		warn_hidden_labels(ORDERED_TEXTS, 2, False)

	assert caught_warnings == []


def test_thin_labels_keeps_one_label_out_of_the_step_from_the_first() -> None:
	"""
	Check the labels kept.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(MANY_TICKS)

	with pytest.warns(ReadabilityWarning):
		thin_labels(axes.xaxis, False, SLANTED)

	labels = read_labels(axes)
	assert labels[:2] == ["Z000", "Z002"]


def test_thin_labels_removes_the_marks_of_the_labels_left_out() -> None:
	"""
	Check that each mark left has its label, at the coordinate of its value.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(MANY_TICKS)

	with pytest.warns(ReadabilityWarning):
		thin_labels(axes.xaxis, False, SLANTED)

	tick_list = axes.get_xticks().tolist()
	assert tick_list[:2] == [0.0, 2.0]


def test_thin_labels_leaves_labels_with_enough_room() -> None:
	"""
	Check a few labels: nothing is left out and nothing warns.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(FEW_TICKS)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		thin_labels(axes.xaxis, False, SLANTED)

	labels = read_labels(axes)
	assert len(labels) == FEW_TICKS
	assert caught_warnings == []


def test_find_tick_locations_gives_each_tick() -> None:
	"""
	Check the coordinates of the ticks.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(2)

	tick_locations = find_tick_locations(axes.xaxis)

	location_list = tick_locations.tolist()
	assert location_list == [0.0, 1.0]
