"""
Refusal of dates, datetimes and durations that a count of nanoseconds cannot hold.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, time, timedelta
from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.integer_bounds import find_value_bounds
from numdaplot.arrays.operations.integer_rules import require_combination_fits
from numdaplot.arrays.operations.operand import Operand
from numdaplot.data_types.type import Type
from numdaplot.errors.integer_overflow_error import IntegerOverflowError
from numdaplot.errors.time_overflow_error import TimeOverflowError

NANOSECOND_TYPES = frozenset({Type.DATETIME, Type.DURATION})
TIME_KINDS = frozenset({"M", "m"})
DECIMAL_KIND = "f"
UNSIGNED_KIND = "u"
IGNORE_MODE = "ignore"
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

	present_values = operand[~numpy.isnat(operand)]
	if present_values.size == 0:
		return

	second_dtype = SECOND_DTYPE_FORMAT.format(kind=operand.dtype.kind)
	seconds = present_values.astype(second_dtype)
	second_counts = seconds.astype(COUNT_DTYPE)
	low_seconds, high_seconds = find_value_bounds(second_counts)
	if low_seconds < LOWEST_SECONDS or high_seconds > HIGHEST_SECONDS:
		raise TimeOverflowError(operation_name, data_type.name)


def to_counts(values: Any) -> NDArray[Any]:
	"""
	Return values of a calculation with their times as integers, a missing time counting as 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Times in nanoseconds or numbers, an array or a single value.

	Returns
	-------
	NDArray
		The counts of nanoseconds, or the numbers.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_bounds import to_counts
	>>> to_counts(numpy.array([5, "NaT"], dtype="timedelta64[ns]"))
	array([5, 0])
	"""
	array = numpy.asarray(values)
	if array.dtype.kind not in TIME_KINDS:
		return array

	counts = array.astype(COUNT_DTYPE)
	missing = numpy.isnat(array)
	present_counts = numpy.where(missing, 0, counts)

	return present_counts


def widen_large_integers(values: Any) -> Any:
	"""
	Return numbers beside a duration as decimals when they do not fit a signed count of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Times in nanoseconds or numbers, an array or a single value.

	Returns
	-------
	Any
		Decimals for integers too large, signed integers for ``UINT64`` that fit, the values themselves otherwise.

	Raises
	------
	OverflowError
		When a Python integer is too large for a decimal.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_bounds import widen_large_integers
	>>> widen_large_integers(2**70)
	1.1805916207174113e+21
	>>> widen_large_integers(numpy.array([2], dtype="uint64"))
	array([2])
	"""
	if isinstance(values, int):
		if LOWEST_NANOSECONDS <= values <= HIGHEST_NANOSECONDS:
			return values

		return float(values)

	if not isinstance(values, numpy.ndarray):
		return values

	# isinstance leaves the array type unknown, because the values are typed Any.
	array = cast(NDArray[Any], values)
	if array.dtype.kind != UNSIGNED_KIND or array.size == 0:
		return array

	_, highest_value = find_value_bounds(array)
	if highest_value > HIGHEST_NANOSECONDS:
		large_decimals = array.astype(numpy.float64)
		return large_decimals

	signed_values = array.astype(COUNT_DTYPE)

	return signed_values


def require_decimal_factor_fits(operands: list[Any], function: numpy.ufunc, result_type: Type, symbol: str) -> None:
	"""
	Check that a duration multiplied or divided by decimals fits a count of nanoseconds.

	A factor that is NaN or infinite and a divisor of 0 have no result to refuse: they give missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The counts of the left and the right operands, one of them holding the decimals.
	function
		``numpy.multiply`` or ``numpy.true_divide``.
	result_type
		The type named by the error message.
	symbol
		The operator shown in the error message.

	Raises
	------
	TimeOverflowError
		When a result is out of range.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_bounds import require_decimal_factor_fits
	>>> operands = [numpy.array([2**62]), numpy.array([4.0])]
	>>> try:
	... 	require_decimal_factor_fits(operands, numpy.multiply, ndp.Type.DURATION, "*")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation * gives values outside the range of DURATION, about 292 years before or after zero.
	"""
	left_counts, right_counts = operands
	factors = right_counts
	if left_counts.dtype.kind == DECIMAL_KIND:
		factors = left_counts

	left_decimals = left_counts.astype(numpy.float64)
	right_decimals = right_counts.astype(numpy.float64)
	with numpy.errstate(all=IGNORE_MODE):
		estimates = function(left_decimals, right_decimals)

	has_result = numpy.isfinite(factors)
	if function == numpy.true_divide:
		has_result = has_result & (factors != 0)

	magnitudes = numpy.abs(estimates)
	is_too_large = (magnitudes >= FIRST_COUNT_TOO_LARGE) & has_result
	has_too_large = bool(numpy.any(is_too_large))
	if has_too_large:
		raise TimeOverflowError(symbol, result_type.name)


def require_time_result_fits(operands: list[Any], function: numpy.ufunc, result_type: Type, symbol: str) -> None:
	"""
	Check that the results of a calculation on times fit a count of nanoseconds, before computing them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The left and the right operands, with their times in nanoseconds.
	function
		The numpy function about to be applied.
	result_type
		The type named by the error message.
	symbol
		The operator shown in the error message.

	Raises
	------
	TimeOverflowError
		When a result is out of range.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.time_bounds import require_time_result_fits
	>>> durations = numpy.array([1], dtype="timedelta64[D]").astype("timedelta64[ns]")
	>>> try:
	... 	require_time_result_fits([durations, 200000], numpy.multiply, ndp.Type.DURATION, "*")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation * gives values outside the range of DURATION, about 292 years before or after zero.
	"""
	left_operand, right_operand = operands
	left_counts = to_counts(left_operand)
	right_counts = to_counts(right_operand)
	count_operands = list[Operand]([left_counts, right_counts])
	has_decimal = DECIMAL_KIND in (left_counts.dtype.kind, right_counts.dtype.kind)
	if has_decimal:
		require_decimal_factor_fits(count_operands, function, result_type, symbol)
		return

	# Dividing by an integer never moves a count away from zero.
	if function == numpy.true_divide:
		return

	wrapped_counts = function(left_counts, right_counts)
	try:
		require_combination_fits(count_operands, function, wrapped_counts, symbol)
	except IntegerOverflowError as error:
		raise TimeOverflowError(symbol, result_type.name) from error

	reaches_missing_marker = wrapped_counts == COUNT_LIMITS.min
	has_marker = bool(numpy.any(reaches_missing_marker))
	if has_marker:
		raise TimeOverflowError(symbol, result_type.name)


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
