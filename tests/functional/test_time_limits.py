"""
Functional tests of the range of dates, datetimes and durations.

.. versionadded:: 0.1.0
"""

import warnings
from dataclasses import dataclass
from datetime import date, datetime, timedelta

import numpy
import pytest

import numdaplot as ndp

ONE_DAY = timedelta(days=1)
TWO_HUNDRED_YEARS = timedelta(days=73000)
HUNDRED_YEARS = timedelta(days=36500)
DAYS_BEYOND_RANGE = 200000
DECIMAL_DAYS_BEYOND_RANGE = 200000.0
HUGE_FACTOR = 2**70
FACTOR_ABOVE_SIGNED_INTEGERS = 2**63
TINY_DIVISOR = 1e-6
START_DATETIME = datetime(2020, 1, 1)
START_DATE = date(2020, 1, 1)
FAR_DATETIME = datetime(3000, 1, 1)
FAR_DATE = date(3000, 1, 1)
OLD_DATETIME = datetime(1600, 1, 1)
LAST_DATETIME = datetime(2262, 4, 11, 23, 47, 16)
FIRST_DATETIME = datetime(1677, 9, 21, 0, 12, 44)
LONGEST_DURATION = timedelta(days=106751)
FAR_YEAR = 3000
DAYS_OF_THREE_HUNDRED_YEARS = 110000
ONE_DAY_UNIT = ndp.DurationUnit.DAY
FAR_TEXT = "3000-01-01 10:00:00"
IMPOSSIBLE_FAR_TEXT = "3000-02-31"
COLUMN_NAME = "when"
DURATION_MESSAGE = "The operation * gives values outside the range of DURATION, about 292 years before or after zero."
DATETIME_MESSAGE = "The operation from_list gives values outside the range of DATETIME, from 1677 to 2262."
DATE_MESSAGE = "The operation + gives values outside the range of DATE, from 1677 to 2262 in a calculation."
CONVERT_MESSAGE = (
	"The operation convert gives values of the column 'when' outside the range of DATETIME, from 1677 to 2262."
)
ZERO_DIVISION_MESSAGE = "The operation / divides by zero: these values became missing."
UNDEFINED_MESSAGE = "The operation / has values without a defined result, such as 0 / 0: they became missing."


@dataclass(frozen=True)
class FactorCase:
	"""
	A calculation on a duration whose result is too large.

	.. versionadded:: 0.1.0
	"""

	symbol: str
	factor: int | float


def compute_factor_case(durations: ndp.Array, case: FactorCase) -> ndp.Array:
	"""
	Return the durations multiplied or divided by the factor of a case.

	.. versionadded:: 0.1.0

	Parameters
	----------
	durations
		The durations.
	case
		The operator and the factor.

	Returns
	-------
	ndp.Array
		The result.
	"""
	if case.symbol == "*":
		product = durations * case.factor
		return product

	quotient = durations / case.factor

	return quotient


@pytest.mark.parametrize(
	"case",
	[
		FactorCase("*", 2**60),
		FactorCase("*", DAYS_BEYOND_RANGE),
		FactorCase("*", HUGE_FACTOR),
		FactorCase("*", DECIMAL_DAYS_BEYOND_RANGE),
		FactorCase("*", 1e300),
		FactorCase("/", TINY_DIVISOR),
		FactorCase("/", 1e-300),
	],
)
def test_a_factor_giving_a_duration_too_large_is_refused(case: FactorCase) -> None:
	"""
	Check that integers and decimals giving a duration too large raise the same error.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	with pytest.raises(ndp.TimeOverflowError):
		compute_factor_case(durations, case)


def test_the_duration_error_names_the_operation_and_the_range() -> None:
	"""
	Check the message of a duration too large.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		_ = durations * DAYS_BEYOND_RANGE

	error_text = str(error_info.value)
	assert error_text == DURATION_MESSAGE


def test_an_integer_array_on_the_left_giving_a_duration_too_large_is_refused() -> None:
	"""
	Check that the order of the operands does not change the refusal.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])
	factors = ndp.Array.from_list([DAYS_BEYOND_RANGE])

	with pytest.raises(ndp.TimeOverflowError):
		_ = factors * durations


def test_unsigned_integers_above_signed_integers_are_refused_as_factors() -> None:
	"""
	Check that a ``UINT64`` factor does not wrap around to a wrong duration.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])
	factors = ndp.Array.from_list([FACTOR_ABOVE_SIGNED_INTEGERS], dtype=ndp.Type.UINT64)

	with pytest.raises(ndp.TimeOverflowError):
		_ = durations * factors


def test_small_unsigned_integers_still_multiply_a_duration() -> None:
	"""
	Check that a ``UINT64`` factor in range gives its product.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])
	factors = ndp.Array.from_list([2], dtype=ndp.Type.UINT64)

	products = durations * factors

	product_list = products.to_list()
	assert product_list == [ONE_DAY * 2]


def test_a_zero_duration_stays_zero_with_a_factor_too_large_for_integers() -> None:
	"""
	Check that a factor alone is not refused: only its results are.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([timedelta(0)])

	products = durations * HUGE_FACTOR

	product_list = products.to_list()
	assert product_list == [timedelta(0)]


