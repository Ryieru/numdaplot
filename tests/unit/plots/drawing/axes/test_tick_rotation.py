"""
Unit tests of the rotation of the labels of the ``x`` values.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pytest
from matplotlib.axes import Axes
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from matplotlib.figure import Figure

from numdaplot.plots.drawing.axes.grid_axes import GridAxes
from numdaplot.plots.drawing.axes.tick_rotation import (
	apply_rotation,
	choose_alignment,
	choose_rotation,
	do_labels_touch,
	has_text_labels,
	is_number_text,
	rotate_x_labels,
	rotate_y_labels,
)
from numdaplot.plots.drawing.drawn_chart import DrawnChart

HORIZONTAL_CHART = DrawnChart(None, None, False, GridAxes.NONE, None)
VERTICAL_CHART = DrawnChart(None, None, True, GridAxes.NONE, None)
TICKS = [0.0, 1.0]
TEXT_LABELS = ["Paris", "Lyon"]
NUMBER_LABELS = ["2025", "2026"]
CHOSEN_ROTATION = 30.0
NEGATIVE_ROTATION = -30.0
TEXT_ROTATION = 45.0
NO_ROTATION = 0.0
NUMBER_TEXTS = ["2025", "-1.5", "\N{MINUS SIGN}1.5", ""]
OTHER_TEXTS = ["Paris", "2026-01-01", "12 h"]
ALIGNMENTS = [(45.0, "right"), (-45.0, "left"), (0.0, "center")]
FIRST_DAY = numpy.datetime64("2026-01-01")
LAST_DAY = numpy.datetime64("2026-12-31")


def build_axes(labels: list[str]) -> Axes:
	"""
	Return matplotlib axes with labels on the ticks of their horizontal axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	labels
		The labels of the ticks.

	Returns
	-------
	Axes
		The axes.
	"""
	axes = Figure().add_subplot()
	axes.xaxis.set_ticks(TICKS, labels)

	return axes


def build_date_axes() -> Axes:
	"""
	Return matplotlib axes with a time axis, as numdaplot places moments.

	.. versionadded:: 0.1.0

	Returns
	-------
	Axes
		The axes.
	"""
	axes = Figure().add_subplot()
	axes.plot([FIRST_DAY, LAST_DAY], TICKS)
	date_locator = AutoDateLocator()
	date_formatter = ConciseDateFormatter(date_locator)
	axes.xaxis.set_major_locator(date_locator)
	axes.xaxis.set_major_formatter(date_formatter)

	return axes


def test_rotate_x_labels_tilts_texts_by_default() -> None:
	"""
	Check that texts are at 45 degrees, their end under their tick.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(TEXT_LABELS)

	rotate_x_labels(axes, HORIZONTAL_CHART, None)

	label = axes.get_xticklabels()[0]
	assert label.get_rotation() == TEXT_ROTATION
	assert label.get_horizontalalignment() == "right"


def test_rotate_x_labels_keeps_numbers_flat_by_default() -> None:
	"""
	Check that numbers written as texts stay horizontal.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(NUMBER_LABELS)

	rotate_x_labels(axes, HORIZONTAL_CHART, None)

	label = axes.get_xticklabels()[0]
	assert label.get_rotation() == NO_ROTATION
	assert label.get_horizontalalignment() == "center"


def test_rotate_x_labels_follows_the_chosen_rotation() -> None:
	"""
	Check that a chosen angle also applies to numbers.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(NUMBER_LABELS)

	rotate_x_labels(axes, HORIZONTAL_CHART, CHOSEN_ROTATION)

	assert axes.get_xticklabels()[0].get_rotation() == CHOSEN_ROTATION


def test_rotate_x_labels_accepts_no_rotation_for_texts() -> None:
	"""
	Check that 0 keeps texts horizontal, centered under their tick.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(TEXT_LABELS)

	rotate_x_labels(axes, HORIZONTAL_CHART, NO_ROTATION)

	assert axes.get_xticklabels()[0].get_rotation() == NO_ROTATION


def test_rotate_x_labels_keeps_vertical_labels_flat_by_default() -> None:
	"""
	Check that the labels of horizontal bars stay horizontal.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.yaxis.set_ticks(TICKS, TEXT_LABELS)

	rotate_x_labels(axes, VERTICAL_CHART, None)

	assert axes.get_yticklabels()[0].get_rotation() == NO_ROTATION


def test_rotate_x_labels_rotates_vertical_labels_when_chosen() -> None:
	"""
	Check that a chosen angle follows the ``x`` values on the vertical axis.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.yaxis.set_ticks(TICKS, TEXT_LABELS)

	rotate_x_labels(axes, VERTICAL_CHART, CHOSEN_ROTATION)

	assert axes.get_yticklabels()[0].get_rotation() == CHOSEN_ROTATION
	assert axes.get_xticklabels()[0].get_rotation() == NO_ROTATION


def test_rotate_x_labels_applies_to_every_tick_of_a_time_axis() -> None:
	"""
	Check that all the labels of a time axis are rotated.

	.. versionadded:: 0.1.0
	"""
	axes = build_date_axes()

	rotate_x_labels(axes, HORIZONTAL_CHART, None)

	rotations = {label.get_rotation() for label in axes.get_xticklabels()}
	assert rotations == {TEXT_ROTATION}


def test_choose_rotation_prefers_the_chosen_angle() -> None:
	"""
	Check an angle chosen for texts.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(TEXT_LABELS)

	rotation = choose_rotation(axes.xaxis, NEGATIVE_ROTATION)

	assert rotation == NEGATIVE_ROTATION


