"""
Unit tests of the placement of the x values of a chart along its axis.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.dates import ConciseDateFormatter
from matplotlib.figure import Figure

from numdaplot.plots.data.chart_values import Positions
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.plots.drawing.position_axis import (
	find_axis,
	place_categories,
	place_positions,
	write_moment_labels,
	write_position_labels,
)

NUMBERS = Positions(PositionKind.NUMBERS, numpy.array([0.5, 2.0, 12.25]), "weight")
EXPECTED_NUMBER_LABELS = ["0.5", "2", "12.25"]
TEXTS = Positions(PositionKind.TEXTS, numpy.array(["Paris", "Lyon"], dtype=object), "city")
DAYS = numpy.array(["2026-01-01", "NaT"], dtype="datetime64[ns]")
TIMES = numpy.array(["2026-01-01T10:30", "2026-01-02"], dtype="datetime64[ns]")
EXPECTED_DAY_LABELS = ["2026-01-01", "NaT"]
EXPECTED_TIME_LABELS = ["2026-01-01 10:30:00", "2026-01-02 00:00:00"]
MOMENTS = Positions(PositionKind.MOMENTS, DAYS, "day")
HOUR_POSITIONS = Positions(PositionKind.TIMES, numpy.array([8.0, 15.5]), "hour")
EXPECTED_HOUR_LABELS = ["08:00", "15:30"]


def test_place_positions_keeps_numbers_as_they_are() -> None:
	"""
	Check that numbers are their own coordinates.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	coordinates = place_positions(axes, NUMBERS, False)

	assert coordinates is NUMBERS.values


def test_place_positions_places_texts_as_labeled_categories() -> None:
	"""
	Check that texts are placed at 0, 1 and labeled with their text.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	coordinates = place_positions(axes, TEXTS, False)

	tick_labels = axes.get_xticklabels()
	labels = [label.get_text() for label in tick_labels]
	assert coordinates.tolist() == [0.0, 1.0]
	assert labels == ["Paris", "Lyon"]


def test_place_positions_gives_moments_a_concise_date_axis() -> None:
	"""
	Check that moments get the concise date labels of matplotlib.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	place_positions(axes, MOMENTS, False)

	formatter = axes.xaxis.get_major_formatter()
	assert isinstance(formatter, ConciseDateFormatter)


def test_place_categories_labels_the_vertical_axis_for_horizontal_bars() -> None:
	"""
	Check that categories go on the vertical axis when asked.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	place_categories(axes, TEXTS, True)

	tick_labels = axes.get_yticklabels()
	labels = [label.get_text() for label in tick_labels]
	assert labels == ["Paris", "Lyon"]


def test_find_axis_gives_the_horizontal_axis_by_default() -> None:
	"""
	Check that False gives the x axis.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	position_axis = find_axis(axes, False)

	assert position_axis is axes.xaxis


def test_write_position_labels_writes_numbers_without_trailing_zeros() -> None:
	"""
	Check that 2.0 is written 2 and 0.5 stays 0.5.

	.. versionadded:: 0.1.0
	"""
	labels = write_position_labels(NUMBERS)

	assert labels == EXPECTED_NUMBER_LABELS


def test_write_moment_labels_writes_days_without_time() -> None:
	"""
	Check that dates at midnight are written without time, NaT staying NaT.

	.. versionadded:: 0.1.0
	"""
	labels = write_moment_labels(DAYS)

	assert labels == EXPECTED_DAY_LABELS


def test_write_moment_labels_writes_the_time_when_one_value_has_one() -> None:
	"""
	Check that every datetime is written with its time when one of them is not at midnight.

	.. versionadded:: 0.1.0
	"""
	labels = write_moment_labels(TIMES)

	assert labels == EXPECTED_TIME_LABELS


def test_write_position_labels_writes_times_of_day() -> None:
	"""
	Check the HH:MM labels of positions in hours.

	.. versionadded:: 0.1.0
	"""
	labels = write_position_labels(HOUR_POSITIONS)

	assert labels == EXPECTED_HOUR_LABELS


def test_place_positions_keeps_the_hours_of_times() -> None:
	"""
	Check that times of day are placed at their hours, on an axis labeled HH:MM.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()

	coordinates = place_positions(axes, HOUR_POSITIONS, False)

	formatter = axes.xaxis.get_major_formatter()
	first_label = formatter(HOUR_POSITIONS.values[0])
	assert coordinates is HOUR_POSITIONS.values
	assert first_label == EXPECTED_HOUR_LABELS[0]