def test_a_large_integer_divisor_gives_a_small_duration() -> None:
	"""
	Check that a divisor too large for integers is not an overflow.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	quotients = durations / HUGE_FACTOR

	quotient_list = quotients.to_list()
	assert quotient_list == [timedelta(0)]


def test_adding_durations_beyond_the_range_is_refused() -> None:
	"""
	Check that two durations in range can give a sum out of range.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([TWO_HUNDRED_YEARS])

	with pytest.raises(ndp.TimeOverflowError):
		_ = durations + durations


def test_subtracting_durations_beyond_the_range_is_refused() -> None:
	"""
	Check the same limit below zero.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([TWO_HUNDRED_YEARS])
	negative_durations = durations * -1

	with pytest.raises(ndp.TimeOverflowError):
		_ = negative_durations - durations


def test_opposite_values_stay_accepted_when_only_the_extremes_would_overflow() -> None:
	"""
	Check that the check looks at each sum, not at the extremes of each side.

	.. versionadded:: 0.1.0
	"""
	left = ndp.Array.from_list([TWO_HUNDRED_YEARS, -TWO_HUNDRED_YEARS])
	right = ndp.Array.from_list([-TWO_HUNDRED_YEARS, TWO_HUNDRED_YEARS])

	sums = left + right

	sum_list = sums.to_list()
	assert sum_list == [timedelta(0), timedelta(0)]


def test_adding_a_duration_beyond_the_last_datetime_is_refused() -> None:
	"""
	Check that a datetime cannot go past 2262.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([START_DATETIME])
	durations = ndp.Array.from_list([TWO_HUNDRED_YEARS])
	later_moments = moments + durations

	with pytest.raises(ndp.TimeOverflowError):
		_ = later_moments + HUNDRED_YEARS


def test_subtracting_dates_too_far_apart_is_refused() -> None:
	"""
	Check that two datetimes in range can be too far apart for a duration.

	.. versionadded:: 0.1.0
	"""
	late_moments = ndp.Array.from_list([datetime(2200, 1, 1)])
	early_moments = ndp.Array.from_list([datetime(1700, 1, 1)])

	with pytest.raises(ndp.TimeOverflowError):
		_ = late_moments - early_moments


def test_a_single_datetime_out_of_range_is_refused_in_a_calculation() -> None:
	"""
	Check a single Python value beside an Array.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([START_DATETIME])

	with pytest.raises(ndp.TimeOverflowError):
		_ = moments - FAR_DATETIME


def test_a_single_duration_out_of_range_is_refused_in_a_calculation() -> None:
	"""
	Check a single Python duration beside an Array.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	with pytest.raises(ndp.TimeOverflowError):
		_ = durations + timedelta(days=DAYS_BEYOND_RANGE)


def test_a_date_out_of_range_is_stored_in_days() -> None:
	"""
	Check that a ``DATE`` is not limited by the range of nanoseconds when it is only stored.

	.. versionadded:: 0.1.0
	"""
	dates = ndp.Array.from_list([FAR_DATE])

	date_list = dates.to_list()
	assert date_list == [FAR_DATE]


def test_a_calculation_on_a_date_out_of_range_is_refused() -> None:
	"""
	Check the message naming the limit of a calculation on dates.

	.. versionadded:: 0.1.0
	"""
	dates = ndp.Array.from_list([FAR_DATE])

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		_ = dates + ONE_DAY

	error_text = str(error_info.value)
	assert error_text == DATE_MESSAGE


def test_missing_values_are_not_counted_in_the_range() -> None:
	"""
	Check that a missing duration stays missing and is never refused.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([None, ONE_DAY])

	products = durations * 2

	product_list = products.to_list()
	assert product_list == [None, ONE_DAY * 2]


@pytest.mark.parametrize("far_value", [FAR_DATETIME, OLD_DATETIME, timedelta(days=DAYS_BEYOND_RANGE)])
def test_from_list_refuses_a_value_out_of_range(far_value: datetime | timedelta) -> None:
	"""
	Check that a value is not stored as a wrong datetime or duration.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.from_list([far_value])


def test_from_list_names_the_range_of_datetimes() -> None:
	"""
	Check the message of a datetime out of range.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError) as error_info:
		ndp.Array.from_list([FAR_DATETIME])

	error_text = str(error_info.value)
	assert error_text == DATETIME_MESSAGE


def test_from_list_refuses_a_date_stored_as_datetime_out_of_range() -> None:
	"""
	Check a date that fits ``DATE`` but not the requested ``DATETIME``.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.from_list([FAR_DATE], dtype=ndp.Type.DATETIME)


