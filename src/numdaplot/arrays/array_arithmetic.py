"""
Arithmetic operators of an Array, with the Array on the left.

.. versionadded:: 0.1.0
"""

from typing import Self

import numpy

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.operations.integer_rules import require_opposite_fits
from numdaplot.arrays.operations.transformation import transform_values
from numdaplot.rules.rule_values import ScalarValue

ADDITION_SYMBOL = "+"
SUBTRACTION_SYMBOL = "-"
MULTIPLICATION_SYMBOL = "*"
DIVISION_SYMBOL = "/"
FLOOR_DIVISION_SYMBOL = "//"
REMAINDER_SYMBOL = "%"
POWER_SYMBOL = "**"


class ArrayArithmetic(ArrayData):
	"""
	Arithmetic operators of an Array, with the Array on the left.

	``+``, ``-``, ``*``, ``/``, ``//``, ``%``, ``**`` and the opposite ``-array``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def __add__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the sum of each value and another operand, written ``array + other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
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
		>>> prices + 5
		Array([15, 25], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.add, ADDITION_SYMBOL)

		return combined_array

	@checked_arguments
	def __sub__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the difference of each value and another operand, written ``array - other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
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
		>>> prices - 5
		Array([ 5, 15], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.subtract, SUBTRACTION_SYMBOL)

		return combined_array

	@checked_arguments
	def __mul__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the product of each value and another operand, written ``array * other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
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
		>>> prices * 2
		Array([20, 40], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.multiply, MULTIPLICATION_SYMBOL)

		return combined_array

	@checked_arguments
	def __truediv__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the quotient of each value and another operand, written ``array / other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		TimeOverflowError
			When a date or a datetime leaves 1677 to 2262, or a duration exceeds about 292 years.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> prices / 4
		Array([2.5, 5. ], dtype=FLOAT64)
		"""
		combined_array = self._combine(other, numpy.true_divide, DIVISION_SYMBOL)

		return combined_array

	@checked_arguments
	def __floordiv__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the whole quotient of each value and another operand, written ``array // other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
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
		>>> prices // 3
		Array([3, 6], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.floor_divide, FLOOR_DIVISION_SYMBOL)

		return combined_array

	@checked_arguments
	def __mod__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the remainder of each value and another operand, written ``array % other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
		IncompatibleTypesError
			When the operation does not apply to the types, such as a number and a text.
		OutOfDomainError
			When integers are divided by 0: convert them to ``FLOAT64`` first.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([10, 20])
		>>> prices % 3
		Array([1, 2], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.remainder, REMAINDER_SYMBOL)

		return combined_array

	@checked_arguments
	def __pow__(self, other: Self | ScalarValue) -> Self:
		"""
		Return the power of each value and another operand, written ``array ** other``.

		Two Arrays are combined value by value. Two Arrays of different shapes are stretched to match,
		as in numpy, with a ``BroadcastWarning``. The result follows the numpy type rules.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a ``ScalarValue``, such as ``10`` or ``2.5``.

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
		ShapeMismatchError
			When the shapes of two Arrays cannot be combined.
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
		>>> prices ** 2
		Array([100, 400], dtype=INT64)
		"""
		combined_array = self._combine(other, numpy.power, POWER_SYMBOL)

		return combined_array

	def __neg__(self) -> Self:
		"""
		Return the opposite of each value, written ``-array``.

		.. versionadded:: 0.1.0

		Returns
		-------
		Self
			A new Array.

		Raises
		------
		IncompatibleTypesError
			When the values have no opposite, such as texts or booleans.
		IntegerOverflowError
			When an integer has no opposite in its type, such as any positive ``UINT8``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> -ndp.Array.from_list([1, -2])
		Array([-1,  2], dtype=INT64)
		"""
		require_opposite_fits(self._values, SUBTRACTION_SYMBOL)
		negated_values = transform_values(self._values, numpy.negative, SUBTRACTION_SYMBOL)
		negated_array = self._wrap(negated_values)

		return negated_array
