"""
Unit tests of the refusal of times out of the range of nanoseconds.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime, timedelta

import numpy
import pytest

from numdaplot.arrays.operations.time_bounds import (
	FIRST_COUNT_TOO_LARGE,
	HIGHEST_DATETIME,
	HIGHEST_NANOSECONDS,
	LONGEST_DURATION,
	LOWEST_DATETIME,
	find_present_bounds,
	is_python_time_in_range,
	require_decimal_durations_fit,
	require_nanoseconds_fit,
	require_stored_times_fit,
	require_whole_durations_fit,
)
from numdaplot.data_types.type import Type
from numdaplot.errors.time_overflow_error import TimeOverflowError

OPERATION_NAME = "+"
ONE_MICROSECOND = timedelta(microseconds=1)
FAR_DATETIME = datetime(3000, 1, 1)
FAR_DATE = date(3000, 1, 1)
CLOSE_DATE = date(2026, 1, 31)
NANOSECOND_DURATION_DTYPE = "timedelta64[ns]"
DAY_DTYPE = "datetime64[D]"
SECOND_DTYPE = "datetime64[s]"
NANOSECONDS_PER_DAY = 86400 * 10**9
DAYS_BEYOND_RANGE = 200000
HIGHEST_NATIVE_TEXT = HIGHEST_DATETIME.isoformat()
LOWEST_NATIVE_TEXT = LOWEST_DATETIME.isoformat()
NANOSECOND_UNIT = "ns"
COUNT_DTYPE = "int64"


@pytest.mark.parametrize(
	"value",
	[HIGHEST_DATETIME, LOWEST_DATETIME, LONGEST_DURATION, -LONGEST_DURATION, CLOSE_DATE, 5, "text", None],
)
def test_is_python_time_in_range_accepts_the_limits_and_other_values(value: object) -> None:
	"""
	Check the limits of the range, and that other values are not concerned.

	.. versionadded:: 0.1.0
	"""
	in_range = is_python_time_in_range(value)

	assert in_range is True


@pytest.mark.parametrize(
	"value",
	[
		HIGHEST_DATETIME + ONE_MICROSECOND,
		LOWEST_DATETIME - ONE_MICROSECOND,
		LONGEST_DURATION + ONE_MICROSECOND,
		-LONGEST_DURATION - ONE_MICROSECOND,
		FAR_DATE,
	],
)
def test_is_python_time_in_range_refuses_what_follows_the_limits(value: object) -> None:
	"""
	Check the first values out of range.

	.. versionadded:: 0.1.0
	"""
	in_range = is_python_time_in_range(value)

	assert in_range is False


def test_is_python_time_in_range_reads_a_datetime_with_a_zone_by_its_clock_time() -> None:
	"""
	Check that a time zone does not stop the comparison.

	.. versionadded:: 0.1.0
	"""
	far_with_zone = FAR_DATETIME.replace(tzinfo=UTC)

	in_range = is_python_time_in_range(far_with_zone)

	assert in_range is False


def test_the_limits_match_the_nanoseconds_numpy_can_count() -> None:
	"""
	Check the Python limits against the counts of numpy.

	.. versionadded:: 0.1.0
	"""
	highest_moment = numpy.datetime64(HIGHEST_NATIVE_TEXT, NANOSECOND_UNIT)
	lowest_moment = numpy.datetime64(LOWEST_NATIVE_TEXT, NANOSECOND_UNIT)
	highest_count = highest_moment.astype(COUNT_DTYPE)
	lowest_count = lowest_moment.astype(COUNT_DTYPE)

	highest_integer = int(highest_count)
	lowest_integer = int(lowest_count)
	assert highest_integer <= HIGHEST_NANOSECONDS
	assert lowest_integer >= -HIGHEST_NANOSECONDS


def test_require_stored_times_fit_refuses_a_datetime_out_of_range() -> None:
	"""
	Check a list of datetimes.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError):
		require_stored_times_fit([FAR_DATETIME], Type.DATETIME, OPERATION_NAME)


