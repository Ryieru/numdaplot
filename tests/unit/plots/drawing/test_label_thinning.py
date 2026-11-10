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
	find_label_step,
	is_ordered_text,
	thin_labels,
	warn_hidden_labels,
)

WIDTH_INCHES = 6.4
HEIGHT_INCHES = 4.8
DPI = 100
SLANTED = 45.0
MANY_TICKS = 60
FEW_TICKS = 5
STACKED_TICK = 1.0
STACKED_TEXTS = ["a", "b", "c", "d", "e"]
STEP_AT_45 = 2
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


def test_find_label_step_keeps_every_label_of_ticks_at_the_same_place() -> None:
	"""
	Check that ticks without any gap between them leave every label.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	stacked_ticks = [STACKED_TICK] * FEW_TICKS
	axes.xaxis.set_ticks(stacked_ticks, STACKED_TEXTS)

	label_step = find_label_step(axes.xaxis, False, SLANTED)

	assert label_step == 1
