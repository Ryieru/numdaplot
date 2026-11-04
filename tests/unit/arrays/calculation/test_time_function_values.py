"""
Unit tests of the application of time functions to Array values.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.calculation.time_function_values import (
	apply_time_function,
	build_durations,
	count_durations,
	find_date_periods,
	read_date_parts,
	require_moments,
)
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.period_unit import PeriodUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError

DATETIMES = numpy.array(["2026-12-31T14:30:15", "NaT"], dtype="datetime64[ns]")
DATES = numpy.array(["2026-12-31", "2027-01-09"], dtype="datetime64[D]")
GRID_DATES = numpy.array([["2026-01-05"], ["2026-02-10"]], dtype="datetime64[D]")
DURATIONS = numpy.array([36, -12], dtype="timedelta64[h]").astype("timedelta64[ns]")
WHOLE_NUMBERS = numpy.array([3, 10])
DECIMALS = numpy.array([1.5, numpy.nan])
NUMBERS = numpy.array([1.5])
TEXTS = numpy.array(["2026"], dtype="T")
BOOLEANS = numpy.array([True])
FUNCTION_NAME = "DatePart"
EXPECTED_HOUR = 14.0
EXPECTED_MINUTE = 30.0
EXPECTED_SECOND = 15.0
EXPECTED_MONTHS = [12.0, 1.0]
EXPECTED_GRID_MONTHS = [[1.0], [2.0]]
EXPECTED_DAYS = [1.5, -0.5]
EXPECTED_WHOLE_DURATIONS = numpy.array([3, 10], dtype="timedelta64[D]").astype("timedelta64[ns]")
EXPECTED_DECIMAL_DURATION = numpy.timedelta64(36, "h")
EXPECTED_HOUR_START = numpy.datetime64("2026-12-31T14:00:00", "ns")
EXPECTED_GRID_PERIODS = numpy.array([["2026-01-01"], ["2026-02-01"]], dtype="datetime64[D]")


@dataclass(frozen=True)
class PartCase:
	"""
	A part read from DATETIMES and DATES, and the expected first value of each.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unit
		The part to read.
	expected_datetime_part
		The part of 2026-12-31 14:30:15.
	expected_date_part
		The part of 2027-01-09.
	"""

	unit: DatePartUnit
	expected_datetime_part: float
	expected_date_part: float


PART_CASES = [
	PartCase(DatePartUnit.YEAR, 2026.0, 2027.0),
	PartCase(DatePartUnit.QUARTER, 4.0, 1.0),
	PartCase(DatePartUnit.MONTH, 12.0, 1.0),
	PartCase(DatePartUnit.WEEK, 53.0, 1.0),
	PartCase(DatePartUnit.DAY, 31.0, 9.0),
	PartCase(DatePartUnit.WEEKDAY, 4.0, 6.0),
	PartCase(DatePartUnit.DAY_OF_YEAR, 365.0, 9.0),
]


class UnknownTimeFunction(TimeFunction):
	"""
	A time function that numdaplot does not know.

	.. versionadded:: 0.1.0
	"""


@pytest.mark.parametrize("case", PART_CASES)
def test_read_date_parts_reads_each_part(case: PartCase) -> None:
	"""
	Check each date part on a datetime and on a date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The part and its expected values.
	"""
	datetime_parts = read_date_parts(DATETIMES, case.unit, FUNCTION_NAME)
	date_parts = read_date_parts(DATES, case.unit, FUNCTION_NAME)

	assert datetime_parts[0] == case.expected_datetime_part
	assert date_parts[1] == case.expected_date_part


def test_read_date_parts_reads_the_time_of_day_of_datetimes() -> None:
	"""
	Check the hour, the minute and the second.

	.. versionadded:: 0.1.0
	"""
	hours = read_date_parts(DATETIMES, DatePartUnit.HOUR, FUNCTION_NAME)
	minutes = read_date_parts(DATETIMES, DatePartUnit.MINUTE, FUNCTION_NAME)
	seconds = read_date_parts(DATETIMES, DatePartUnit.SECOND, FUNCTION_NAME)

	assert hours[0] == EXPECTED_HOUR
	assert minutes[0] == EXPECTED_MINUTE
	assert seconds[0] == EXPECTED_SECOND


def test_read_date_parts_gives_nan_for_a_missing_value() -> None:
	"""
	Check that NaT gives NaN.

	.. versionadded:: 0.1.0
	"""
	parts = read_date_parts(DATETIMES, DatePartUnit.WEEK, FUNCTION_NAME)

	nan_parts = numpy.isnan(parts)
	is_nan = bool(nan_parts[1])
	assert is_nan


def test_read_date_parts_keeps_the_shape() -> None:
	"""
	Check that a two-dimensional Array keeps its shape.

	.. versionadded:: 0.1.0
	"""
	months = read_date_parts(GRID_DATES, DatePartUnit.MONTH, FUNCTION_NAME)

	month_rows = months.tolist()
	assert month_rows == EXPECTED_GRID_MONTHS


@pytest.mark.parametrize("values", [DATES, NUMBERS])
def test_require_moments_rejects_dates_for_a_time_of_day_and_numbers(values: NDArray[numpy.generic]) -> None:
	"""
	Check that dates asked for an hour, and numbers, raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Dates or numbers.
	"""
	with pytest.raises(IncompatibleTypesError):
		require_moments(values, True, FUNCTION_NAME)


def test_find_date_periods_gives_the_first_day_of_each_period() -> None:
	"""
	Check months of a two-dimensional Array.

	.. versionadded:: 0.1.0
	"""
	periods = find_date_periods(GRID_DATES, PeriodUnit.MONTH, FUNCTION_NAME)

	same_periods = numpy.array_equal(periods, EXPECTED_GRID_PERIODS)
	is_expected = bool(same_periods)
	assert is_expected


def test_find_date_periods_gives_datetimes_for_hours() -> None:
	"""
	Check that hours keep the date and the hour, and that a missing value stays missing.

	.. versionadded:: 0.1.0
	"""
	periods = find_date_periods(DATETIMES, PeriodUnit.HOUR, FUNCTION_NAME)

	missing_periods = numpy.isnat(periods)
	is_missing = bool(missing_periods[1])
	assert periods[0] == EXPECTED_HOUR_START
	assert is_missing


def test_find_date_periods_rejects_hours_of_dates() -> None:
	"""
	Check that hours of dates raise IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		find_date_periods(DATES, PeriodUnit.HOUR, FUNCTION_NAME)


