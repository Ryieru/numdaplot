"""
Unit tests of the axes of times of day.

.. versionadded:: 0.1.0
"""

from datetime import time

import numpy
import pytest
from matplotlib.figure import Figure
from numpy.typing import NDArray

import numdaplot as ndp
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.sample_values import read_sample_values
from numdaplot.plots.drawing.axes.time_axis import (
	choose_hour_step,
	format_hour,
	measures_times,
	place_hour_ticks,
	place_value_hours,
)
from numdaplot.plots.layers.chart_layer import ChartLayer

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
HOURS_BEFORE_MIDNIGHT = -3.0
HOURS_AFTER_MIDNIGHT = 27.0
OUTSIDE_DAY_LABEL = ""
HALF_PAST_EIGHT = 8.5
EXPECTED_HALF_PAST_EIGHT = "08:30"
LINE_CHART_NAME = "LineChart"
BOX_CHART_NAME = "BoxChart"
VALUE_HOURS = ndp.Array.from_list([time(8), time(14)])
VALUE_COUNTS = ndp.Array.from_list([3.0, 5.0])


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


@pytest.mark.parametrize("hours", [HOURS_BEFORE_MIDNIGHT, HOURS_AFTER_MIDNIGHT])
def test_format_hour_leaves_ticks_outside_the_day_without_label(hours: float) -> None:
	"""
	Check that the ticks of the margins before 00:00 and after 24:00 have no label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	hours
		Hours outside the day.
	"""
	hour_label = format_hour(hours)

	assert hour_label == OUTSIDE_DAY_LABEL


@pytest.mark.parametrize(("value_type", "expected_result"), [(ndp.Type.TIME, True), (ndp.Type.INT64, False)])
def test_measures_times_is_true_for_times_of_day_only(value_type: ndp.Type, expected_result: bool) -> None:
	"""
	Check that only TIME values are measured on an axis of hours.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value_type
		The type of the values.
	expected_result
		Whether they are times of day.
	"""
	is_time = measures_times(value_type)

	assert is_time == expected_result


def test_place_value_hours_labels_the_axis_of_a_line_of_times() -> None:
	"""
	Check that a line of times of day labels the vertical axis HH:MM.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	hour_values = read_array_values(VALUE_HOURS, LINE_CHART_NAME)
	hour_line = ChartLayer(ndp.LineChart(), hour_values)

	place_value_hours(axes, [hour_line])

	formatter = axes.yaxis.get_major_formatter()
	hour_label = formatter(HALF_PAST_EIGHT)
	assert hour_label == EXPECTED_HALF_PAST_EIGHT


def test_place_value_hours_keeps_the_axis_of_a_line_of_numbers() -> None:
	"""
	Check that a line of numbers keeps the formatter of matplotlib.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	default_formatter = axes.yaxis.get_major_formatter()
	count_values = read_array_values(VALUE_COUNTS, LINE_CHART_NAME)
	count_line = ChartLayer(ndp.LineChart(), count_values)

	place_value_hours(axes, [count_line])

	formatter = axes.yaxis.get_major_formatter()
	assert formatter is default_formatter


def test_place_value_hours_leaves_boxes_to_their_own_drawing() -> None:
	"""
	Check that boxes of times of day are skipped, as they label their own axis.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	axes = figure.add_subplot()
	default_formatter = axes.yaxis.get_major_formatter()
	hour_samples = read_sample_values(VALUE_HOURS, None, None, BOX_CHART_NAME)
	hour_boxes = ChartLayer(ndp.BoxChart(), hour_samples)

	place_value_hours(axes, [hour_boxes])

	formatter = axes.yaxis.get_major_formatter()
	assert formatter is default_formatter
