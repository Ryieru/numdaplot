"""
Values stored by an Array, shared by every group of Array methods.

.. versionadded:: 0.1.0
"""

from typing import Any, Never, Self, cast

import numpy
import numpy.typing

from numdaplot.arrays.operations.combination import combine_values
from numdaplot.arrays.operations.operand import Operand
from numdaplot.arrays.shape import Shape
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.time_of_day import read_time_objects
from numdaplot.data_types.type import Type
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.rule_values import ScalarValue

CONSTRUCTOR_OPERATION = "Creating an Array with ndp.Array(...)"
CONSTRUCTOR_ALTERNATIVE = "ndp.Array.from_list, from_numpy, filled, from_range, from_spacing or random"


class ArrayData:
	"""
	Values stored by an Array, shared by every group of Array methods.

	Use ``ndp.Array`` and its ``from_*`` methods; this base class only holds the values.

	.. versionadded:: 0.1.0
	"""

	# numpy then hands every operation between an ndarray and an Array to the Array, which refuses it.
	__array_ufunc__ = None
	_values: numpy.typing.NDArray[Any]

	def __init__(self, *arguments: Never, **keyword_arguments: Never) -> None:
		"""
		Refuse the creation of an Array by its constructor: the ``from_*`` methods create Arrays.

		.. versionadded:: 0.1.0

		Parameters
		----------
		arguments
			Any value, refused.
		keyword_arguments
			Any named value, refused.

		Raises
		------
		RefusedOperationError
			Always, naming the ``from_*`` methods.
		"""
		raise RefusedOperationError(CONSTRUCTOR_OPERATION, CONSTRUCTOR_ALTERNATIVE)

	@classmethod
	def _create(cls, values: numpy.typing.NDArray[Any]) -> Self:
		"""
		Return a new Array storing numpy values without copy, made read-only.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The numpy values, of a type numdaplot supports.

		Returns
		-------
		Self
			The new Array.
		"""
		created_array = cls.__new__(cls)
		values.flags.writeable = False
		created_array._values = values

		return created_array

	@property
	def shape(self) -> Shape:
		"""
		Number of values along each dimension.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2, 3], [4, 5, 6]]).shape
		Shape(dimensions=[2, 3])
		"""
		dimensions = list(self._values.shape)
		array_shape = Shape(dimensions)

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
			A writable copy of the values. Texts use ``StringDType`` with NaN as missing value. Times of day are
			Python ``datetime.time`` objects, None where missing, as numpy has no type for them.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> values = ndp.Array.from_list([1, 2]).to_numpy()
		>>> values[0] = 99
		>>> values
		array([99,  2])
		"""
		array_type = from_numpy_dtype(self._values.dtype)
		if array_type == Type.TIME:
			time_objects = read_time_objects(self._values)
			return time_objects

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
		wrapped_array = array_class._create(values)

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
		"""
		if isinstance(other, ArrayData):
			return other._values

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
		ShapeMismatchError, IncompatibleTypesError
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
		IncompatibleTypesError
			When the operand is not accepted, as in ``combine_values``.
		"""
		left_values = self._read_operand(other)
		combined_values = combine_values(left_values, self._values, function, symbol)
		combined_array = self._wrap(combined_values)

		return combined_array


def read_stored_values(array: ArrayData) -> numpy.typing.NDArray[Any]:
	"""
	Return the values an Array stores, without copy, for the code of numdaplot that builds other objects from them.

	Unlike ``Array.to_numpy``, times of day stay stored as the time since midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		An Array.

	Returns
	-------
	numpy.typing.NDArray
		The stored values, which must not be changed.

	Examples
	--------
	>>> from datetime import time
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.array_data import read_stored_values
	>>> read_stored_values(ndp.Array.from_list([time(0, 1)]))
	array([60000000], dtype='timedelta64[us]')
	"""
	# The function lives next to the class to read its stored values on behalf of the rest of numdaplot.
	stored_values = array._values  # pyright: ignore[reportPrivateUsage]

	return stored_values
