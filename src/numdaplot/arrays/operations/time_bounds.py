"""
Refusal of dates, datetimes and durations that a count of nanoseconds cannot hold.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, time, timedelta
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.integer_bounds import find_value_bounds
from numdaplot.arrays.operations.operand import Operand
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.types.type import Type

NANOSECOND_TYPES = frozenset({Type.DATETIME, Type.DURATION})
TIME_KINDS = frozenset({"M", "m"})
NANOSECOND_DTYPES = frozenset({numpy.dtype("datetime64[ns]"), numpy.dtype("timedelta64[ns]")})
SECOND_DTYPE_FORMAT = "{kind}8[s]"
COUNT_DTYPE = numpy.dtype(numpy.int64)
COUNT_LIMITS = numpy.iinfo(COUNT_DTYPE)
# numpy keeps the lowest count for NaT, so the range is the same on both sides of zero.
HIGHEST_NANOSECONDS = int(COUNT_LIMITS.max)
LOWEST_NANOSECONDS = -HIGHEST_NANOSECONDS
FIRST_COUNT_TOO_LARGE = 2.0**63
NANOSECONDS_PER_SECOND = 10**9
HIGHEST_SECONDS = HIGHEST_NANOSECONDS // NANOSECONDS_PER_SECOND
LOWEST_SECONDS = -HIGHEST_SECONDS
LOWEST_DATETIME = datetime(1677, 9, 21, 0, 12, 43, 145225)
HIGHEST_DATETIME = datetime(2262, 4, 11, 23, 47, 16, 854775)
LONGEST_DURATION = timedelta(days=106751, seconds=85636, microseconds=854775)


def is_python_time_in_range(value: object) -> bool:
	"""
	Return whether a Python value is not a date, a datetime or a duration beyond a count of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single Python value.

	Returns
	-------
	bool
		False for a date, a datetime or a duration out of range, True for any other value.

	Examples
	--------
	>>> from datetime import datetime
	>>> from numdaplot.arrays.operations.time_bounds import is_python_time_in_range
	>>> is_python_time_in_range(datetime(2026, 1, 31))
	True
	>>> is_python_time_in_range(datetime(3000, 1, 31))
	False
	"""
	if isinstance(value, timedelta):
		duration_in_range = -LONGEST_DURATION <= value <= LONGEST_DURATION
		return duration_in_range

	if isinstance(value, datetime):
		clock_time = value.replace(tzinfo=None)
		datetime_in_range = LOWEST_DATETIME <= clock_time <= HIGHEST_DATETIME
		return datetime_in_range

	if isinstance(value, date):
		midnight = datetime.combine(value, time.min)
		date_in_range = LOWEST_DATETIME <= midnight <= HIGHEST_DATETIME
		return date_in_range

	return True


def require_stored_times_fit(single_values: list[object], stored_type: Type, operation_name: str) -> None:
	"""
	Check that Python values stored as datetimes or durations fit a count of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	single_values
		Single Python values.
	stored_type
		The type the values are stored as. Other types than ``DATETIME`` and ``DURATION`` are not checked.
	operation_name
		The operation shown in the error message.

	Raises
	------
	TimeOverflowError
		When a value is out of range.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_bounds import require_stored_times_fit
	>>> try:
	... 	require_stored_times_fit([datetime(3000, 1, 31)], ndp.Type.DATETIME, "from_list")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation from_list gives values outside the range of DATETIME, from 1677 to 2262.
	"""
	if stored_type not in NANOSECOND_TYPES:
		return

	for value in single_values:
		value_in_range = is_python_time_in_range(value)
		if not value_in_range:
			raise TimeOverflowError(operation_name, stored_type.name)


def require_nanoseconds_fit(operand: Operand, data_type: Type, operation_name: str) -> None:
	"""
	Check that the dates, datetimes or durations of an operand can be counted in nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operand
		The values of an Array, or a single value. Other values than times are not checked.
	data_type
		The type named by the error message.
	operation_name
		The operation shown in the error message.

	Raises
	------
	TimeOverflowError
		When a value is out of range. An Array in a coarser unit is compared to the second.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_bounds import require_nanoseconds_fit
	>>> try:
	... 	require_nanoseconds_fit(numpy.array(["3000-01-31"], dtype="datetime64[D]"), ndp.Type.DATE, "+")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation + gives values outside the range of DATE, from 1677 to 2262 in a calculation.
	"""
	if not isinstance(operand, numpy.ndarray):
		operand_in_range = is_python_time_in_range(operand)
		if not operand_in_range:
			raise TimeOverflowError(operation_name, data_type.name)

		return

	if operand.dtype.kind not in TIME_KINDS or operand.dtype in NANOSECOND_DTYPES:
		return

	count_bounds = find_present_bounds(operand)
	if count_bounds is None:
		return

	second_dtype = SECOND_DTYPE_FORMAT.format(kind=operand.dtype.kind)
	bound_counts = numpy.array(count_bounds, dtype=COUNT_DTYPE)
	bound_times = bound_counts.astype(operand.dtype)
	bound_seconds = bound_times.astype(second_dtype)
	second_counts = bound_seconds.astype(COUNT_DTYPE)
	low_seconds, high_seconds = find_value_bounds(second_counts)
	if low_seconds < LOWEST_SECONDS or high_seconds > HIGHEST_SECONDS:
		raise TimeOverflowError(operation_name, data_type.name)


def find_present_bounds(values: Any) -> tuple[int, int] | None:
	"""
	Return the lowest and the highest values of a calculation, times being counted in their unit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Times or integers, an array or a single value.

	Returns
	-------
	tuple[int, int] or None
		The bounds of the present values, or ``None`` when no value is present.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_bounds import find_present_bounds
	>>> find_present_bounds(numpy.array([5, "NaT", 2], dtype="timedelta64[ns]"))
	(2, 5)
	>>> find_present_bounds(3)
	(3, 3)
	"""
	array = numpy.asarray(values)
	if array.size == 0:
		return None

	if array.dtype.kind not in TIME_KINDS:
		number_bounds = find_value_bounds(array)
		return number_bounds

	counts = array.view(COUNT_DTYPE)
	low_count, high_count = find_value_bounds(counts)
	if low_count != COUNT_LIMITS.min:
		return low_count, high_count

	is_present = counts != COUNT_LIMITS.min
	present_counts = counts[is_present]
	if present_counts.size == 0:
		return None

	present_bounds = find_value_bounds(present_counts)

	return present_bounds


def require_whole_durations_fit(values: NDArray[Any], nanoseconds_per_unit: int, function_name: str) -> None:
	"""
	Check that integers read as durations in a unit fit a count of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Integers.
	nanoseconds_per_unit
		The number of nanoseconds in the unit of the integers.
	function_name
		The function shown in the error message.

	Raises
	------
	TimeOverflowError
		When a duration is out of range.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_bounds import require_whole_durations_fit
	>>> require_whole_durations_fit(numpy.array([1, 2]), 1000, "ToDuration")
	"""
	if values.size == 0:
		return

	low_value, high_value = find_value_bounds(values)
	low_count = low_value * nanoseconds_per_unit
	high_count = high_value * nanoseconds_per_unit
	if low_count < LOWEST_NANOSECONDS or high_count > HIGHEST_NANOSECONDS:
		raise TimeOverflowError(function_name, Type.DURATION.name)


def require_decimal_durations_fit(nanoseconds: NDArray[Any], function_name: str) -> None:
	"""
	Check that decimal numbers of nanoseconds fit a count of nanoseconds, an infinite number being out of range.

	.. versionadded:: 0.1.0

	Parameters
	----------
	nanoseconds
		Decimal numbers of nanoseconds, NaN for a missing value.
	function_name
		The function shown in the error message.

	Raises
	------
	TimeOverflowError
		When a duration is out of range.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_bounds import require_decimal_durations_fit
	>>> require_decimal_durations_fit(numpy.array([1.5, numpy.nan]), "ToDuration")
	"""
	magnitudes = numpy.abs(nanoseconds)
	# A comparison with NaN is False, so a missing value is never out of range.
	is_too_large = magnitudes >= FIRST_COUNT_TOO_LARGE
	has_too_large = bool(numpy.any(is_too_large))
	if has_too_large:
		raise TimeOverflowError(function_name, Type.DURATION.name)
