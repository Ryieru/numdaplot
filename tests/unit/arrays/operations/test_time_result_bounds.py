"""
Unit tests of the refusal of results of calculations on times.

.. versionadded:: 0.1.0
"""

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.operations.time_bounds import HIGHEST_NANOSECONDS
from numdaplot.arrays.operations.time_result_bounds import (
	can_decimal_factor_overflow,
	can_integers_overflow,
	find_strongest_factor,
	require_decimal_factor_fits,
	require_time_result_fits,
	to_counts,
	widen_large_integers,
)
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.types.type import Type

OPERATION_NAME = "+"
NANOSECOND_DURATION_DTYPE = "timedelta64[ns]"
UNSIGNED_DTYPE = "uint64"
LARGE_INTEGER = 2**70
NANOSECONDS_PER_DAY = 86400 * 10**9
DAYS_OF_LAST_WHOLE_RANGE = 106751


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


def test_can_integers_overflow_is_false_without_present_value() -> None:
	"""
	Check that missing values have no result to refuse.

	.. versionadded:: 0.1.0
	"""
	missing = numpy.array(["NaT"], dtype=NANOSECOND_DURATION_DTYPE)

	can_overflow = can_integers_overflow([missing, 2], numpy.multiply)

	assert can_overflow is False


def test_can_integers_overflow_is_true_when_only_the_extremes_overflow() -> None:
	"""
	Check that bounds out of range send the calculation to the exact check.

	.. versionadded:: 0.1.0
	"""
	durations = numpy.array([HIGHEST_NANOSECONDS, -HIGHEST_NANOSECONDS], dtype=NANOSECOND_DURATION_DTYPE)

	can_overflow = can_integers_overflow([durations, durations], numpy.add)

	assert can_overflow is True


def test_can_decimal_factor_overflow_ignores_factors_without_a_result() -> None:
	"""
	Check that NaN, an infinite factor and 0 are not counted as the strongest factor.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(1)
	factors = numpy.array([numpy.nan, numpy.inf, 0.0])

	can_overflow = can_decimal_factor_overflow(durations, factors, numpy.multiply)

	assert can_overflow is False


def test_can_decimal_factor_overflow_reads_decimals_on_the_left() -> None:
	"""
	Check the factor found on either side.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(1)
	factors = numpy.array([1e300])

	can_overflow = can_decimal_factor_overflow(factors, durations, numpy.multiply)

	assert can_overflow is True


def test_can_decimal_factor_overflow_is_false_without_present_duration() -> None:
	"""
	Check missing durations.

	.. versionadded:: 0.1.0
	"""
	missing = numpy.array(["NaT"], dtype=NANOSECOND_DURATION_DTYPE)

	can_overflow = can_decimal_factor_overflow(missing, 1e300, numpy.multiply)

	assert can_overflow is False


def test_find_strongest_factor_gives_none_for_no_decimal() -> None:
	"""
	Check an Array without value.

	.. versionadded:: 0.1.0
	"""
	factors = numpy.array([], dtype="float64")

	strongest_factor = find_strongest_factor(factors, numpy.multiply)

	assert strongest_factor is None


def test_find_strongest_factor_skips_an_infinite_factor() -> None:
	"""
	Check a factor without result beside a usable one.

	.. versionadded:: 0.1.0
	"""
	factors = numpy.array([numpy.inf, 3.0])

	strongest_factor = find_strongest_factor(factors, numpy.multiply)

	assert strongest_factor == 3.0


def test_find_strongest_factor_uses_the_smallest_divisor() -> None:
	"""
	Check that a small divisor is the strongest.

	.. versionadded:: 0.1.0
	"""
	divisors = numpy.array([4.0, 0.5, 0.0])

	strongest_factor = find_strongest_factor(divisors, numpy.true_divide)

	assert strongest_factor == 2.0


def test_find_strongest_factor_gives_none_for_divisors_of_zero() -> None:
	"""
	Check divisors without result.

	.. versionadded:: 0.1.0
	"""
	divisors = numpy.array([0.0, numpy.nan])

	strongest_factor = find_strongest_factor(divisors, numpy.true_divide)

	assert strongest_factor is None
