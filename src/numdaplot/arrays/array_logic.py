"""
Boolean operators of an Array, combining the masks returned by ``check``.

.. versionadded:: 0.1.0
"""

from typing import Self

import numpy

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.operations.boolean_operands import require_booleans
from numdaplot.arrays.operations.transformation import transform_values

AND_SYMBOL = "&"
OR_SYMBOL = "|"
NOT_SYMBOL = "~"


class ArrayLogic(ArrayData):
	"""
	Boolean operators of an Array: ``&`` (and), ``|`` (or) and ``~`` (not).

	They only apply to ``BOOL`` values, such as the masks returned by ``check``.

	.. versionadded:: 0.1.0
	"""

	@checked_arguments
	def __and__(self, other: Self | bool) -> Self:
		"""
		Return True where both operands are True, written ``array & other``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``BOOL`` Array or a boolean.

		Returns
		-------
		Self
			A new ``BOOL`` Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When an operand is not a boolean.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ages = ndp.Array.from_list([15, 30, 70])
		>>> ages.check(ndp.Greater(18)) & ages.check(ndp.Less(65))
		Array([False,  True, False], dtype=BOOL)
		"""
		combined_array = self._combine_booleans(other, numpy.logical_and, AND_SYMBOL)

		return combined_array

	@checked_arguments
	def __rand__(self, other: bool) -> Self:
		"""
		Return True where both operands are True, written ``value & array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A boolean.

		Returns
		-------
		Self
			A new ``BOOL`` Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When an operand is not a boolean.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> True & ndp.Array.from_list([True, False])
		Array([ True, False], dtype=BOOL)
		"""
		combined_array = self._combine_booleans(other, numpy.logical_and, AND_SYMBOL)

		return combined_array

	@checked_arguments
	def __or__(self, other: Self | bool) -> Self:
		"""
		Return True where at least one operand is True, written ``array | other``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``BOOL`` Array or a boolean.

		Returns
		-------
		Self
			A new ``BOOL`` Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When an operand is not a boolean.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ages = ndp.Array.from_list([15, 30, 70])
		>>> ages.check(ndp.Less(18)) | ages.check(ndp.Greater(65))
		Array([ True, False,  True], dtype=BOOL)
		"""
		combined_array = self._combine_booleans(other, numpy.logical_or, OR_SYMBOL)

		return combined_array

	@checked_arguments
	def __ror__(self, other: bool) -> Self:
		"""
		Return True where at least one operand is True, written ``value | array``.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A boolean.

		Returns
		-------
		Self
			A new ``BOOL`` Array.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		IncompatibleTypesError
			When an operand is not a boolean.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> False | ndp.Array.from_list([True, False])
		Array([ True, False], dtype=BOOL)
		"""
		combined_array = self._combine_booleans(other, numpy.logical_or, OR_SYMBOL)

		return combined_array

	def __invert__(self) -> Self:
		"""
		Return True where the value is False, and False where it is True, written ``~array``.

		.. versionadded:: 0.1.0

		Returns
		-------
		Self
			A new ``BOOL`` Array.

		Raises
		------
		IncompatibleTypesError
			When the values are not booleans.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ~ndp.Array.from_list([True, False])
		Array([False,  True], dtype=BOOL)
		"""
		require_booleans([self._values], NOT_SYMBOL)
		inverted_values = transform_values(self._values, numpy.logical_not, NOT_SYMBOL)
		inverted_array = self._wrap(inverted_values)

		return inverted_array

	def _combine_booleans(self, other: object, function: numpy.ufunc, symbol: str) -> Self:
		"""
		Return a new Array combining the booleans of this Array with another boolean operand.

		Both boolean operators are symmetric, so the side of each operand does not matter.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A ``BOOL`` Array or a boolean.
		function
			``numpy.logical_and`` or ``numpy.logical_or``.
		symbol
			The operator shown in error messages.

		Returns
		-------
		Self
			The combined Array.

		Raises
		------
		IncompatibleTypesError
			When an operand is not a boolean.
		"""
		other_values = self._read_operand(other)
		require_booleans([self._values, other_values], symbol)
		combined_array = self._combine(other, function, symbol)

		return combined_array
