"""
Unit tests of the arithmetic between dates, datetimes, durations and numbers.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import numpy
import pytest

from numdaplot.arrays.operations.operand import Operand
from numdaplot.arrays.operations.time_arithmetic import (
	combine_nanoseconds,
	combine_time_values,
	find_time_result_type,
	involves_time,
	require_date_next_to_time,
	require_time_operation,
	require_whole_days,
	store_time_result,
	to_nanoseconds,
)
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.value_conversion_error import ValueConversionError

DATES = numpy.array(["2026-01-31", "NaT"], dtype="datetime64[D]")
DATETIMES = numpy.array(["2026-01-31T12:00"], dtype="datetime64[ns]")
DAYS = numpy.array([1, 2], dtype="timedelta64[D]").astype("timedelta64[ns]")
HOURS = numpy.array([36], dtype="timedelta64[h]").astype("timedelta64[ns]")
NUMBERS = numpy.array([2, 3])
ONE_DAY = timedelta(days=1)
TWELVE_HOURS = timedelta(hours=12)
NEW_YEAR = date(2026, 1, 1)
NOON = datetime(2026, 1, 31, 12)
PLUS_SYMBOL = "+"
MINUS_SYMBOL = "-"
TIMES_SYMBOL = "*"
DIVIDE_SYMBOL = "/"
EXPECTED_HOURS_TEXT = "1 days 12:00:00"
EXPECTED_SHIFTED_DATE = numpy.datetime64("2026-02-01")
NANOSECOND_DATETIME_DTYPE = numpy.dtype("datetime64[ns]")
NANOSECOND_DURATION_DTYPE = numpy.dtype("timedelta64[ns]")
MISSING_DURATION = numpy.timedelta64("NaT", "ns")
STORED_TIMES = numpy.array([60000000], dtype="timedelta64[us]")
LATE_TIMES = numpy.array([82800000000, 29700000000, "NaT"], dtype="timedelta64[us]")
ONE_HOUR = timedelta(hours=1)
MORNING_TIMES = numpy.array([29700000000, "NaT"], dtype="timedelta64[us]")
TWO_HOURS = timedelta(hours=2)
NINE_HOURS = timedelta(hours=9)
TIME_NAME = "TIME"
DURATION_NAME = "DURATION"
DATETIME_NAME = "DATETIME"
BASTILLE_DAYS = numpy.array(["2025-07-14", "2025-07-14", "2025-07-14"], dtype="datetime64[D]")
EXPECTED_MOMENTS = numpy.array(["2025-07-14T23:00", "2025-07-14T08:15", "NaT"], dtype="datetime64[ns]")
MORNING_DATETIMES = numpy.array(["2025-07-14T10:00"], dtype="datetime64[ns]")
ONE_TIME = numpy.array([60000000], dtype="timedelta64[us]")
HOUR_IN_NANOSECONDS = numpy.array([3600000000000, -1, 86400000000000, "NaT"], dtype="timedelta64[ns]")


@dataclass(frozen=True)
class OperationCase:
	"""
	An accepted time operation and the type of its result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	function
		The numpy function.
	expected_type
		The type of the result.
	"""

	left: Any
	right: Any
	function: numpy.ufunc
	expected_type: Type


ACCEPTED_CASES = [
	OperationCase(DATES, ONE_DAY, numpy.add, Type.DATE),
	OperationCase(ONE_DAY, DATES, numpy.add, Type.DATE),
	OperationCase(DATES, DAYS, numpy.subtract, Type.DATE),
	OperationCase(DATES, NEW_YEAR, numpy.subtract, Type.DURATION),
	OperationCase(DATES, DATETIMES, numpy.subtract, Type.DURATION),
	OperationCase(DATETIMES, TWELVE_HOURS, numpy.add, Type.DATETIME),
	OperationCase(DATETIMES, NOON, numpy.subtract, Type.DURATION),
	OperationCase(DAYS, ONE_DAY, numpy.add, Type.DURATION),
	OperationCase(DAYS, DAYS, numpy.subtract, Type.DURATION),
	OperationCase(DAYS, NUMBERS, numpy.multiply, Type.DURATION),
	OperationCase(2.5, DAYS, numpy.multiply, Type.DURATION),
	OperationCase(DAYS, 2, numpy.true_divide, Type.DURATION),
]
INCOMPATIBLE_CASES = [
	(DATES, 1, numpy.add),
	(DATES, DATES, numpy.add),
	(DAYS, DATES, numpy.subtract),
	(DAYS, DAYS, numpy.floor_divide),
	(DAYS, DAYS, numpy.remainder),
	(DATES, 2, numpy.multiply),
	(NUMBERS, DAYS, numpy.true_divide),
]
REFUSED_CASES = [
	(DAYS, DAYS, numpy.true_divide),
	(NUMBERS, ONE_DAY, numpy.multiply),
	(ONE_DAY, NUMBERS, numpy.multiply),
]


@pytest.mark.parametrize("case", ACCEPTED_CASES)
def test_combine_time_values_gives_the_type_of_each_accepted_operation(case: OperationCase) -> None:
	"""
	Check the type of the result of each accepted operation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The operands, the function and the expected type.
	"""
	combined_values = combine_time_values(case.left, case.right, case.function, PLUS_SYMBOL)

	result_type = from_numpy_dtype(combined_values.dtype)
	assert result_type == case.expected_type


def test_combine_time_values_adds_days_to_dates() -> None:
	"""
	Check the dates of a date plus one day, a missing date staying missing.

	.. versionadded:: 0.1.0
	"""
	shifted_dates = combine_time_values(DATES, ONE_DAY, numpy.add, PLUS_SYMBOL)

	missing = numpy.isnat(shifted_dates)
	is_missing = bool(missing[1])
	assert shifted_dates[0] == EXPECTED_SHIFTED_DATE
	assert is_missing


@pytest.mark.parametrize(("left", "right", "function"), INCOMPATIBLE_CASES)
def test_combine_time_values_rejects_other_operations(left: Operand, right: Operand, function: numpy.ufunc) -> None:
	"""
	Check that an operation outside the accepted ones raises IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	function
		The numpy function.
	"""
	with pytest.raises(IncompatibleTypesError):
		combine_time_values(left, right, function, MINUS_SYMBOL)


@pytest.mark.parametrize(("left", "right", "function"), REFUSED_CASES)
def test_combine_time_values_refuses_the_duration_conversions(
	left: Operand,
	right: Operand,
	function: numpy.ufunc,
) -> None:
	"""
	Check that a duration divided by a duration and numbers times one duration raise RefusedOperationError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	function
		The numpy function.
	"""
	with pytest.raises(RefusedOperationError):
		combine_time_values(left, right, function, DIVIDE_SYMBOL)


def test_combine_time_values_rejects_part_of_a_day_added_to_dates() -> None:
	"""
	Check that 12 hours added to dates raise ValueConversionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		combine_time_values(DATES, TWELVE_HOURS, numpy.add, PLUS_SYMBOL)


