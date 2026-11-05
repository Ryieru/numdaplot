"""
Refusal of integer calculations whose result numpy would silently write as a wrong number.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.integer_bounds import find_result_bounds, find_sum_bounds, find_value_bounds
from numdaplot.arrays.operations.operand import Operand
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.errors.integer_overflow_error import IntegerOverflowError
from numdaplot.errors.out_of_domain_error import OutOfDomainError

SIGNED_KIND = "i"
UNSIGNED_KIND = "u"
INTEGER_KINDS = frozenset({SIGNED_KIND, UNSIGNED_KIND})
INTEGER_OR_BOOL_KINDS = frozenset({SIGNED_KIND, UNSIGNED_KIND, "b"})
POWER_NAME = "Power"
ZERO_DIVISION_NAMES = dict[numpy.ufunc, str](
	{
		numpy.floor_divide: "Floor division",
		numpy.remainder: "Remainder",
	}
)
OVERFLOWING_FUNCTIONS = frozenset({numpy.add, numpy.subtract, numpy.multiply, numpy.power, numpy.floor_divide})
PYTHON_OBJECT_DTYPE = numpy.dtype(object)
ESTIMATE_DTYPE = numpy.dtype(numpy.float64)
IGNORE_MODE = "ignore"
# A decimal estimate below half the limit cannot hide a result above it, and one above twice the limit cannot hide a
# result below it. Exact integers are computed only between both, which also avoids computing huge powers.
SAFE_ESTIMATE_RATIO = 0.5
CERTAIN_ESTIMATE_RATIO = 2


def require_defined_integers(left: Operand, right: Operand, function: numpy.ufunc) -> None:
	"""
	Check that an operation between integers has a result an integer can hold.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value.
	function
		The numpy function about to be applied.

	Raises
	------
	OutOfDomainError
		When integers are divided by 0 with ``//`` or ``%``, or raised to a negative power.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.integer_rules import require_defined_integers
	>>> try:
	... 	require_defined_integers(numpy.array([1, 2]), 0, numpy.floor_divide)
	... except ndp.OutOfDomainError as error:
	... 	print(error)
	Floor division is not defined for 0 between integers. Convert the values to FLOAT64 first.
	"""
	left_values = numpy.asarray(left)
	right_values = numpy.asarray(right)
	has_integers = left_values.dtype.kind in INTEGER_OR_BOOL_KINDS and right_values.dtype.kind in INTEGER_OR_BOOL_KINDS
	if not has_integers:
		return

	if function in ZERO_DIVISION_NAMES:
		zeros = right_values == 0
		has_zero = bool(zeros.any())
		if has_zero:
			raise OutOfDomainError(ZERO_DIVISION_NAMES[function], 0, True)

	if function == numpy.power:
		negatives = right_values < 0
		has_negative = bool(negatives.any())
		if has_negative:
			negative_values = right_values[negatives]
			first_negative = negative_values[0].item()
			raise OutOfDomainError(POWER_NAME, first_negative, True)


def require_combination_fits(operands: list[Operand], function: numpy.ufunc, result: NDArray[Any], symbol: str) -> None:
	"""
	Check that the integers of a result were not wrapped around by numpy.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The left and the right operands, each the values of an Array or a single value.
	function
		The numpy function that was applied.
	result
		Its result.
	symbol
		The operator shown in the error message.

	Raises
	------
	IntegerOverflowError
		When a result does not fit the integer type of ``result``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import require_combination_fits
	>>> require_combination_fits([numpy.array([1]), 2], numpy.add, numpy.array([3]), "+")
	"""
	if result.dtype.kind not in INTEGER_KINDS:
		return

	if function not in OVERFLOWING_FUNCTIONS:
		return

	left_operand, right_operand = operands
	left_array = numpy.asarray(left_operand)
	right_array = numpy.asarray(right_operand)
	if left_array.size == 0 or right_array.size == 0:
		return

	left_bounds = find_value_bounds(left_array)
	right_bounds = find_value_bounds(right_array)
	result_bounds = find_result_bounds(left_bounds, right_bounds, function)
	bounds_fit = do_bounds_fit(result_bounds, result)
	if bounds_fit:
		return

	left_values, right_values = numpy.broadcast_arrays(left_array, right_array)
	left_estimates = left_values.astype(ESTIMATE_DTYPE)
	right_estimates = right_values.astype(ESTIMATE_DTYPE)
	with numpy.errstate(all=IGNORE_MODE):
		estimates = function(left_estimates, right_estimates)

	doubtful = find_doubtful_estimates(estimates, result, symbol)
	has_doubt = bool(doubtful.any())
	if not has_doubt:
		return

	exact_left = left_values[doubtful].astype(PYTHON_OBJECT_DTYPE)
	exact_right = right_values[doubtful].astype(PYTHON_OBJECT_DTYPE)
	exact_values = function(exact_left, exact_right)
	require_exact_values_fit(exact_values, result, symbol)


def require_sum_fits(values: NDArray[Any], axis: int | None, result: NDArray[Any], statistic_name: str) -> None:
	"""
	Check that the integers of a sum were not wrapped around by numpy.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The summed values.
	axis
		The numpy axis reduced, or ``None`` for the whole Array.
	result
		The sum given by numpy.
	statistic_name
		Name of the statistic, shown in the error message.

	Raises
	------
	IntegerOverflowError
		When a sum does not fit the integer type of ``result``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.integer_rules import require_sum_fits
	>>> values = numpy.array([2**62, 2**62])
	>>> try:
	... 	require_sum_fits(values, None, numpy.array([0]), "Sum")
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation Sum gives values too large for INT64. Convert the values to FLOAT64 first.
	"""
	if result.dtype.kind not in INTEGER_KINDS:
		return

	if values.size == 0:
		return

	sum_bounds = find_sum_bounds(values, axis)
	bounds_fit = do_bounds_fit(sum_bounds, result)
	if bounds_fit:
		return

	decimal_values = values.astype(ESTIMATE_DTYPE)
	estimates = numpy.sum(decimal_values, axis=axis)
	estimate_values = numpy.asarray(estimates)
	doubtful = find_doubtful_estimates(estimate_values, result, statistic_name)
	has_doubt = bool(doubtful.any())
	if not has_doubt:
		return

	exact_integers = values.astype(PYTHON_OBJECT_DTYPE)
	exact_values = numpy.sum(exact_integers, axis=axis)
	exact_array = numpy.asarray(exact_values, dtype=PYTHON_OBJECT_DTYPE)
	require_exact_values_fit(exact_array, result, statistic_name)


def do_bounds_fit(bounds: tuple[int, int], result: NDArray[Any]) -> bool:
	"""
	Return whether bounds of a result stay within the limits of its integer type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bounds
		The low and the high bounds of the result.
	result
		The result computed with integers, giving the integer type.

	Returns
	-------
	bool
		True when no value can have been wrapped around.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import do_bounds_fit
	>>> do_bounds_fit((0, 127), numpy.array([0], dtype="int8"))
	True
	>>> do_bounds_fit((0, 128), numpy.array([0], dtype="int8"))
	False
	"""
	limits = numpy.iinfo(result.dtype)
	low_bound, high_bound = bounds
	bounds_fit = limits.min <= low_bound and high_bound <= limits.max

	return bounds_fit


def require_absolute_fits(values: NDArray[Any], operation_name: str) -> None:
	"""
	Check that signed integers have an absolute value of their type: the lowest integer has none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array.
	operation_name
		The operator or the function, shown in the error message.

	Raises
	------
	IntegerOverflowError
		When a value is the lowest integer of its type.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import require_absolute_fits
	>>> require_absolute_fits(numpy.array([-1, 2]), "Absolute")
	"""
	if values.dtype.kind != SIGNED_KIND:
		return

	limits = numpy.iinfo(values.dtype)
	is_lowest = values == limits.min
	has_lowest = bool(is_lowest.any())
	if has_lowest:
		values_type = from_numpy_dtype(values.dtype)
		raise IntegerOverflowError(operation_name, values_type.name)


def require_opposite_fits(values: NDArray[Any], operation_name: str) -> None:
	"""
	Check that integers have an opposite of their type: unsigned integers only have the opposite of 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array.
	operation_name
		The operator, shown in the error message.

	Raises
	------
	IntegerOverflowError
		When a value has no opposite in its type.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import require_opposite_fits
	>>> require_opposite_fits(numpy.array([0], dtype="uint8"), "-")
	"""
	require_absolute_fits(values, operation_name)
	if values.dtype.kind != UNSIGNED_KIND:
		return

	has_value_above_zero = bool(values.any())
	if has_value_above_zero:
		values_type = from_numpy_dtype(values.dtype)
		raise IntegerOverflowError(operation_name, values_type.name)


def find_doubtful_estimates(estimates: NDArray[Any], result: NDArray[Any], operation_name: str) -> NDArray[numpy.bool_]:
	"""
	Return which decimal estimates of integers need an exact calculation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	estimates
		The result computed with decimals.
	result
		The result computed with integers, giving the integer type.
	operation_name
		The operator or the statistic, shown in the error message.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each estimate too close to the limits of the type to conclude.

	Raises
	------
	IntegerOverflowError
		When an estimate is far above the limits of the type.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import find_doubtful_estimates
	>>> find_doubtful_estimates(numpy.array([1.0, 100.0]), numpy.array([1, 100], dtype="int8"), "+")
	array([False,  True])
	"""
	limits = numpy.iinfo(result.dtype)
	magnitudes = numpy.abs(estimates)
	is_certain = magnitudes >= limits.max * CERTAIN_ESTIMATE_RATIO
	has_certain_overflow = bool(numpy.any(is_certain))
	if has_certain_overflow:
		result_type = from_numpy_dtype(result.dtype)
		raise IntegerOverflowError(operation_name, result_type.name)

	is_near_limit = magnitudes >= limits.max * SAFE_ESTIMATE_RATIO
	is_below_lowest = estimates < limits.min
	doubtful = is_near_limit | is_below_lowest

	return doubtful


def require_exact_values_fit(exact_values: NDArray[Any], result: NDArray[Any], operation_name: str) -> None:
	"""
	Check that exact Python integers fit an integer type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	exact_values
		Python integers, in a numpy array of objects.
	result
		The result computed with integers, giving the integer type.
	operation_name
		The operator or the statistic, shown in the error message.

	Raises
	------
	IntegerOverflowError
		When a value is outside the limits of the type.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_rules import require_exact_values_fit
	>>> require_exact_values_fit(numpy.array([100], dtype=object), numpy.array([100], dtype="int8"), "+")
	"""
	limits = numpy.iinfo(result.dtype)
	is_above = exact_values > limits.max
	is_below = exact_values < limits.min
	is_outside = is_above | is_below
	has_outside_value = bool(numpy.any(is_outside))
	if has_outside_value:
		result_type = from_numpy_dtype(result.dtype)
		raise IntegerOverflowError(operation_name, result_type.name)
