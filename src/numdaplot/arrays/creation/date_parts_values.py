"""
Dates built from their year, their month and their day.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.date_parts import DateParts
from numdaplot.data_types.type import Type
from numdaplot.errors.rejected_dates import RejectedDate, RejectedDatePart
from numdaplot.errors.value_conversion_error import ValueConversionError

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array

DECIMAL_DTYPE = numpy.float64
WHOLE_DTYPE = numpy.int64
YEAR_DTYPE = "datetime64[Y]"
MONTH_DTYPE = "datetime64[M]"
DATE_DTYPE = "datetime64[D]"
MONTH_STEP_DTYPE = "timedelta64[M]"
DAY_STEP_DTYPE = "timedelta64[D]"
MISSING_DATE = numpy.datetime64("NaT", "D")
EPOCH_YEAR = 1970
MONTHS_PER_YEAR = 12
FIRST_YEAR = 1
LAST_YEAR = 9999
FIRST_MONTH = 1
LAST_MONTH = 12
FIRST_DAY = 1
LAST_DAY = 31
SAFE_PART = 1
YEAR_PART = "year"
MONTH_PART = "month"
DAY_PART = "day"


@dataclass(frozen=True, eq=False)
class PartNumbers:
	"""
	The year, the month and the day of each date, as flat decimals, NaN where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	years
		The years.
	months
		The months.
	days
		The days.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.date_parts_values import PartNumbers
	>>> PartNumbers(numpy.array([2025.0]), numpy.array([3.0]), numpy.array([15.0])).days
	array([15.])
	"""

	years: NDArray[numpy.float64]
	months: NDArray[numpy.float64]
	days: NDArray[numpy.float64]


def build_dates(parts: DateParts) -> NDArray[numpy.datetime64]:
	"""
	Return the dates of a year, a month and a day, missing where a part is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	parts
		The year, the month and the day of each date.

	Returns
	-------
	NDArray[numpy.datetime64]
		The dates in ``datetime64[D]``, in the shape of the parts, NaT where a part is missing.

	Raises
	------
	ValueConversionError
		At the first part that is not a whole number, then at the first year, month and day that form no date.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.date_parts_values import build_dates
	>>> years = ndp.Array.from_list([2025.0, None])
	>>> months = ndp.Array.from_list([2.0, 3.0])
	>>> days = ndp.Array.from_list([28.0, 1.0])
	>>> build_dates(ndp.DateParts(year=years, month=months, day=days))
	array(['2025-02-28',        'NaT'], dtype='datetime64[D]')
	"""
	numbers = read_part_numbers(parts)
	missing = find_missing_parts(numbers)
	require_whole_parts(numbers, missing, parts)
	safe_numbers = replace_unusable_parts(numbers, missing)
	dates = combine_parts(safe_numbers)
	require_real_dates(numbers, dates, missing, parts.year)
	present_dates = numpy.where(missing, MISSING_DATE, dates)
	dimensions = parts.year.shape.dimensions
	shaped_dates = present_dates.reshape(dimensions)

	return shaped_dates


def read_part_numbers(parts: DateParts) -> PartNumbers:
	"""
	Return the year, the month and the day of each date as flat decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	parts
		The year, the month and the day of each date.

	Returns
	-------
	PartNumbers
		The parts as float64 numbers in one dimension, NaN where missing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.date_parts_values import read_part_numbers
	>>> single = ndp.Array.from_list([[1]])
	>>> read_part_numbers(ndp.DateParts(year=single, month=single, day=single)).years
	array([1.])
	"""
	years = read_flat_decimals(parts.year)
	months = read_flat_decimals(parts.month)
	days = read_flat_decimals(parts.day)
	numbers = PartNumbers(years, months, days)

	return numbers


def read_flat_decimals(part: Array) -> NDArray[numpy.float64]:
	"""
	Return the numbers of an Array as decimals in one dimension.

	.. versionadded:: 0.1.0

	Parameters
	----------
	part
		An Array of numbers.

	Returns
	-------
	NDArray[numpy.float64]
		Its numbers, NaN where missing.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.date_parts_values import read_flat_decimals
	>>> read_flat_decimals(ndp.Array.from_list([[1, 2]]))
	array([1., 2.])
	"""
	values = part.to_numpy()
	decimals = values.astype(DECIMAL_DTYPE)
	flat_decimals = decimals.ravel()

	return flat_decimals


def find_missing_parts(numbers: PartNumbers) -> NDArray[numpy.bool_]:
	"""
	Return where a part of a date is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The parts as decimals.

	Returns
	-------
	NDArray[numpy.bool_]
		True where the year, the month or the day is NaN.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.date_parts_values import PartNumbers, find_missing_parts
	>>> find_missing_parts(PartNumbers(numpy.array([2025.0, 2025.0]), numpy.array([1.0, numpy.nan]), numpy.ones(2)))
	array([False,  True])
	"""
	missing_years = numpy.isnan(numbers.years)
	missing_months = numpy.isnan(numbers.months)
	missing_days = numpy.isnan(numbers.days)
	missing = missing_years | missing_months | missing_days

	return missing


def require_whole_parts(numbers: PartNumbers, missing: NDArray[numpy.bool_], parts: DateParts) -> None:
	"""
	Check that every present part is a whole number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The parts as decimals.
	missing
		True where a part is missing.
	parts
		The Arrays of the parts, whose types the error names.

	Raises
	------
	ValueConversionError
		At the first part that is not a whole number, the years first, then the months, then the days.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.date_parts_values import (
	... 	find_missing_parts,
	... 	read_part_numbers,
	... 	require_whole_parts,
	... )
	>>> years = ndp.Array.from_list([2025.0])
	>>> months = ndp.Array.from_list([3.0])
	>>> days = ndp.Array.from_list([3.5])
	>>> parts = ndp.DateParts(year=years, month=months, day=days)
	>>> numbers = read_part_numbers(parts)
	>>> try:
	... 	require_whole_parts(numbers, find_missing_parts(numbers), parts)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot use the FLOAT64 value 3.5 as a day: date parts must be whole numbers.
	"""
	checked_parts = (
		(YEAR_PART, numbers.years, parts.year),
		(MONTH_PART, numbers.months, parts.month),
		(DAY_PART, numbers.days, parts.day),
	)
	for part_name, part_numbers, part in checked_parts:
		rounded_numbers = numpy.floor(part_numbers)
		is_whole = (rounded_numbers == part_numbers) & numpy.isfinite(part_numbers)
		is_rejected = ~is_whole & ~missing
		has_rejected = bool(is_rejected.any())
		if not has_rejected:
			continue

		rejected_numbers = part_numbers[is_rejected]
		first_number = float(rejected_numbers[0])
		rejected_part = RejectedDatePart(part_name, first_number)
		raise ValueConversionError(part.dtype.name, Type.DATE.name, rejected_part)


def replace_unusable_parts(numbers: PartNumbers, missing: NDArray[numpy.bool_]) -> PartNumbers:
	"""
	Return the parts with 1 where a part is missing or outside its usual range, so that every date can be computed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The whole parts as decimals.
	missing
		True where a part is missing.

	Returns
	-------
	PartNumbers
		The parts, each from 1 to its largest usual value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.date_parts_values import PartNumbers, replace_unusable_parts
	>>> numbers = PartNumbers(numpy.array([2025.0]), numpy.array([13.0]), numpy.array([1.0]))
	>>> replace_unusable_parts(numbers, numpy.array([False])).months
	array([1.])
	"""
	usable_years = keep_in_range(numbers.years, missing, LAST_YEAR)
	usable_months = keep_in_range(numbers.months, missing, LAST_MONTH)
	usable_days = keep_in_range(numbers.days, missing, LAST_DAY)
	usable_numbers = PartNumbers(usable_years, usable_months, usable_days)

	return usable_numbers


def keep_in_range(
	part_numbers: NDArray[numpy.float64], missing: NDArray[numpy.bool_], last_value: int
) -> NDArray[numpy.float64]:
	"""
	Return a part with 1 where it is missing or outside 1 to its last value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	part_numbers
		The numbers of one part.
	missing
		True where a part of the date is missing.
	last_value
		The largest value of the part.

	Returns
	-------
	NDArray[numpy.float64]
		The numbers kept, 1 elsewhere.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.date_parts_values import keep_in_range
	>>> keep_in_range(numpy.array([0.0, 5.0, 40.0]), numpy.array([False, False, False]), 31)
	array([1., 5., 1.])
	"""
	is_in_range = (part_numbers >= SAFE_PART) & (part_numbers <= last_value) & ~missing
	kept_numbers = numpy.where(is_in_range, part_numbers, SAFE_PART)

	return kept_numbers


def combine_parts(numbers: PartNumbers) -> NDArray[numpy.datetime64]:
	"""
	Return the dates of whole parts, a day beyond the end of its month spilling over the next month.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		Whole parts, each in its usual range.

	Returns
	-------
	NDArray[numpy.datetime64]
		The dates in ``datetime64[D]``: the 31st of February gives the 3rd of March, 2025.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.date_parts_values import PartNumbers, combine_parts
	>>> combine_parts(PartNumbers(numpy.array([2025.0]), numpy.array([2.0]), numpy.array([31.0])))
	array(['2025-03-03'], dtype='datetime64[D]')
	"""
	whole_years = numbers.years.astype(WHOLE_DTYPE)
	whole_months = numbers.months.astype(WHOLE_DTYPE)
	whole_days = numbers.days.astype(WHOLE_DTYPE)
	years_since_epoch = whole_years - EPOCH_YEAR
	year_starts = years_since_epoch.astype(YEAR_DTYPE)
	month_steps = whole_months - FIRST_MONTH
	month_offsets = month_steps.astype(MONTH_STEP_DTYPE)
	month_starts = year_starts + month_offsets
	month_start_days = month_starts.astype(DATE_DTYPE)
	day_steps = whole_days - FIRST_DAY
	day_offsets = day_steps.astype(DAY_STEP_DTYPE)
	raw_dates = month_start_days + day_offsets
	# Some versions of the numpy stubs lose the datetime type of a sum of datetimes and durations.
	dates = cast(Any, raw_dates)

	return dates


def require_real_dates(
	numbers: PartNumbers, dates: NDArray[numpy.datetime64], missing: NDArray[numpy.bool_], year_part: Array
) -> None:
	"""
	Check that each computed date has the year, the month and the day it was built from.

	A part outside its usual range, or a day beyond the end of its month, gives another date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The whole parts, as given.
	dates
		The dates computed from the parts kept in their usual ranges.
	missing
		True where a part is missing.
	year_part
		The Array of the years, whose type the error names.

	Raises
	------
	ValueConversionError
		At the first year, month and day that form no date.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.date_parts_values import PartNumbers, combine_parts, require_real_dates
	>>> numbers = PartNumbers(numpy.array([2025.0]), numpy.array([2.0]), numpy.array([31.0]))
	>>> try:
	... 	require_real_dates(numbers, combine_parts(numbers), numpy.array([False]), ndp.Array.from_list([2025]))
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot build a DATE from the year 2025, the month 2 and the day 31.
	"""
	year_values = dates.astype(YEAR_DTYPE)
	month_values = dates.astype(MONTH_DTYPE)
	built_years = year_values.astype(WHOLE_DTYPE) + EPOCH_YEAR
	month_counts = month_values.astype(WHOLE_DTYPE)
	built_months = month_counts % MONTHS_PER_YEAR + FIRST_MONTH
	day_steps = dates - month_values.astype(DATE_DTYPE)
	built_days = day_steps.astype(WHOLE_DTYPE) + FIRST_DAY
	same_years = (built_years == numbers.years) & (numbers.years >= FIRST_YEAR)
	same_dates = same_years & (built_months == numbers.months) & (built_days == numbers.days)
	is_rejected = ~same_dates & ~missing
	has_rejected = bool(is_rejected.any())
	if not has_rejected:
		return

	rejected_positions = numpy.flatnonzero(is_rejected)
	first_position = int(rejected_positions[0])
	first_year = int(numbers.years[first_position])
	first_month = int(numbers.months[first_position])
	first_day = int(numbers.days[first_position])
	rejected_date = RejectedDate(first_year, first_month, first_day)
	raise ValueConversionError(year_part.dtype.name, Type.DATE.name, rejected_date)