def test_require_stored_times_fit_leaves_dates_stored_in_days() -> None:
	"""
	Check that ``DATE`` values are not limited when they are stored.

	.. versionadded:: 0.1.0
	"""
	require_stored_times_fit([FAR_DATE], Type.DATE, OPERATION_NAME)


def test_require_nanoseconds_fit_refuses_a_single_value() -> None:
	"""
	Check a single Python value.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError):
		require_nanoseconds_fit(FAR_DATETIME, Type.DATETIME, OPERATION_NAME)


def test_require_nanoseconds_fit_accepts_a_single_number() -> None:
	"""
	Check that a number is not concerned.

	.. versionadded:: 0.1.0
	"""
	require_nanoseconds_fit(5, Type.INT64, OPERATION_NAME)


@pytest.mark.parametrize("dtype", [DAY_DTYPE, SECOND_DTYPE])
def test_require_nanoseconds_fit_refuses_a_coarser_array(dtype: str) -> None:
	"""
	Check Arrays in other units than nanoseconds.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(["3000-01-01"], dtype=dtype)

	with pytest.raises(TimeOverflowError):
		require_nanoseconds_fit(values, Type.DATE, OPERATION_NAME)


def test_require_nanoseconds_fit_accepts_a_coarser_array_in_range() -> None:
	"""
	Check dates that can be counted in nanoseconds.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(["2026-01-01", "NaT"], dtype=DAY_DTYPE)

	require_nanoseconds_fit(values, Type.DATE, OPERATION_NAME)


def test_require_nanoseconds_fit_accepts_only_missing_values() -> None:
	"""
	Check an Array without present value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(["NaT"], dtype=DAY_DTYPE)

	require_nanoseconds_fit(values, Type.DATE, OPERATION_NAME)


def test_require_whole_durations_fit_refuses_a_large_integer() -> None:
	"""
	Check integers read as durations.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([DAYS_BEYOND_RANGE])

	with pytest.raises(TimeOverflowError):
		require_whole_durations_fit(values, NANOSECONDS_PER_DAY, OPERATION_NAME)


def test_require_whole_durations_fit_accepts_no_value() -> None:
	"""
	Check an Array without value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([], dtype="int64")

	require_whole_durations_fit(values, NANOSECONDS_PER_DAY, OPERATION_NAME)


def test_require_decimal_durations_fit_refuses_the_first_count_too_large() -> None:
	"""
	Check the limit of decimal counts.

	.. versionadded:: 0.1.0
	"""
	nanoseconds = numpy.array([FIRST_COUNT_TOO_LARGE])

	with pytest.raises(TimeOverflowError):
		require_decimal_durations_fit(nanoseconds, OPERATION_NAME)


def test_require_decimal_durations_fit_accepts_a_missing_value() -> None:
	"""
	Check that NaN is never out of range.

	.. versionadded:: 0.1.0
	"""
	nanoseconds = numpy.array([numpy.nan])

	require_decimal_durations_fit(nanoseconds, OPERATION_NAME)


def test_find_present_bounds_skips_missing_values() -> None:
	"""
	Check that NaT does not count as the lowest value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([5, "NaT", 2], dtype=NANOSECOND_DURATION_DTYPE)

	bounds = find_present_bounds(values)

	assert bounds == (2, 5)


def test_find_present_bounds_gives_none_without_present_value() -> None:
	"""
	Check an Array holding only missing values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(["NaT"], dtype=NANOSECOND_DURATION_DTYPE)

	bounds = find_present_bounds(values)

	assert bounds is None


def test_find_present_bounds_gives_none_for_an_empty_array() -> None:
	"""
	Check an Array without value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([], dtype=NANOSECOND_DURATION_DTYPE)

	bounds = find_present_bounds(values)

	assert bounds is None


def test_find_present_bounds_reads_a_single_number() -> None:
	"""
	Check a single integer.

	.. versionadded:: 0.1.0
	"""
	bounds = find_present_bounds(3)

	assert bounds == (3, 3)