def test_count_durations_counts_in_the_unit() -> None:
	"""
	Check durations counted in days, a negative one included.

	.. versionadded:: 0.1.0
	"""
	days = count_durations(DURATIONS, DurationUnit.DAY, FUNCTION_NAME)

	day_list = days.tolist()
	assert day_list == EXPECTED_DAYS


def test_count_durations_rejects_numbers() -> None:
	"""
	Check that numbers raise IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		count_durations(NUMBERS, DurationUnit.DAY, FUNCTION_NAME)


def test_build_durations_reads_whole_numbers_exactly() -> None:
	"""
	Check integers read as days.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(WHOLE_NUMBERS, DurationUnit.DAY, FUNCTION_NAME)

	same_durations = numpy.array_equal(durations, EXPECTED_WHOLE_DURATIONS)
	is_expected = bool(same_durations)
	assert is_expected


def test_build_durations_reads_decimals_and_keeps_missing_values() -> None:
	"""
	Check that 1.5 days gives 36 hours and NaN gives NaT.

	.. versionadded:: 0.1.0
	"""
	durations = build_durations(DECIMALS, DurationUnit.DAY, FUNCTION_NAME)

	missing_durations = numpy.isnat(durations)
	is_missing = bool(missing_durations[1])
	assert durations[0] == EXPECTED_DECIMAL_DURATION
	assert is_missing


@pytest.mark.parametrize("values", [BOOLEANS, TEXTS])
def test_build_durations_rejects_booleans_and_texts(values: NDArray[numpy.generic]) -> None:
	"""
	Check that booleans and texts raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Booleans or texts.
	"""
	with pytest.raises(IncompatibleTypesError):
		build_durations(values, DurationUnit.DAY, FUNCTION_NAME)


def test_apply_time_function_hands_the_function_to_its_reader() -> None:
	"""
	Check that DatePart reads the parts.

	.. versionadded:: 0.1.0
	"""
	months = apply_time_function(DATES, DatePart(unit=DatePartUnit.MONTH))

	month_list = months.tolist()
	assert month_list == EXPECTED_MONTHS


def test_apply_time_function_refuses_an_unknown_function() -> None:
	"""
	Check that a function numdaplot does not know raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		apply_time_function(DATES, UnknownTimeFunction())
