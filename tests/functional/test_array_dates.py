"""
Functional tests of dates, datetimes and durations in an Array: arithmetic, time functions and text.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime, timedelta

import pytest

import numdaplot as ndp

ARRIVALS = [date(2026, 1, 1), date(2026, 1, 10)]
DEPARTURES = [date(2026, 1, 4), date(2026, 1, 20)]
EXPECTED_NIGHTS = [3.0, 10.0]
ONE_WEEK = timedelta(days=7)
EXPECTED_NEXT_WEEK = [date(2026, 1, 8), date(2026, 1, 17)]
TWELVE_HOURS = timedelta(hours=12)
NOON = datetime(2026, 7, 1, 12)
EXPECTED_MIDNIGHT = [datetime(2026, 7, 2, 0, 0)]
SALE_DAYS = [date(2026, 1, 5), None, date(2027, 1, 9)]
EXPECTED_MISSING_MONTHS = [False, True, False]
EXPECTED_PRESENT_MONTHS = [1.0, 1.0]
EXPECTED_MONTH_STARTS = [date(2026, 1, 1), None, date(2027, 1, 1)]
NIGHT_COUNTS = [1.5, 2.0]
EXPECTED_DURATION_TEXT = "Array(['1 days 12:00:00', '2 days 00:00:00'], dtype=DURATION)"
EXPECTED_DATETIME_TEXT = "Array(['2026-07-01 12:00:00'], dtype=DATETIME)"
DOUBLE = 2
EXPECTED_DOUBLE_TEXT = "Array(['6 days 00:00:00', '20 days 00:00:00'], dtype=DURATION)"
UTC_NOON = datetime(2026, 7, 1, 12, tzinfo=UTC)


def build_stays() -> ndp.Array:
	"""
	Return the durations of two stays, of 3 and 10 nights.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Array
		The durations.
	"""
	arrivals = ndp.Array.from_list(ARRIVALS)
	departures = ndp.Array.from_list(DEPARTURES)
	stays = departures - arrivals

	return stays


def test_two_dates_subtract_into_durations_counted_in_days() -> None:
	"""
	Check the number of nights of each stay.

	.. versionadded:: 0.1.0
	"""
	stays = build_stays()

	nights = stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.DAY))

	night_list = nights.to_list()
	assert night_list == EXPECTED_NIGHTS


def test_a_duration_added_to_dates_gives_dates() -> None:
	"""
	Check that one week later is still a date.

	.. versionadded:: 0.1.0
	"""
	arrivals = ndp.Array.from_list(ARRIVALS)

	next_week = arrivals + ONE_WEEK

	next_week_list = next_week.to_list()
	assert next_week.dtype == ndp.Type.DATE
	assert next_week_list == EXPECTED_NEXT_WEEK


def test_hours_added_to_dates_are_refused() -> None:
	"""
	Check that 12 hours added to dates raise ValueConversionError.

	.. versionadded:: 0.1.0
	"""
	arrivals = ndp.Array.from_list(ARRIVALS)

	with pytest.raises(ndp.ValueConversionError):
		_ = arrivals + TWELVE_HOURS


def test_hours_added_to_datetimes_give_datetimes() -> None:
	"""
	Check noon plus 12 hours.

	.. versionadded:: 0.1.0
	"""
	noons = ndp.Array.from_list([NOON])

	midnights = noons + TWELVE_HOURS

	midnight_list = midnights.to_list()
	assert midnight_list == EXPECTED_MIDNIGHT


def test_a_number_added_to_dates_is_refused() -> None:
	"""
	Check that a date plus 1 raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	arrivals = ndp.Array.from_list(ARRIVALS)

	with pytest.raises(ndp.IncompatibleTypesError):
		_ = arrivals + 1


def test_durations_multiply_by_numbers() -> None:
	"""
	Check stays twice as long.

	.. versionadded:: 0.1.0
	"""
	stays = build_stays()

	double_stays = stays * DOUBLE

	stay_text = repr(double_stays)
	assert stay_text == EXPECTED_DOUBLE_TEXT


def test_durations_divided_by_durations_point_to_duration_in() -> None:
	"""
	Check that dividing two durations raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	stays = build_stays()

	with pytest.raises(ndp.RefusedOperationError):
		_ = stays / stays


def test_numbers_times_a_timedelta_point_to_to_duration() -> None:
	"""
	Check that numbers multiplied by one timedelta raise RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	nights = ndp.Array.from_list(NIGHT_COUNTS)

	with pytest.raises(ndp.RefusedOperationError):
		_ = nights * ONE_WEEK


def test_numbers_become_durations_with_to_duration() -> None:
	"""
	Check 1.5 and 2 days written as durations.

	.. versionadded:: 0.1.0
	"""
	nights = ndp.Array.from_list(NIGHT_COUNTS)

	durations = nights.apply(ndp.ToDuration(unit=ndp.DurationUnit.DAY))

	duration_text = repr(durations)
	assert duration_text == EXPECTED_DURATION_TEXT


def test_date_parts_are_decimals_with_missing_values() -> None:
	"""
	Check the month of each sale, a missing date giving a missing month.

	.. versionadded:: 0.1.0
	"""
	sale_days = ndp.Array.from_list(SALE_DAYS)

	months = sale_days.apply(ndp.DatePart(unit=ndp.DatePartUnit.MONTH))

	missing_months = months.check(ndp.IsMissing())
	present_months = months.select(ndp.IsPresent())
	missing_list = missing_months.to_list()
	present_list = present_months.to_list()
	assert missing_list == EXPECTED_MISSING_MONTHS
	assert present_list == EXPECTED_PRESENT_MONTHS


def test_date_periods_give_the_first_day_of_each_month() -> None:
	"""
	Check that January 2026 and January 2027 stay apart.

	.. versionadded:: 0.1.0
	"""
	sale_days = ndp.Array.from_list(SALE_DAYS)

	month_starts = sale_days.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))

	month_start_list = month_starts.to_list()
	assert month_start_list == EXPECTED_MONTH_STARTS


def test_hours_of_dates_are_refused() -> None:
	"""
	Check that the hour of a date raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	sale_days = ndp.Array.from_list(SALE_DAYS)

	with pytest.raises(ndp.IncompatibleTypesError):
		sale_days.apply(ndp.DatePart(unit=ndp.DatePartUnit.HOUR))


def test_datetimes_are_written_without_t_nor_nanoseconds() -> None:
	"""
	Check the text of a datetime Array.

	.. versionadded:: 0.1.0
	"""
	noons = ndp.Array.from_list([NOON])

	noon_text = repr(noons)
	assert noon_text == EXPECTED_DATETIME_TEXT


def test_an_array_refuses_datetimes_with_a_time_zone() -> None:
	"""
	Check that an Array of datetimes with a zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeZoneMismatchError):
		ndp.Array.from_list([UTC_NOON])
