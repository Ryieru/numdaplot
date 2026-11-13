"""
Unit tests of the corner label of a time axis.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import numpy
from matplotlib.axes import Axes
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from matplotlib.figure import Figure

from numdaplot.plots.drawing.axes.moment_period_formatter import (
	MomentPeriodFormatter,
	find_data_bounds,
	find_view_bounds,
	find_visible_period,
	write_period,
)

MOMENT_DTYPE = "datetime64[ns]"
DAY_UNIT = "D"
TWO_VALUES = [1.0, 2.0]
MONTH_FORMAT = "%Y-%b"
LOW_COORDINATE = 10.0
MIDDLE_COORDINATE = 15.0
HIGH_COORDINATE = 20.0
HIGHEST_COORDINATE = 30.0
ZOOM_START = 12.0
ZOOM_STOP = 14.0
FAR_ZOOM_START = 50.0
FAR_ZOOM_STOP = 60.0


def find_date_number(day: str) -> float:
	"""
	Return the matplotlib date number of a day, the count of days since 1970.

	.. versionadded:: 0.1.0

	Parameters
	----------
	day
		The day, as ``YYYY-MM-DD``.

	Returns
	-------
	float
		The date number.
	"""
	day_moment = numpy.datetime64(day, DAY_UNIT)
	day_count = day_moment.astype(numpy.int64)
	date_number = float(day_count)

	return date_number


def build_time_axes(first_moment: str, last_moment: str) -> tuple[Figure, Axes]:
	"""
	Return a figure and its axes with a line between two moments on a time axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_moment
		The first moment.
	last_moment
		The last moment.

	Returns
	-------
	tuple[Figure, Axes]
		The figure and its axes.
	"""
	figure = Figure()
	axes = figure.add_subplot()
	moments = numpy.array([first_moment, last_moment], dtype=MOMENT_DTYPE)
	axes.plot(moments, TWO_VALUES)
	locator = AutoDateLocator()
	axes.xaxis.set_major_locator(locator)
	formatter = MomentPeriodFormatter(locator, axes, False)
	axes.xaxis.set_major_formatter(formatter)

	return figure, axes


def read_corner_label(first_moment: str, last_moment: str) -> str:
	"""
	Return the corner label of a time axis going from one moment to another.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first_moment
		The first moment.
	last_moment
		The last moment.

	Returns
	-------
	str
		The text of the corner label.
	"""
	figure, axes = build_time_axes(first_moment, last_moment)
	figure.draw_without_rendering()
	corner_label = axes.xaxis.get_offset_text()
	corner_text = corner_label.get_text()

	return corner_text


def test_formatter_keeps_the_concise_labels_of_matplotlib() -> None:
	"""
	Check that the formatter is a concise date formatter, which the tick rotation relies on.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	locator = AutoDateLocator()

	formatter = MomentPeriodFormatter(locator, axes, False)

	assert isinstance(formatter, ConciseDateFormatter)


def test_corner_label_ignores_a_last_tick_past_the_values() -> None:
	"""
	Check that a tick on April 1 does not name April when the values stop in March.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-03-01", "2019-03-31")

	assert corner_text == "2019-Mar"


def test_corner_label_gives_both_months_of_a_longer_period() -> None:
	"""
	Check that a period over several months names its first and its last month.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-03-15", "2019-05-15")

	assert corner_text == "2019-Mar to 2019-May"


def test_corner_label_gives_both_years_of_a_period_across_years() -> None:
	"""
	Check that a period across two years names both.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-11-01", "2020-02-15")

	assert corner_text == "2019-Nov to 2020-Feb"


def test_corner_label_gives_one_day_for_hours_of_one_day() -> None:
	"""
	Check that hours inside one day give that day.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-03-05T06:00", "2019-03-05T20:00")

	assert corner_text == "2019-Mar-05"


