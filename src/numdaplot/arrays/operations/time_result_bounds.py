"""
Refusal of the results of calculations on times that a count of nanoseconds cannot hold.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.integer_bounds import find_result_bounds, find_value_bounds
from numdaplot.arrays.operations.integer_rules import require_combination_fits
from numdaplot.arrays.operations.operand import Operand
from numdaplot.arrays.operations.time_bounds import (
	COUNT_DTYPE,
	COUNT_LIMITS,
	FIRST_COUNT_TOO_LARGE,
	HIGHEST_NANOSECONDS,
	LOWEST_NANOSECONDS,
	TIME_KINDS,
	find_present_bounds,
)
from numdaplot.errors.dates.time_overflow_error import TimeOverflowError
from numdaplot.errors.types.integer_overflow_error import IntegerOverflowError
from numdaplot.types.type import Type

DECIMAL_KIND = "f"
UNSIGNED_KIND = "u"
IGNORE_MODE = "ignore"


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
	>>> from numdaplot.arrays.operations.time_result_bounds import widen_large_integers
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


def can_integers_overflow(operands: list[Any], function: numpy.ufunc) -> bool:
	"""
	Return whether the bounds of a calculation on times and integers leave the range of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The left and the right operands, with their times in nanoseconds.
	function
		``numpy.add``, ``numpy.subtract`` or ``numpy.multiply``.

	Returns
	-------
	bool
		False when every result is in range, True when each result must be looked at.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_result_bounds import can_integers_overflow
	>>> durations = numpy.array([1000], dtype="timedelta64[ns]")
	>>> can_integers_overflow([durations, 2], numpy.multiply)
	False
	>>> can_integers_overflow([durations, 2**62], numpy.multiply)
	True
	"""
	left_operand, right_operand = operands
	left_bounds = find_present_bounds(left_operand)
	right_bounds = find_present_bounds(right_operand)
	if left_bounds is None or right_bounds is None:
		return False

	low_result, high_result = find_result_bounds(left_bounds, right_bounds, function)
	bounds_fit = LOWEST_NANOSECONDS <= low_result and high_result <= HIGHEST_NANOSECONDS

	return not bounds_fit


def find_strongest_factor(factors: NDArray[Any], function: numpy.ufunc) -> float | None:
	"""
	Return what most moves a duration away from zero among decimal factors or divisors.

	A factor that is NaN or infinite and a divisor of 0 have no result to refuse, so they are not counted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	factors
		The decimals.
	function
		``numpy.multiply`` or ``numpy.true_divide``.

	Returns
	-------
	float or None
		The number a duration is multiplied by at most, or ``None`` when no decimal gives a result.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_result_bounds import find_strongest_factor
	>>> find_strongest_factor(numpy.array([2.0, -4.0, numpy.nan]), numpy.multiply)
	4.0
	>>> find_strongest_factor(numpy.array([2.0, 0.5, 0.0]), numpy.true_divide)
	2.0
	"""
	decimals = factors.astype(numpy.float64)
	magnitudes = numpy.abs(decimals)
	if magnitudes.size == 0:
		return None

	multiplies = function == numpy.multiply
	if multiplies:
		largest_magnitude = float(magnitudes.max())
		is_finite = bool(numpy.isfinite(largest_magnitude))
		if is_finite:
			return largest_magnitude

	is_usable = numpy.isfinite(magnitudes) & (magnitudes != 0)
	usable_magnitudes = magnitudes[is_usable]
	if usable_magnitudes.size == 0:
		return None

	if multiplies:
		largest_usable = float(usable_magnitudes.max())
		return largest_usable

	smallest_divisor = float(usable_magnitudes.min())
	with numpy.errstate(all=IGNORE_MODE):
		strongest_factor = 1 / numpy.float64(smallest_divisor)

	return float(strongest_factor)


def can_decimal_factor_overflow(left_counts: Any, right_counts: Any, function: numpy.ufunc) -> bool:
	"""
	Return whether the largest duration and the strongest decimal factor leave the range of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left_counts
		The left operand: durations in nanoseconds, or decimals.
	right_counts
		The right operand: durations in nanoseconds, or decimals.
	function
		``numpy.multiply`` or ``numpy.true_divide``.

	Returns
	-------
	bool
		False when every result is in range, True when each result must be looked at.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.time_result_bounds import can_decimal_factor_overflow
	>>> durations = numpy.array([1000], dtype="timedelta64[ns]")
	>>> can_decimal_factor_overflow(durations, 2.5, numpy.multiply)
	False
	>>> can_decimal_factor_overflow(durations, 1e-300, numpy.true_divide)
	True
	"""
	left_array = numpy.asarray(left_counts)
	right_array = numpy.asarray(right_counts)
	durations, factors = left_array, right_array
	if left_array.dtype.kind == DECIMAL_KIND:
		durations, factors = right_array, left_array

	duration_bounds = find_present_bounds(durations)
	if duration_bounds is None:
		return False

	strongest_factor = find_strongest_factor(factors, function)
	if strongest_factor is None:
		return False

	low_duration, high_duration = duration_bounds
	low_magnitude = abs(low_duration)
	high_magnitude = abs(high_duration)
	longest_count = max(low_magnitude, high_magnitude)
	longest_duration = float(longest_count)
	with numpy.errstate(all=IGNORE_MODE):
		largest_estimate = longest_duration * strongest_factor

	return bool(largest_estimate >= FIRST_COUNT_TOO_LARGE)


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
	>>> from numdaplot.arrays.operations.time_result_bounds import to_counts
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
	>>> from numdaplot.arrays.operations.time_result_bounds import require_decimal_factor_fits
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
	>>> from numdaplot.arrays.operations.time_result_bounds import require_time_result_fits
	>>> durations = numpy.array([1], dtype="timedelta64[D]").astype("timedelta64[ns]")
	>>> try:
	... 	require_time_result_fits([durations, 200000], numpy.multiply, ndp.Type.DURATION, "*")
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation * gives values outside the range of DURATION, about 292 years before or after zero.
	"""
	left_operand, right_operand = operands
	left_kind = numpy.asarray(left_operand).dtype.kind
	right_kind = numpy.asarray(right_operand).dtype.kind
	has_decimal = DECIMAL_KIND in (left_kind, right_kind)
	if has_decimal:
		can_overflow = can_decimal_factor_overflow(left_operand, right_operand, function)
		if can_overflow:
			left_counts = to_counts(left_operand)
			right_counts = to_counts(right_operand)
			require_decimal_factor_fits([left_counts, right_counts], function, result_type, symbol)

		return

	# Dividing by an integer never moves a count away from zero.
	if function == numpy.true_divide:
		return

	can_overflow = can_integers_overflow(operands, function)
	if not can_overflow:
		return

	left_counts = to_counts(left_operand)
	right_counts = to_counts(right_operand)
	count_operands = list[Operand]([left_counts, right_counts])
	wrapped_counts = function(left_counts, right_counts)
	try:
		require_combination_fits(count_operands, function, wrapped_counts, symbol)
	except IntegerOverflowError as error:
		raise TimeOverflowError(symbol, result_type.name) from error

	reaches_missing_marker = wrapped_counts == COUNT_LIMITS.min
	has_marker = bool(numpy.any(reaches_missing_marker))
	if has_marker:
		raise TimeOverflowError(symbol, result_type.name)