def test_involves_time_is_false_for_numbers() -> None:
	"""
	Check numbers on both sides, then a duration on one side.

	.. versionadded:: 0.1.0
	"""
	with_numbers = involves_time(NUMBERS, 2)
	with_duration = involves_time(NUMBERS, ONE_DAY)

	assert not with_numbers
	assert with_duration


def test_require_time_operation_accepts_durations_times_numbers() -> None:
	"""
	Check that an Array of durations multiplied by numbers is accepted.

	.. versionadded:: 0.1.0
	"""
	operation_key = (numpy.multiply, ValueFamily.DURATION, ValueFamily.NUMBER)

	require_time_operation(DAYS, NUMBERS, operation_key)


def test_to_nanoseconds_converts_dates_and_durations() -> None:
	"""
	Check a single date and an Array of durations, and that numbers stay the same.

	.. versionadded:: 0.1.0
	"""
	moment = to_nanoseconds(NEW_YEAR, ValueFamily.MOMENT)
	durations = to_nanoseconds(DAYS, ValueFamily.DURATION)
	numbers = to_nanoseconds(NUMBERS, ValueFamily.NUMBER)

	assert moment.dtype == NANOSECOND_DATETIME_DTYPE
	assert durations.dtype == NANOSECOND_DURATION_DTYPE
	assert numbers is NUMBERS


