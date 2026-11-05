"""
Bounds of an integer result, found from the lowest and the highest values of its operands.

.. versionadded:: 0.1.0
"""

import math
from typing import Any

import numpy
from numpy.typing import NDArray

# A power above this number of bits fits no integer type, and is not worth computing exactly.
LARGEST_COMPUTED_BITS = 65
BEYOND_EVERY_INTEGER = 2**LARGEST_COMPUTED_BITS


def find_value_bounds(values: NDArray[Any]) -> tuple[int, int]:
	"""
	Return the lowest and the highest values of integers or booleans, as Python integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		At least one integer or boolean.

	Returns
	-------
	tuple[int, int]
		The lowest and the highest values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_bounds import find_value_bounds
	>>> find_value_bounds(numpy.array([3, -1, 2]))
	(-1, 3)
	"""
	lowest_value = values.min()
	highest_value = values.max()
	low_bound = int(lowest_value)
	high_bound = int(highest_value)

	return low_bound, high_bound


def find_result_bounds(left: tuple[int, int], right: tuple[int, int], function: numpy.ufunc) -> tuple[int, int]:
	"""
	Return bounds that every result of an integer function stays within.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The bounds of the left operand.
	right
		The bounds of the right operand. No divisor is 0 and no power is negative.
	function
		``numpy.add``, ``numpy.subtract``, ``numpy.multiply``, ``numpy.floor_divide`` or ``numpy.power``.

	Returns
	-------
	tuple[int, int]
		The low and the high bounds.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_bounds import find_result_bounds
	>>> find_result_bounds((-2, 3), (4, 5), numpy.multiply)
	(-10, 15)
	"""
	left_low, left_high = left
	right_low, right_high = right
	if function == numpy.add:
		sum_bounds = (left_low + right_low, left_high + right_high)
		return sum_bounds

	if function == numpy.subtract:
		difference_bounds = (left_low - right_high, left_high - right_low)
		return difference_bounds

	if function == numpy.multiply:
		products = [left_low * right_low, left_low * right_high, left_high * right_low, left_high * right_high]
		lowest_product = min(products)
		highest_product = max(products)
		return lowest_product, highest_product

	left_magnitude = max(abs(left_low), abs(left_high))
	if function == numpy.floor_divide:
		has_negative = left_low < 0 or right_low < 0
		lowest_quotient = -left_magnitude if has_negative else 0
		return lowest_quotient, left_magnitude

	highest_power = find_power_bound(left_magnitude, right_high)
	lowest_power = -highest_power if left_low < 0 else 0

	return lowest_power, highest_power


def find_power_bound(magnitude: int, power: int) -> int:
	"""
	Return a bound of the absolute value of integers raised to a power.

	.. versionadded:: 0.1.0

	Parameters
	----------
	magnitude
		The highest absolute value of the integers.
	power
		The highest power, 0 or more.

	Returns
	-------
	int
		The bound, or a number beyond every integer type when the exact bound would be huge.

	Examples
	--------
	>>> from numdaplot.arrays.operations.integer_bounds import find_power_bound
	>>> find_power_bound(2, 10)
	1024
	>>> find_power_bound(3, 10**18) > 2**64
	True
	"""
	if magnitude <= 1:
		return 1

	magnitude_bits = math.log2(magnitude)
	power_bits = power * magnitude_bits
	if power_bits > LARGEST_COMPUTED_BITS:
		return BEYOND_EVERY_INTEGER

	power_bound = magnitude**power

	return power_bound


def find_sum_bounds(values: NDArray[Any], axis: int | None) -> tuple[int, int]:
	"""
	Return bounds that every sum of integers or booleans stays within.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		At least one integer or boolean.
	axis
		The numpy axis reduced, or ``None`` for the whole Array.

	Returns
	-------
	tuple[int, int]
		The low and the high bounds.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.integer_bounds import find_sum_bounds
	>>> find_sum_bounds(numpy.array([[1, 2], [-3, 4]]), None)
	(-12, 16)
	>>> find_sum_bounds(numpy.array([[1, 2], [-3, 4]]), 1)
	(-6, 8)
	"""
	value_count = values.size if axis is None else values.shape[axis]
	low_value, high_value = find_value_bounds(values)
	low_bound = min(low_value, 0) * value_count
	high_bound = max(high_value, 0) * value_count

	return low_bound, high_bound
