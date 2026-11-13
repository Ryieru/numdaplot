"""
Unit tests of the room between the labels of an axis.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.plots.drawing.axes.position_axis import set_fixed_labels
from numdaplot.plots.drawing.labels.label_room import (
	LAYOUT_MARGIN_PIXELS,
	estimate_final_length,
	find_current_length,
	find_font_pixels,
	find_needed_room,
	find_tick_locations,
	find_tick_room,
	find_widest_label,
	read_label_texts,
)

MANY_LABEL_COUNT = 500
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
FEW_TICKS = 5
LONG_LABEL = "a very long label of the axis"
SHORT_LABEL = "a"
AXES_LENGTH = 500.0
EXPECTED_ROOM = 50.0
VIEW_STOP = 10.0
TEXTS = ["Paris", "Lyon", "Nice"]


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


def test_find_tick_locations_gives_each_tick() -> None:
	"""
	Check the coordinates of the ticks.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(2)

	tick_locations = find_tick_locations(axes.xaxis)

	location_list = tick_locations.tolist()
	assert location_list == [0.0, 1.0]


def test_read_label_texts_reads_fixed_labels_without_creating_their_ticks() -> None:
	"""
	Check that reading labels placed by set_fixed_labels leaves their ticks uncreated.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	coordinates = numpy.arange(MANY_LABEL_COUNT, dtype=numpy.float64)
	labels = [str(i) for i in range(MANY_LABEL_COUNT)]
	set_fixed_labels(axes.xaxis, coordinates, labels)

	label_texts = read_label_texts(axes.xaxis)

	tick_count = len(axes.xaxis.get_major_ticks(1))
	assert label_texts == labels
	assert tick_count == 1


def test_find_widest_label_measures_the_longest_label_among_many() -> None:
	"""
	Check that the widest label is found among more labels than are measured.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	coordinates = numpy.arange(MANY_LABEL_COUNT, dtype=numpy.float64)
	labels = [SHORT_LABEL] * MANY_LABEL_COUNT
	labels[-1] = LONG_LABEL
	set_fixed_labels(axes.xaxis, coordinates, labels)
	axes_with_long_label = Figure().add_subplot()
	axes_with_long_label.xaxis.set_ticks([0.0], [LONG_LABEL])

	widest_label = find_widest_label(axes.xaxis)

	assert widest_label == find_widest_label(axes_with_long_label.xaxis)
