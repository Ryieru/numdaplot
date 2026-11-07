"""
Unit tests of the axes of times of day.

.. versionadded:: 0.1.0
"""

import numpy
import pytest
from matplotlib.figure import Figure
from numpy.typing import NDArray

from numdaplot.plots.drawing.time_axis import choose_hour_step, format_hour, place_hour_ticks

DAY_HOURS = numpy.array([8.0, 23.0])
HALF_HOUR = numpy.array([8.0, 8.5])
TWO_HOURS = numpy.array([8.0, 10.0])
FIVE_HOURS = numpy.array([8.0, 13.0])
TEN_HOURS = numpy.array([8.0, 18.0])
MISSING_HOURS = numpy.array([numpy.nan])
FIRST_DRAWN_HOUR = 8.0
LAST_DRAWN_HOUR = 14.0
DRAWN_HOURS = numpy.array([FIRST_DRAWN_HOUR, LAST_DRAWN_HOUR])
EXPECTED_LABELS = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]


@pytest.mark.parametrize(
	("hours", "expected_label"), [(15.5, "15:30"), (0.0, "00:00"), (24.0, "24:00"), (8.2, "08:12")]
)
def test_format_hour_writes_hours_and_minutes(hours: float, expected_label: str) -> None:
	"""
	Check the label of a number of hours since midnight, rounded to the minute.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		The hours since midnight.
	expected_label
		The label.
	"""
	hour_label = format_hour(hours)

	assert hour_label == expected_label


@pytest.mark.parametrize(
	("hours", "expected_step"),
	[(HALF_HOUR, 0.25), (TWO_HOURS, 0.5), (FIVE_HOURS, 1.0), (TEN_HOURS, 2.0), (DAY_HOURS, 3.0), (MISSING_HOURS, 3.0)],
)
def test_choose_hour_step_widens_with_the_span(hours: NDArray[numpy.float64], expected_step: float) -> None:
	"""
	Check the step chosen for each span of times, three hours without any time.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		The hours shown.
	expected_step
		The step between two labels.
	"""
	step = choose_hour_step(hours)

	assert step == expected_step


def test_place_hour_ticks_labels_the_axis_with_times() -> None:
	"""
	Check the labels of an axis from 08:00 to 14:00.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	axes.set_xlim(FIRST_DRAWN_HOUR, LAST_DRAWN_HOUR)

	place_hour_ticks(axes.xaxis, DRAWN_HOURS)
	figure.draw_without_rendering()

	tick_labels = axes.get_xticklabels()
	labels = [label.get_text() for label in tick_labels]
	assert labels == EXPECTED_LABELS
