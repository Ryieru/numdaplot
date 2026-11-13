"""
Unit tests of the dates built from their year, their month and their day.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp
from numdaplot.arrays.creation.date_parts_values import (
	PartNumbers,
	build_dates,
	combine_parts,
	find_missing_parts,
	keep_in_range,
	read_flat_decimals,
	read_part_numbers,
	replace_unusable_parts,
	require_real_dates,
	require_whole_parts,
)
from numdaplot.errors.dates.rejected_dates import RejectedDate, RejectedDatePart
from numdaplot.errors.types.value_conversion_error import ValueConversionError

GRID_YEARS = ndp.Array.from_list([[2025, 2025], [2024, 1]])
GRID_MONTHS = ndp.Array.from_list([[1, 12], [2, 1]])
GRID_DAYS = ndp.Array.from_list([[31, 25], [29, 1]])
EXPECTED_GRID_DATES = [["2025-01-31", "2025-12-25"], ["2024-02-29", "0001-01-01"]]
DATE_TEXT_DTYPE = "U10"
DECIMAL_YEARS = ndp.Array.from_list([2025.0, None])
DECIMAL_MONTHS = ndp.Array.from_list([3.0, 3.0])
DECIMAL_DAYS = ndp.Array.from_list([1.0, 1.0])
EXPECTED_MISSING_DATES = [False, True]
ONE_YEAR = ndp.Array.from_list([2025])
ONE_MONTH = ndp.Array.from_list([2])
HALF_DAY = ndp.Array.from_list([3.5])
EXPECTED_HALF_DAY = RejectedDatePart("day", 3.5)
NO_MISSING = numpy.array([False])
FEBRUARY_31 = PartNumbers(numpy.array([2025.0]), numpy.array([2.0]), numpy.array([31.0]))
EXPECTED_FEBRUARY_31 = RejectedDate(2025, 2, 31)
EXPECTED_MARCH_3 = numpy.datetime64("2025-03-03", "D")
MONTH_13 = PartNumbers(numpy.array([2025.0]), numpy.array([13.0]), numpy.array([1.0]))
YEAR_0 = PartNumbers(numpy.array([0.0]), numpy.array([1.0]), numpy.array([1.0]))
YEAR_10000 = PartNumbers(numpy.array([10000.0]), numpy.array([1.0]), numpy.array([1.0]))
EXPECTED_SAFE_MONTHS = [1.0]
RANGE_NUMBERS = numpy.array([0.0, 5.0, 40.0, numpy.nan])
RANGE_MISSING = numpy.array([False, False, False, True])
EXPECTED_KEPT_NUMBERS = [1.0, 5.0, 1.0, 1.0]
LAST_DAY = 31


def test_build_dates_keeps_the_shape_of_the_parts() -> None:
	"""
	Check two-dimensional parts, a leap day and the year 1.

	.. versionadded:: 0.1.0
	"""
	parts = ndp.DateParts(year=GRID_YEARS, month=GRID_MONTHS, day=GRID_DAYS)

	dates = build_dates(parts)

	date_texts = dates.astype(DATE_TEXT_DTYPE)
	date_list = date_texts.tolist()
	assert date_list == EXPECTED_GRID_DATES


def test_build_dates_gives_a_missing_date_for_a_missing_part() -> None:
	"""
	Check that a missing year gives NaT.

	.. versionadded:: 0.1.0
	"""
	parts = ndp.DateParts(year=DECIMAL_YEARS, month=DECIMAL_MONTHS, day=DECIMAL_DAYS)

	dates = build_dates(parts)

	missing_dates = numpy.isnat(dates)
	missing_list = missing_dates.tolist()
	assert missing_list == EXPECTED_MISSING_DATES


def test_require_whole_parts_names_a_day_that_is_not_whole() -> None:
	"""
	Check that the day 3.5 raises ValueConversionError with the part and the value.

	.. versionadded:: 0.1.0
	"""
	parts = ndp.DateParts(year=ONE_YEAR, month=ONE_MONTH, day=HALF_DAY)
	numbers = read_part_numbers(parts)

	with pytest.raises(ValueConversionError) as error_info:
		require_whole_parts(numbers, NO_MISSING, parts)

	assert error_info.value.rejected_value == EXPECTED_HALF_DAY


def test_combine_parts_spills_a_day_beyond_its_month() -> None:
	"""
	Check that the 31st of February gives the 3rd of March, which the check then refuses.

	.. versionadded:: 0.1.0
	"""
	dates = combine_parts(FEBRUARY_31)

	assert dates[0] == EXPECTED_MARCH_3


@pytest.mark.parametrize("numbers", [FEBRUARY_31, MONTH_13, YEAR_0, YEAR_10000])
def test_require_real_dates_rejects_parts_that_form_no_date(numbers: PartNumbers) -> None:
	"""
	Check the 31st of February, a month 13 and the years 0 and 10000.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		Parts that form no date.
	"""
	usable_numbers = replace_unusable_parts(numbers, NO_MISSING)
	dates = combine_parts(usable_numbers)

	with pytest.raises(ValueConversionError):
		require_real_dates(numbers, dates, NO_MISSING, ONE_YEAR)


def test_require_real_dates_names_the_first_impossible_date() -> None:
	"""
	Check the rejected value of the 31st of February.

	.. versionadded:: 0.1.0
	"""
	dates = combine_parts(FEBRUARY_31)

	with pytest.raises(ValueConversionError) as error_info:
		require_real_dates(FEBRUARY_31, dates, NO_MISSING, ONE_YEAR)

	assert error_info.value.rejected_value == EXPECTED_FEBRUARY_31


def test_replace_unusable_parts_puts_one_outside_the_usual_range() -> None:
	"""
	Check that the month 13 becomes 1 to be computed safely.

	.. versionadded:: 0.1.0
	"""
	usable_numbers = replace_unusable_parts(MONTH_13, NO_MISSING)

	usable_months = usable_numbers.months.tolist()
	assert usable_months == EXPECTED_SAFE_MONTHS


def test_keep_in_range_puts_one_where_missing_or_out_of_range() -> None:
	"""
	Check 0, a usual value, 40 and NaN for days.

	.. versionadded:: 0.1.0
	"""
	kept_numbers = keep_in_range(RANGE_NUMBERS, RANGE_MISSING, LAST_DAY)

	kept_list = kept_numbers.tolist()
	assert kept_list == EXPECTED_KEPT_NUMBERS


def test_find_missing_parts_marks_any_missing_part() -> None:
	"""
	Check that a missing year marks the date as missing.

	.. versionadded:: 0.1.0
	"""
	parts = ndp.DateParts(year=DECIMAL_YEARS, month=DECIMAL_MONTHS, day=DECIMAL_DAYS)
	numbers = read_part_numbers(parts)

	missing = find_missing_parts(numbers)

	missing_list = missing.tolist()
	assert missing_list == EXPECTED_MISSING_DATES


def test_read_flat_decimals_gives_one_dimension() -> None:
	"""
	Check that a grid of integers becomes flat decimals.

	.. versionadded:: 0.1.0
	"""
	decimals = read_flat_decimals(GRID_YEARS)

	dimension_count = decimals.ndim
	assert dimension_count == 1