def test_require_whole_days_cites_the_first_partial_day() -> None:
	"""
	Check the rejected value of 36 hours.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as caught:
		require_whole_days(HOURS)

	assert caught.value.rejected_value == EXPECTED_HOURS_TEXT


def test_require_whole_days_accepts_whole_days_and_missing_durations() -> None:
	"""
	Check that whole days and NaT are accepted.

	.. versionadded:: 0.1.0
	"""
	require_whole_days(DAYS)
	require_whole_days(MISSING_DURATION)


def read_type_name(values: Any) -> str:
	"""
	Return the name of the numdaplot type of numpy values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Values computed by an operation.

	Returns
	-------
	str
		The name of their type.
	"""
	values_type = from_numpy_dtype(values.dtype)
	type_name = values_type.name

	return type_name


def test_combine_time_values_subtracts_times_into_durations() -> None:
	"""
	Check that two times of day give a duration, NaT kept.

	.. versionadded:: 0.1.0
	"""
	durations = combine_time_values(LATE_TIMES, LATE_TIMES, numpy.subtract, "-")

	assert read_type_name(durations) == DURATION_NAME
	assert bool(numpy.isnat(durations[-1]))


@pytest.mark.parametrize(
	("left", "right", "function"),
	[
		(MORNING_TIMES, ONE_HOUR, numpy.add),
		(ONE_HOUR, MORNING_TIMES, numpy.add),
		(MORNING_TIMES, ONE_HOUR, numpy.subtract),
	],
)
def test_combine_time_values_moves_times_by_a_duration(left: Operand, right: Operand, function: numpy.ufunc) -> None:
	"""
	Check that a duration added on either side, or subtracted, gives times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	function
		The operation.
	"""
	times = combine_time_values(left, right, function, "+")

	assert read_type_name(times) == TIME_NAME


@pytest.mark.parametrize(("duration", "function"), [(TWO_HOURS, numpy.add), (NINE_HOURS, numpy.subtract)])
def test_combine_time_values_refuses_times_past_midnight(duration: timedelta, function: numpy.ufunc) -> None:
	"""
	Check that 23:00 plus 2 hours, or 08:15 minus 9 hours, raise TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	duration
		The duration moving the times.
	function
		The operation.
	"""
	with pytest.raises(TimeOverflowError):
		combine_time_values(LATE_TIMES, duration, function, "+")


@pytest.mark.parametrize(("left", "right"), [(BASTILLE_DAYS, LATE_TIMES), (LATE_TIMES, BASTILLE_DAYS)])
def test_combine_time_values_adds_times_to_dates(left: Operand, right: Operand) -> None:
	"""
	Check that a date plus a time, in either order, gives datetimes, NaT kept.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	"""
	moments = combine_time_values(left, right, numpy.add, "+")

	assert read_type_name(moments) == DATETIME_NAME
	assert numpy.array_equal(moments, EXPECTED_MOMENTS, equal_nan=True)


@pytest.mark.parametrize(("left", "right"), [(MORNING_DATETIMES, ONE_TIME), (ONE_TIME, ONE_TIME)])
def test_combine_time_values_refuses_times_with_datetimes_or_times(left: Operand, right: Operand) -> None:
	"""
	Check that a datetime plus a time, and a time plus a time, raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The left operand.
	right
		The right operand.
	"""
	with pytest.raises(IncompatibleTypesError):
		combine_time_values(left, right, numpy.add, "+")


def test_combine_nanoseconds_counts_durations_in_nanoseconds() -> None:
	"""
	Check the dtype of a sum of a time and a duration before it becomes a time again.

	.. versionadded:: 0.1.0
	"""
	durations = combine_nanoseconds([ONE_TIME, ONE_HOUR], numpy.add, Type.TIME, "+")

	assert read_type_name(durations) == DURATION_NAME


def test_store_time_result_refuses_times_outside_the_day() -> None:
	"""
	Check that before midnight and from the next midnight raise TimeOverflowError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError):
		store_time_result(HOUR_IN_NANOSECONDS, "+")


def test_store_time_result_gives_microseconds() -> None:
	"""
	Check that durations within the day become times of day.

	.. versionadded:: 0.1.0
	"""
	within_day = HOUR_IN_NANOSECONDS[[0, 3]]

	times = store_time_result(within_day, "+")

	assert read_type_name(times) == TIME_NAME


def test_require_date_next_to_time_accepts_dates() -> None:
	"""
	Check that a date next to a time raises nothing.

	.. versionadded:: 0.1.0
	"""
	require_date_next_to_time(Type.DATE, Type.TIME, "+")


def test_find_time_result_type_gives_time_for_the_time_family() -> None:
	"""
	Check the type of a time moved by a duration.

	.. versionadded:: 0.1.0
	"""
	result_type = find_time_result_type(ValueFamily.TIME, False)

	assert result_type == Type.TIME
