"""
Unit tests of the refusal of times out of the range of nanoseconds.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime, timedelta

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.operations.time_bounds import (
	FIRST_COUNT_TOO_LARGE,
	HIGHEST_DATETIME,
	HIGHEST_NANOSECONDS,
	LONGEST_DURATION,
	LOWEST_DATETIME,
	is_python_time_in_range,
	require_decimal_durations_fit,
	require_decimal_factor_fits,
	require_nanoseconds_fit,
	require_stored_times_fit,
	require_time_result_fits,
	require_whole_durations_fit,
	to_counts,
	widen_large_integers,
)
from numdaplot.data_types.type import Type
from numdaplot.errors.time_overflow_error import TimeOverflowError

OPERATION_NAME = "+"
ONE_MICROSECOND = timedelta(microseconds=1)
FAR_DATETIME = datetime(3000, 1, 1)
FAR_DATE = date(3000, 1, 1)
FAR_DURATION = timedelta(days=200000)
CLOSE_DATE = date(2026, 1, 31)
NANOSECOND_DURATION_DTYPE = "timedelta64[ns]"
NANOSECOND_DATETIME_DTYPE = "datetime64[ns]"
DAY_DTYPE = "datetime64[D]"
SECOND_DTYPE = "datetime64[s]"
UNSIGNED_DTYPE = "uint64"
LARGE_INTEGER = 2**70
NANOSECONDS_PER_DAY = 86400 * 10**9
DAYS_BEYOND_RANGE = 200000
DAYS_OF_LAST_WHOLE_RANGE = 106751
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


def test_to_counts_gives_zero_for_a_missing_time() -> None:
	"""
	Check that NaT does not count as the lowest integer.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([5, "NaT"], dtype=NANOSECOND_DURATION_DTYPE)

	counts = to_counts(values)

	count_list = counts.tolist()
	assert count_list == [5, 0]


def test_to_counts_keeps_numbers() -> None:
	"""
	Check that numbers are not changed.

	.. versionadded:: 0.1.0
	"""
	counts = to_counts(2.5)

	single_count = counts.item()
	assert single_count == 2.5


def test_widen_large_integers_turns_a_large_integer_into_a_decimal() -> None:
	"""
	Check a Python integer that fits no signed count.

	.. versionadded:: 0.1.0
	"""
	widened = widen_large_integers(LARGE_INTEGER)

	assert widened == float(LARGE_INTEGER)


def test_widen_large_integers_keeps_an_integer_that_fits() -> None:
	"""
	Check a small Python integer.

	.. versionadded:: 0.1.0
	"""
	widened = widen_large_integers(2)

	assert widened == 2


def test_widen_large_integers_keeps_unsigned_integers_exact_when_they_fit() -> None:
	"""
	Check ``UINT64`` values that fit a signed count.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([2], dtype=UNSIGNED_DTYPE)

	widened = widen_large_integers(values)

	assert widened.dtype.kind == "i"


def test_widen_large_integers_turns_large_unsigned_integers_into_decimals() -> None:
	"""
	Check ``UINT64`` values above the signed counts.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([2**63], dtype=UNSIGNED_DTYPE)

	widened = widen_large_integers(values)

	assert widened.dtype.kind == "f"


def test_widen_large_integers_keeps_an_empty_unsigned_array() -> None:
	"""
	Check an Array without value, which has no bounds.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([], dtype=UNSIGNED_DTYPE)

	widened = widen_large_integers(values)

	assert widened.size == 0


def test_require_decimal_factor_fits_accepts_a_divisor_of_zero() -> None:
	"""
	Check that a division by 0 gives a missing value and not a refusal.

	.. versionadded:: 0.1.0
	"""
	operands = [numpy.array([NANOSECONDS_PER_DAY]), numpy.array([0.0])]

	require_decimal_factor_fits(operands, numpy.true_divide, Type.DURATION, OPERATION_NAME)


def test_require_decimal_factor_fits_refuses_a_decimal_on_the_left() -> None:
	"""
	Check the factor found on either side.

	.. versionadded:: 0.1.0
	"""
	operands = [numpy.array([1e300]), numpy.array([NANOSECONDS_PER_DAY])]

	with pytest.raises(TimeOverflowError):
		require_decimal_factor_fits(operands, numpy.multiply, Type.DURATION, OPERATION_NAME)


def build_durations(day_count: int) -> NDArray[numpy.timedelta64]:
	"""
	Return one duration in nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	day_count
		The number of days.

	Returns
	-------
	NDArray[numpy.timedelta64]
		The duration.
	"""
	days = numpy.array([day_count], dtype="timedelta64[D]")
	durations = days.astype(NANOSECOND_DURATION_DTYPE)

	return durations


def test_require_time_result_fits_refuses_a_sum_too_large() -> None:
	"""
	Check a sum beyond the range.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(DAYS_OF_LAST_WHOLE_RANGE)

	with pytest.raises(TimeOverflowError):
		require_time_result_fits([durations, durations], numpy.add, Type.DURATION, OPERATION_NAME)


def test_require_time_result_fits_accepts_an_integer_division() -> None:
	"""
	Check that a division by an integer cannot move away from zero.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(DAYS_OF_LAST_WHOLE_RANGE)

	require_time_result_fits([durations, 0], numpy.true_divide, Type.DURATION, OPERATION_NAME)


def test_require_time_result_fits_refuses_the_count_kept_for_missing_values() -> None:
	"""
	Check that a result cannot become a missing value by reaching the lowest count.

	.. versionadded:: 0.1.0
	"""
	lowest_duration = numpy.array([-HIGHEST_NANOSECONDS], dtype=NANOSECOND_DURATION_DTYPE)
	one_nanosecond = numpy.array([1], dtype=NANOSECOND_DURATION_DTYPE)
	operands = [lowest_duration, one_nanosecond]

	with pytest.raises(TimeOverflowError):
		require_time_result_fits(operands, numpy.subtract, Type.DURATION, OPERATION_NAME)


def test_require_time_result_fits_accepts_a_missing_value_with_a_large_value() -> None:
	"""
	Check that a missing value counts as nothing.

	.. versionadded:: 0.1.0
	"""
	durations = numpy.array([HIGHEST_NANOSECONDS], dtype=NANOSECOND_DURATION_DTYPE)
	missing = numpy.array(["NaT"], dtype=NANOSECOND_DURATION_DTYPE)

	require_time_result_fits([durations, missing], numpy.add, Type.DURATION, OPERATION_NAME)


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