def test_has_text_labels_finds_texts() -> None:
	"""
	Check labels that are not numbers.

	.. versionadded:: 0.1.0
	"""
	axes = build_axes(TEXT_LABELS)

	assert has_text_labels(axes.xaxis)


def test_has_text_labels_refuses_a_number_axis() -> None:
	"""
	Check the default axis of matplotlib, holding numbers.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	assert not has_text_labels(axes.xaxis)


def test_has_text_labels_finds_a_time_axis() -> None:
	"""
	Check that moments count as texts.

	.. versionadded:: 0.1.0
	"""
	axes = build_date_axes()

	assert has_text_labels(axes.xaxis)


@pytest.mark.parametrize("text", NUMBER_TEXTS)
def test_is_number_text_accepts_numbers(text: str) -> None:
	"""
	Check numbers, the minus sign of matplotlib and an empty label.

	.. versionadded:: 0.1.0
	"""
	assert is_number_text(text)


@pytest.mark.parametrize("text", OTHER_TEXTS)
def test_is_number_text_refuses_other_texts(text: str) -> None:
	"""
	Check texts that are not numbers.

	.. versionadded:: 0.1.0
	"""
	assert not is_number_text(text)


@pytest.mark.parametrize(("rotation", "expected_alignment"), ALIGNMENTS)
def test_choose_alignment_follows_the_sign_of_the_angle(rotation: float, expected_alignment: str) -> None:
	"""
	Check a positive angle, a negative one and no rotation.

	.. versionadded:: 0.1.0
	"""
	alignment = choose_alignment(rotation)

	assert alignment == expected_alignment


def test_rotate_y_labels_keeps_the_labels_by_default() -> None:
	"""
	Check that the labels of the values stay horizontal without a chosen angle.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	rotate_y_labels(axes, HORIZONTAL_CHART, None)

	assert axes.get_yticklabels()[0].get_rotation() == NO_ROTATION


def test_rotate_y_labels_rotates_the_vertical_axis() -> None:
	"""
	Check that a chosen angle applies to the vertical axis of a chart with vertical values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	rotate_y_labels(axes, HORIZONTAL_CHART, CHOSEN_ROTATION)

	assert axes.get_yticklabels()[0].get_rotation() == CHOSEN_ROTATION
	assert axes.get_xticklabels()[0].get_rotation() == NO_ROTATION


def test_rotate_y_labels_rotates_the_values_of_horizontal_bars() -> None:
	"""
	Check that a chosen angle follows the ``y`` values on the horizontal axis.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	rotate_y_labels(axes, VERTICAL_CHART, CHOSEN_ROTATION)

	label = axes.get_xticklabels()[0]
	assert label.get_rotation() == CHOSEN_ROTATION
	assert label.get_horizontalalignment() == "right"
	assert axes.get_yticklabels()[0].get_rotation() == NO_ROTATION


def test_apply_rotation_leaves_the_alignment_of_a_vertical_axis() -> None:
	"""
	Check that the labels of a vertical axis still end at their tick.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	apply_rotation(axes, True, NEGATIVE_ROTATION)

	assert axes.get_yticklabels()[0].get_horizontalalignment() == "right"


def test_do_labels_touch_refuses_scalar_labels() -> None:
	"""
	Check that labels chosen by matplotlib never touch.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	labels_touch = do_labels_touch(axes.xaxis)

	assert not labels_touch


def test_do_labels_touch_ignores_a_single_label() -> None:
	"""
	Check that a single label has nothing to touch.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.xaxis.set_ticks([0.0], ["1000000"])

	labels_touch = do_labels_touch(axes.xaxis)

	assert not labels_touch


def test_do_labels_touch_finds_wide_labels_on_close_ticks() -> None:
	"""
	Check that many wide labels touch.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	tick_positions = [float(position) for position in range(30)]
	tick_labels = [str(1000000 + position) for position in range(30)]
	axes.xaxis.set_ticks(tick_positions, tick_labels)

	labels_touch = do_labels_touch(axes.xaxis)

	assert labels_touch


def test_do_labels_touch_leaves_short_labels_on_distant_ticks() -> None:
	"""
	Check that few short labels have room.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.xaxis.set_ticks([0.0, 1.0, 2.0], ["1", "2", "3"])

	labels_touch = do_labels_touch(axes.xaxis)

	assert not labels_touch


def test_do_labels_touch_uses_the_closest_ticks() -> None:
	"""
	Check that two close ticks are enough for labels to touch.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.xaxis.set_ticks([0.0, 0.001, 100.0], ["2000", "2001", "2002"])

	labels_touch = do_labels_touch(axes.xaxis)

	assert labels_touch
