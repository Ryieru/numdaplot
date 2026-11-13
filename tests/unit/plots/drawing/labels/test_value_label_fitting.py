"""
Unit tests of the values written on bars, fitted to their bars once the figure is laid out.

.. versionadded:: 0.2.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import warnings

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from numdaplot.errors.warnings.readability_warning import ReadabilityWarning
from numdaplot.plots.drawing.labels.bar_label_reading import read_bar_labels
from numdaplot.plots.drawing.labels.bar_value_labels import LabelPlace, write_value_labels
from numdaplot.plots.drawing.labels.label_room import RIGHT_ANGLE
from numdaplot.plots.drawing.labels.value_label_fitting import (
	fit_label,
	fit_labels_to_bars,
	fit_value_labels,
	fits_across,
	fits_inside,
)

NO_ROTATION = 0.0
SMALL_FIGURE_SIZE = (2.0, 2.0)
TWO_POSITIONS = [0.0, 1.0]
TWO_LENGTHS = [1.0, 2.0]
TWO_TEXTS = ["1.00", "2.00"]
LOWER_LIMIT = 0.0
UPPER_LIMIT = 2.0
MANY_BAR_COUNT = 8
MANY_POSITIONS = [float(position) for position in range(MANY_BAR_COUNT)]
MANY_LENGTHS = [1.0] * MANY_BAR_COUNT
WIDE_TEXTS = ["1234.56"] * MANY_BAR_COUNT
CROWDED_BAR_COUNT = 200
CROWDED_POSITIONS = [float(position) for position in range(CROWDED_BAR_COUNT)]
CROWDED_LENGTHS = [1.0] * CROWDED_BAR_COUNT
CROWDED_TEXTS = ["1234.56"] * CROWDED_BAR_COUNT
SHORT_LENGTHS = [1.0, 0.001]
SHORT_TEXTS = ["1.00", "0.00"]
EXPECTED_HIDDEN_MESSAGE = (
	"The values of 200 bars do not fit their bars and are not written. Give a larger ndp.Size, or fewer decimals in "
	"ValueLabels."
)


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


def test_fit_labels_to_bars_turns_every_end_value_upright_when_one_is_too_wide() -> None:
	"""
	Check that values wider than vertical bars all turn upright, and still fit.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure(SMALL_FIGURE_SIZE)
	bars = axes.bar(MANY_POSITIONS, MANY_LENGTHS)
	write_value_labels(axes, bars, WIDE_TEXTS, LabelPlace.VERTICAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	hidden_count = fit_labels_to_bars(bar_labels)

	rotations = {text.get_rotation() for text in axes.texts}
	assert hidden_count == 0
	assert rotations == {RIGHT_ANGLE}


def test_fit_labels_to_bars_keeps_values_level_when_they_fit() -> None:
	"""
	Check that values narrower than their bars stay level.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	write_value_labels(axes, bars, TWO_TEXTS, LabelPlace.VERTICAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	hidden_count = fit_labels_to_bars(bar_labels)

	rotations = {text.get_rotation() for text in axes.texts}
	assert hidden_count == 0
	assert rotations == {NO_ROTATION}


def test_fit_labels_to_bars_hides_values_that_do_not_fit_even_upright() -> None:
	"""
	Check that values of bars too thin even for an upright text are hidden and counted.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure(SMALL_FIGURE_SIZE)
	bars = axes.bar(CROWDED_POSITIONS, CROWDED_LENGTHS)
	write_value_labels(axes, bars, CROWDED_TEXTS, LabelPlace.VERTICAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	hidden_count = fit_labels_to_bars(bar_labels)

	shown_texts = [text for text in axes.texts if text.get_visible()]
	assert hidden_count == CROWDED_BAR_COUNT
	assert shown_texts == []


def test_fit_label_turns_upright_a_middle_value_too_wide_for_its_bar() -> None:
	"""
	Check that a value in the middle of a narrow but tall vertical bar turns upright.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure(SMALL_FIGURE_SIZE)
	bars = axes.bar(MANY_POSITIONS, MANY_LENGTHS)
	write_value_labels(axes, bars, WIDE_TEXTS, LabelPlace.VERTICAL_MIDDLE)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)
	first_label = bar_labels[0]

	is_fitted = fit_label(first_label)

	rotation = first_label.text.get_rotation()
	assert is_fitted
	assert rotation == RIGHT_ANGLE


def test_fit_label_refuses_a_middle_value_too_long_for_a_horizontal_bar() -> None:
	"""
	Check that a value in the middle of a short horizontal bar does not fit and does not turn.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.barh(TWO_POSITIONS, SHORT_LENGTHS)
	write_value_labels(axes, bars, SHORT_TEXTS, LabelPlace.HORIZONTAL_MIDDLE)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)
	short_label = bar_labels[1]

	is_fitted = fit_label(short_label)

	rotation = short_label.text.get_rotation()
	assert not is_fitted
	assert rotation == NO_ROTATION


def test_fits_across_compares_the_height_of_horizontal_bars() -> None:
	"""
	Check that a value past the end of a thick horizontal bar fits across it.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.barh(TWO_POSITIONS, TWO_LENGTHS)
	write_value_labels(axes, bars, TWO_TEXTS, LabelPlace.HORIZONTAL_END)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	fitted_labels = [fits_across(bar_label) for bar_label in bar_labels]

	assert fitted_labels == [True, True]


def test_fits_inside_refuses_a_value_taller_than_its_bar() -> None:
	"""
	Check that a value in the middle of a very short bar does not fit inside it.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	bars = axes.bar(TWO_POSITIONS, SHORT_LENGTHS)
	write_value_labels(axes, bars, SHORT_TEXTS, LabelPlace.VERTICAL_MIDDLE)
	figure.draw_without_rendering()
	bar_labels = read_bar_labels(axes)

	fitted_labels = [fits_inside(bar_label) for bar_label in bar_labels]

	assert fitted_labels == [True, False]


def test_fit_value_labels_leaves_a_figure_without_values() -> None:
	"""
	Check that a figure without values on bars keeps its limits.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure()
	axes.bar(TWO_POSITIONS, TWO_LENGTHS)
	axes.set_ylim(LOWER_LIMIT, UPPER_LIMIT)

	fit_value_labels(figure)

	limits = axes.get_ylim()
	assert limits == (LOWER_LIMIT, UPPER_LIMIT)


def test_fit_value_labels_warns_about_hidden_values() -> None:
	"""
	Check that values hidden for lack of room give a ReadabilityWarning counting them.

	.. versionadded:: 0.2.0
	"""
	figure, axes = build_figure(SMALL_FIGURE_SIZE)
	bars = axes.bar(CROWDED_POSITIONS, CROWDED_LENGTHS)
	write_value_labels(axes, bars, CROWDED_TEXTS, LabelPlace.VERTICAL_END)

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		fit_value_labels(figure)

	readability_warnings = [caught for caught in caught_warnings if caught.category is ReadabilityWarning]
	warning_count = len(readability_warnings)
	warning_text = str(readability_warnings[0].message)
	assert warning_count == 1
	assert warning_text == EXPECTED_HIDDEN_MESSAGE