@pytest.mark.parametrize("edge_value", [LAST_DATETIME, FIRST_DATETIME, LONGEST_DURATION, -LONGEST_DURATION])
def test_from_list_keeps_the_last_values_of_the_range(edge_value: datetime | timedelta) -> None:
	"""
	Check that the limits themselves stay accepted.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([edge_value])

	value_list = values.to_list()
	assert value_list == [edge_value]


def test_filled_refuses_a_value_out_of_range() -> None:
	"""
	Check that ``Array.filled`` follows ``Array.from_list``.

	.. versionadded:: 0.1.0
	"""
	shape = ndp.Shape([2])

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.filled(shape, FAR_DATETIME)


def test_replace_refuses_a_value_out_of_range() -> None:
	"""
	Check that ``Array.replace`` does not store a wrong datetime.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([START_DATETIME])
	first_moment = ndp.Region(rows=ndp.Index(0))
	replacement = ndp.Replacement(region=first_moment, value=FAR_DATETIME)

	with pytest.raises(ndp.TimeOverflowError):
		moments.replace(replacement)


@pytest.mark.parametrize(
	"numbers",
	[
		[DAYS_OF_THREE_HUNDRED_YEARS],
		[-DAYS_OF_THREE_HUNDRED_YEARS],
		[2**62],
		[float(DAYS_OF_THREE_HUNDRED_YEARS)],
		[numpy.inf],
	],
)
def test_to_duration_refuses_a_number_out_of_range(numbers: list[int] | list[float]) -> None:
	"""
	Check integers and decimals read as durations too large.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list(numbers)
	function = ndp.ToDuration(unit=ONE_DAY_UNIT)

	with pytest.raises(ndp.TimeOverflowError):
		values.apply(function)


def test_to_duration_refuses_unsigned_integers_above_signed_integers() -> None:
	"""
	Check that a ``UINT64`` number does not wrap around before being read as a duration.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([FACTOR_ABOVE_SIGNED_INTEGERS], dtype=ndp.Type.UINT64)
	function = ndp.ToDuration(unit=ndp.DurationUnit.SECOND)

	with pytest.raises(ndp.TimeOverflowError):
		values.apply(function)


def test_to_duration_keeps_missing_numbers_missing() -> None:
	"""
	Check that a missing number is never out of range.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([None, 1.0])
	function = ndp.ToDuration(unit=ONE_DAY_UNIT)

	durations = values.apply(function)

	duration_list = durations.to_list()
	assert duration_list == [None, ONE_DAY]


def build_text_table(text: str) -> ndp.Table:
	"""
	Return a Table with one text column holding one text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of the column.

	Returns
	-------
	ndp.Table
		The Table.
	"""
	texts = ndp.Array.from_list([text])
	table = ndp.Table.from_arrays({COLUMN_NAME: texts})

	return table


@pytest.mark.parametrize(
	"date_format",
	[None, ndp.DateFormat.YEAR_MONTH_DAY_TIME, ndp.CustomDateFormat("%Y-%m-%d %H:%M:%S")],
)
def test_convert_refuses_a_text_read_as_a_datetime_out_of_range(
	date_format: ndp.DateFormat | ndp.CustomDateFormat | None,
) -> None:
	"""
	Check every way to read a text with the same error on every version of pandas.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME, format=date_format)

	with pytest.raises(ndp.TimeOverflowError):
		table.convert(conversion)


def test_convert_names_the_column_out_of_range() -> None:
	"""
	Check the message of a column out of range.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		table.convert(conversion)

	error_text = str(error_info.value)
	assert error_text == CONVERT_MESSAGE


def test_convert_refuses_dates_out_of_range_as_datetimes() -> None:
	"""
	Check dates that ``DATE`` holds but ``DATETIME`` cannot.

	.. versionadded:: 0.1.0
	"""
	dates = ndp.Array.from_list([FAR_DATE])
	table = ndp.Table.from_arrays({COLUMN_NAME: dates})
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.TimeOverflowError):
		table.convert(conversion)


def test_convert_still_refuses_an_impossible_date_as_unreadable() -> None:
	"""
	Check that a text that is not a real date keeps its error, whatever its year.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(IMPOSSIBLE_FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.ValueConversionError):
		table.convert(conversion)


def test_a_duration_divided_by_a_single_zero_warns_of_a_missing_value() -> None:
	"""
	Check that the warning names what the value became.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	with pytest.warns(ndp.CalculationWarning) as caught_warnings:
		quotients = durations / 0

	warning_text = str(caught_warnings[0].message)
	quotient_list = quotients.to_list()
	assert warning_text == ZERO_DIVISION_MESSAGE
	assert quotient_list == [None]


def test_a_zero_duration_divided_by_a_single_zero_warns_of_a_missing_value() -> None:
	"""
	Check the warning of 0 / 0.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([timedelta(0)])

	with pytest.warns(ndp.CalculationWarning) as caught_warnings:
		_ = durations / 0.0

	warning_text = str(caught_warnings[0].message)
	assert warning_text == UNDEFINED_MESSAGE


@pytest.mark.parametrize("factor", [numpy.nan, numpy.inf])
def test_a_factor_without_a_result_gives_a_missing_value_without_warning(factor: float) -> None:
	"""
	Check that NaN and an infinite factor are not refused, as on decimals.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([ONE_DAY])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		products = durations * factor

	product_list = products.to_list()
	assert product_list == [None]
	assert caught_warnings == []