def test_corner_label_gives_both_days_of_hours_across_midnight() -> None:
	"""
	Check that hours across midnight name both days.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-03-05T22:00", "2019-03-06T02:00")

	assert corner_text == "2019-Mar-05 to 2019-Mar-06"


def test_corner_label_stays_empty_when_the_ticks_give_the_years() -> None:
	"""
	Check that ticks showing the years need no corner label.

	.. versionadded:: 0.1.0
	"""
	corner_text = read_corner_label("2019-01-01", "2021-06-01")

	assert corner_text == ""


def test_corner_label_follows_a_zoom() -> None:
	"""
	Check that the label gives only the visible part of the values.

	.. versionadded:: 0.1.0
	"""
	figure, axes = build_time_axes("2019-03-15", "2019-05-15")
	zoom_start = find_date_number("2019-04-05")
	zoom_stop = find_date_number("2019-04-20")
	axes.set_xlim(zoom_start, zoom_stop)

	figure.draw_without_rendering()

	corner_label = axes.xaxis.get_offset_text()
	corner_text = corner_label.get_text()
	assert corner_text == "2019-Apr"


def test_find_visible_period_gives_the_values_inside_the_margins() -> None:
	"""
	Check that the margins of the axis are not part of the period.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([LOW_COORDINATE, HIGH_COORDINATE], TWO_VALUES)

	period = find_visible_period(axes, False)

	assert period == (LOW_COORDINATE, HIGH_COORDINATE)


def test_find_visible_period_stops_at_the_zoom() -> None:
	"""
	Check that a zoom inside the values limits the period.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([LOW_COORDINATE, HIGH_COORDINATE], TWO_VALUES)
	axes.set_xlim(ZOOM_START, ZOOM_STOP)

	period = find_visible_period(axes, False)

	assert period == (ZOOM_START, ZOOM_STOP)


def test_find_visible_period_gives_the_view_when_it_shows_no_value() -> None:
	"""
	Check that a zoom away from the values gives the visible axis.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([LOW_COORDINATE, HIGH_COORDINATE], TWO_VALUES)
	axes.set_xlim(FAR_ZOOM_START, FAR_ZOOM_STOP)

	period = find_visible_period(axes, False)

	assert period == (FAR_ZOOM_START, FAR_ZOOM_STOP)


def test_find_visible_period_stays_ordered_on_an_inverted_axis() -> None:
	"""
	Check that an inverted axis gives the period in increasing order.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot([LOW_COORDINATE, HIGH_COORDINATE], TWO_VALUES)
	axes.invert_xaxis()

	period = find_visible_period(axes, False)

	assert period == (LOW_COORDINATE, HIGH_COORDINATE)


def test_find_visible_period_reads_the_vertical_axis() -> None:
	"""
	Check that moments on the vertical axis use the vertical values.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.plot(TWO_VALUES, [LOW_COORDINATE, HIGH_COORDINATE])

	period = find_visible_period(axes, True)

	assert period == (LOW_COORDINATE, HIGH_COORDINATE)


def test_find_data_bounds_includes_the_axes_on_the_right() -> None:
	"""
	Check that values of the axes sharing the axis count in the bounds.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	right_axes = axes.twinx()
	axes.plot([LOW_COORDINATE, HIGH_COORDINATE], TWO_VALUES)
	right_axes.plot([MIDDLE_COORDINATE, HIGHEST_COORDINATE], TWO_VALUES)

	bounds = find_data_bounds(axes, False)

	assert bounds == (LOW_COORDINATE, HIGHEST_COORDINATE)


def test_find_data_bounds_are_reversed_without_value() -> None:
	"""
	Check that axes without value give a low bound above the high bound.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()

	low_bound, high_bound = find_data_bounds(axes, False)

	assert low_bound > high_bound


def test_find_view_bounds_stays_ordered_on_an_inverted_axis() -> None:
	"""
	Check that the low bound comes first on an inverted axis.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.set_xlim(HIGH_COORDINATE, LOW_COORDINATE)

	bounds = find_view_bounds(axes, False)

	assert bounds == (LOW_COORDINATE, HIGH_COORDINATE)


def test_find_view_bounds_reads_the_vertical_axis() -> None:
	"""
	Check that the vertical axis gives its own bounds.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	axes.set_ylim(LOW_COORDINATE, HIGH_COORDINATE)

	bounds = find_view_bounds(axes, True)

	assert bounds == (LOW_COORDINATE, HIGH_COORDINATE)


def test_write_period_writes_one_value_when_both_ends_read_the_same() -> None:
	"""
	Check that two days of one month read as that month.

	.. versionadded:: 0.1.0
	"""
	start = find_date_number("2019-03-01")
	stop = find_date_number("2019-03-31")

	period_text = write_period(start, stop, MONTH_FORMAT)

	assert period_text == "2019-Mar"


def test_write_period_writes_both_ends_when_they_differ() -> None:
	"""
	Check that two different months are separated by to.

	.. versionadded:: 0.1.0
	"""
	start = find_date_number("2019-02-28")
	stop = find_date_number("2019-03-31")

	period_text = write_period(start, stop, MONTH_FORMAT)

	assert period_text == "2019-Feb to 2019-Mar"
