"""
Values stored by an Array, shared by every group of Array methods.

.. versionadded:: 0.1.0
"""

from typing import Any, Self, cast

import numpy
import numpy.typing

from numdaplot.arrays.operations.combination import combine_values
from numdaplot.arrays.operations.operand import Operand, require_single_value
from numdaplot.arrays.shape import Shape
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.rules.rule_values import ScalarValue


class ArrayData:
	"""
	Values stored by an Array, shared by every group of Array methods.

	Use ``ndp.Array`` and its ``from_*`` methods; this base class only holds the values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The numpy values, stored without copy and made read-only.
	"""

	# numpy then hands every operation between an ndarray and an Array to the Array, which refuses it.
	__array_ufunc__ = None

	def __init__(self, values: numpy.typing.NDArray[Any]) -> None:
		"""
		Store numpy values without copy and make them read-only.

		The ``from_*`` methods create Arrays; this constructor is reserved to numdaplot.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The numpy values, of a type numdaplot supports.
		"""
		values.flags.writeable = False
		self._values = values

	@property
	def shape(self) -> Shape:
		"""
		Number of values along each dimension.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2, 3], [4, 5, 6]]).shape
		Shape(dimensions=(2, 3))
		"""
		array_shape = Shape(self._values.shape)

		return array_shape

	@property
	def dtype(self) -> Type:
		"""
		Type of the values.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([1.5, 2.0]).dtype
		<Type.FLOAT64: 10>
		"""
		array_type = from_numpy_dtype(self._values.dtype)

		return array_type

	def to_numpy(self) -> numpy.typing.NDArray[Any]:
		"""
		Return a numpy copy of the values; changing it never changes the Array.

		.. versionadded:: 0.1.0

		Returns
		-------
		numpy.typing.NDArray
			A writable copy of the values.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> values = ndp.Array.from_list([1, 2]).to_numpy()
		>>> values[0] = 99
		>>> values
		array([99,  2])
		"""
		copied_values = self._values.copy()

		return copied_values

	def _wrap(self, values: numpy.typing.NDArray[Any]) -> Self:
		"""
		Return a new Array of the same class holding other values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The numpy values of the new Array, stored without copy.

		Returns
		-------
		Self
			The new Array.
		"""
		array_class = type(self)
		wrapped_array = array_class(values)

		return wrapped_array

	def _read_operand(self, other: object) -> Operand:
		"""
		Return the values of an Array, or check that a value is a single value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a single value.

		Returns
		-------
		Operand
			The numpy values of the Array, or the single value itself.

		Raises
		------
		UnsupportedOperandError
			When ``other`` is neither an Array nor a single value.
		"""
		if isinstance(other, ArrayData):
			return other._values

		require_single_value(other)
		single_value = cast(ScalarValue, other)

		return single_value

	def _combine(self, other: object, function: numpy.ufunc, symbol: str) -> Self:
		"""
		Return a new Array combining this Array, on the left, with another operand.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a single value, on the right.
		function
			The numpy function, such as ``numpy.add``.
		symbol
			The operator shown in error messages, such as ``"+"``.

		Returns
		-------
		Self
			The combined Array.

		Raises
		------
		UnsupportedOperandError, ShapeMismatchError, IncompatibleTypesError
			When the operand is not accepted, as in ``combine_values``.
		"""
		right_values = self._read_operand(other)
		combined_values = combine_values(self._values, right_values, function, symbol)
		combined_array = self._wrap(combined_values)

		return combined_array

	def _combine_reflected(self, other: object, function: numpy.ufunc, symbol: str) -> Self:
		"""
		Return a new Array combining another operand, on the left, with this Array.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A single value, on the left.
		function
			The numpy function, such as ``numpy.subtract``.
		symbol
			The operator shown in error messages, such as ``"-"``.

		Returns
		-------
		Self
			The combined Array.

		Raises
		------
		UnsupportedOperandError, IncompatibleTypesError
			When the operand is not accepted, as in ``combine_values``.
		"""
		left_values = self._read_operand(other)
		combined_values = combine_values(left_values, self._values, function, symbol)
		combined_array = self._wrap(combined_values)

		return combined_array
