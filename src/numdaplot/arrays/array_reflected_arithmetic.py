"""
Arithmetic operators of an Array, with a single value on the left.

.. versionadded:: 0.1.0
"""

from typing import Self

import numpy

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array_arithmetic import (
	ADDITION_SYMBOL,
	DIVISION_SYMBOL,
	FLOOR_DIVISION_SYMBOL,
	MULTIPLICATION_SYMBOL,
	POWER_SYMBOL,
	REMAINDER_SYMBOL,
	SUBTRACTION_SYMBOL,
)
from numdaplot.arrays.array_data import ArrayData
from numdaplot.rules.rule_values import ScalarValue


class ArrayReflectedArithmetic(ArrayData):
	"""
	Arithmetic operators of an Array with a single value on the left, such as ``100 - array``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def __radd__(self, other: ScalarValue) -> Self:
		"""
		Return the sum of a single value and each value, written ``value + array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		IntegerOverflowError
			When a result does not fit its integer type, which refuses to wrap around to a wrong number.
		TimeOverflowError
			When a date or a datetime leaves 1677 to 2262, a duration exceeds about 292 years, or a time of day moves
			past midnight.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 5 + prices
		Array([15, 25], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.add, ADDITION_SYMBOL)

		return combined_array

	@checked_arguments
	def __rsub__(self, other: ScalarValue) -> Self:
		"""
		Return the difference of a single value and each value, written ``value - array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		IntegerOverflowError
			When a result does not fit its integer type, which refuses to wrap around to a wrong number.
		TimeOverflowError
			When a date or a datetime leaves 1677 to 2262, a duration exceeds about 292 years, or a time of day moves
			past midnight.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 100 - prices
		Array([90, 80], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.subtract, SUBTRACTION_SYMBOL)

		return combined_array

	@checked_arguments
	def __rmul__(self, other: ScalarValue) -> Self:
		"""
		Return the product of a single value and each value, written ``value * array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		IntegerOverflowError
			When a result does not fit its integer type, which refuses to wrap around to a wrong number.
		TimeOverflowError
			When a date or a datetime leaves 1677 to 2262, or a duration exceeds about 292 years.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 2 * prices
		Array([20, 40], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.multiply, MULTIPLICATION_SYMBOL)

		return combined_array

	@checked_arguments
	def __rtruediv__(self, other: ScalarValue) -> Self:
		"""
		Return the quotient of a single value and each value, written ``value / array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 100 / prices
		Array([10.,  5.], dtype=FLOAT64)
		"""
		combined_array = self._combine_reflected(other, numpy.true_divide, DIVISION_SYMBOL)

		return combined_array

	@checked_arguments
	def __rfloordiv__(self, other: ScalarValue) -> Self:
		"""
		Return the whole quotient of a single value and each value, written ``value // array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		OutOfDomainError
			When integers are divided by 0: convert them to ``FLOAT64`` first.
		IntegerOverflowError
			When a result does not fit its integer type, which refuses to wrap around to a wrong number.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 100 // prices
		Array([10,  5], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.floor_divide, FLOOR_DIVISION_SYMBOL)

		return combined_array

	@checked_arguments
	def __rmod__(self, other: ScalarValue) -> Self:
		"""
		Return the remainder of a single value and each value, written ``value % array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		OutOfDomainError
			When integers are divided by 0: convert them to ``FLOAT64`` first.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 25 % prices
		Array([5, 5], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.remainder, REMAINDER_SYMBOL)

		return combined_array

	@checked_arguments
	def __rpow__(self, other: ScalarValue) -> Self:
		"""
		Return the power of a single value and each value, written ``value ** array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``ScalarValue``, such as ``10`` or ``2.5``, on the left of the operator.

		Returns
		-------
		Self
			A new Array.

		Warns
		-----
		CalculationWarning
			When values of decimals become NaN or an infinite value.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		OutOfDomainError
			When integers are raised to a negative power: convert them to ``FLOAT64`` first.
		IntegerOverflowError
			When a result does not fit its integer type, which refuses to wrap around to a wrong number.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> 2 ** prices
		Array([   1024, 1048576], dtype=INT64)
		"""
		combined_array = self._combine_reflected(other, numpy.power, POWER_SYMBOL)

		return combined_array
