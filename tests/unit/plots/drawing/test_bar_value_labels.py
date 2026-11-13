"""
Unit tests of the values written on the bars of a BarChart.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.plots.charts.value_labels import ValueLabels
from numdaplot.plots.drawing.bar_value_labels import (
	LABELED_BAR_ID,
	LabelPlace,
	find_label_place,
	format_value_labels,
	write_value_labels,
)
from numdaplot.plots.drawing.text_contrast import DARK_TEXT_COLOR, LIGHT_TEXT_COLOR
from numdaplot.types.type import Type

SHARES = numpy.array([0.523, 0.18])
EXPECTED_SHARE_TEXTS = ["0.52", "0.18"]
WHOLE_COUNTS = numpy.array([120.0, 7.0])
EXPECTED_COUNT_TEXTS = ["120", "7"]
HALF_COUNTS = numpy.array([2.5])
EXPECTED_HALF_TEXTS = ["2.50"]
WHOLE_DECIMALS = numpy.array([3.0])
EXPECTED_WHOLE_DECIMAL_TEXTS = ["3.00"]
ROUNDED_SHARES = numpy.array([0.6])
EXPECTED_ROUNDED_TEXTS = ["1"]
NO_DECIMALS = ValueLabels(decimals=0)
DEFAULT_LABELS = ValueLabels()
POSITIONS = [0.0, 1.0]
LENGTHS = [0.52, 0.18]
LABEL_TEXTS = ["0.52", "0.18"]
DARK_BAR_COLOR = "#1f3a93"
LIGHT_BAR_COLOR = "#ffd966"
PLACE_CASES = [
	(False, False, LabelPlace.VERTICAL_END),
	(True, False, LabelPlace.HORIZONTAL_END),
	(False, True, LabelPlace.VERTICAL_MIDDLE),
	(True, True, LabelPlace.HORIZONTAL_MIDDLE),
]


def build_axes() -> Axes:
	"""
	Return an empty axes to draw bars on.

	.. versionadded:: 0.2.0

	Returns
	-------
	Axes
		The axes of a new figure.
	"""
	figure = Figure()
	axes = figure.add_subplot()

	return axes


@pytest.mark.parametrize(("is_horizontal", "is_stacked", "expected_place"), PLACE_CASES)
def test_find_label_place_follows_the_direction_and_the_layout(
	is_horizontal: bool, is_stacked: bool, expected_place: LabelPlace
) -> None:
	"""
	Check the place of the values for each direction and layout of the bars.

	.. versionadded:: 0.2.0

	Parameters
	----------
	is_horizontal
		True for horizontal bars.
	is_stacked
		True for stacked bars.
	expected_place
		The expected place.
	"""
	label_place = find_label_place(is_horizontal, is_stacked)

	assert label_place == expected_place


def test_format_value_labels_rounds_decimals() -> None:
	"""
	Check that decimals are rounded to the number of decimals asked.

	.. versionadded:: 0.2.0
	"""
	label_texts = format_value_labels(SHARES, DEFAULT_LABELS, Type.FLOAT64)

	assert label_texts == EXPECTED_SHARE_TEXTS


def test_format_value_labels_writes_whole_integers_without_decimals() -> None:
	"""
	Check that the whole values of integers have no decimals.

	.. versionadded:: 0.2.0
	"""
	label_texts = format_value_labels(WHOLE_COUNTS, DEFAULT_LABELS, Type.INT64)

	assert label_texts == EXPECTED_COUNT_TEXTS


def test_format_value_labels_keeps_decimals_of_a_decimal_among_integers() -> None:
	"""
	Check that a value that is not whole keeps its decimals, even when the chart holds integers.

	.. versionadded:: 0.2.0
	"""
	label_texts = format_value_labels(HALF_COUNTS, DEFAULT_LABELS, Type.INT64)

	assert label_texts == EXPECTED_HALF_TEXTS


def test_format_value_labels_keeps_decimals_of_whole_decimals() -> None:
	"""
	Check that a whole value of a decimal type keeps its decimals.

	.. versionadded:: 0.2.0
	"""
	label_texts = format_value_labels(WHOLE_DECIMALS, DEFAULT_LABELS, Type.FLOAT64)

	assert label_texts == EXPECTED_WHOLE_DECIMAL_TEXTS


def test_format_value_labels_rounds_to_whole_numbers_without_decimals() -> None:
	"""
	Check that 0 decimals rounds the values to whole numbers.

	.. versionadded:: 0.2.0
	"""
	label_texts = format_value_labels(ROUNDED_SHARES, NO_DECIMALS, Type.FLOAT64)

	assert label_texts == EXPECTED_ROUNDED_TEXTS


def test_write_value_labels_marks_the_bars_and_their_values() -> None:
	"""
	Check that each bar gets its text, both marked for the fitting after the layout.

	.. versionadded:: 0.2.0
	"""
	axes = build_axes()
	bars = axes.bar(POSITIONS, LENGTHS)

	write_value_labels(axes, bars, LABEL_TEXTS, LabelPlace.VERTICAL_END)

	texts = [text.get_text() for text in axes.texts]
	text_ids = {text.get_gid() for text in axes.texts}
	bar_ids = {bar.get_gid() for bar in bars.patches}
	assert texts == LABEL_TEXTS
	assert text_ids == {LabelPlace.VERTICAL_END.value}
	assert bar_ids == {LABELED_BAR_ID}


def test_write_value_labels_writes_white_in_the_middle_of_dark_bars() -> None:
	"""
	Check that a value in the middle of a dark bar is white.

	.. versionadded:: 0.2.0
	"""
	axes = build_axes()
	bars = axes.bar(POSITIONS, LENGTHS, color=DARK_BAR_COLOR)

	write_value_labels(axes, bars, LABEL_TEXTS, LabelPlace.VERTICAL_MIDDLE)

	text_colors = {text.get_color() for text in axes.texts}
	assert text_colors == {LIGHT_TEXT_COLOR}


def test_write_value_labels_writes_black_in_the_middle_of_light_bars() -> None:
	"""
	Check that a value in the middle of a light bar is black.

	.. versionadded:: 0.2.0
	"""
	axes = build_axes()
	bars = axes.bar(POSITIONS, LENGTHS, color=LIGHT_BAR_COLOR)

	write_value_labels(axes, bars, LABEL_TEXTS, LabelPlace.VERTICAL_MIDDLE)

	text_colors = {text.get_color() for text in axes.texts}
	assert text_colors == {DARK_TEXT_COLOR}


def test_write_value_labels_writes_nothing_without_bars() -> None:
	"""
	Check that a series without present value writes no text.

	.. versionadded:: 0.2.0
	"""
	axes = build_axes()
	bars = axes.bar([], [])

	write_value_labels(axes, bars, [], LabelPlace.VERTICAL_END)

	text_count = len(axes.texts)
	assert text_count == 0
