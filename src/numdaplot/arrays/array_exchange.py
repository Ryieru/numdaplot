"""
Exchange of an Array with Python values and numpy, and comparison of two Arrays.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

import numpy
import numpy.typing

from numdaplot.argument_checks.argument_types import checked_arguments
from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.equality.equality_check import are_equal
from numdaplot.arrays.export.python_values import to_python_list
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.time_of_day import read_time_objects
from numdaplot.types.type import Type

if TYPE_CHECKING:
	from numdaplot.arrays.equality.equality import Equality

SINGLE_VALUE_COUNT = 1
FLAT_DIMENSIONS = (-1,)
EQUALITY_TARGET = "Array.is_equal other"
EQUALITY_EXPECTED = "an Array"


class ArrayExchange(ArrayData):
	"""
	Exchange of an Array with Python values and numpy, and comparison with ``is_equal``.

	.. versionadded:: 0.1.0
	"""

	def to_list(self) -> list[Any]:
		"""
		Return the values as a Python list, with one nested list per row for several dimensions.

		This is the way to loop over the values: ``for value in array.to_list()``.

		.. versionadded:: 0.1.0

		Returns
		-------
		list[Any]
			Python values, ``datetime.time`` for times of day. A missing date, datetime, duration or time of day
			becomes ``None``, a missing decimal ``nan``.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2], [3, 4]]).to_list()
		[[1, 2], [3, 4]]
		"""
		python_values = to_python_list(self._values)

		return python_values

	def to_value(self) -> Any:
		"""
		Return the single value of an Array holding exactly one value, as a Python value.

		.. versionadded:: 0.1.0

		Returns
		-------
		Any
			The value, ``None`` for a missing date, datetime or duration.

		Raises
		------
		NotSingleValueError
			When the Array does not hold exactly one value.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([3, 1, 2]).compute(ndp.Max()).to_value()
		3
		"""
		if self._values.size != SINGLE_VALUE_COUNT:
			raise NotSingleValueError(self._values.size)

		flat_values = self._values.reshape(FLAT_DIMENSIONS)
		python_values = to_python_list(flat_values)
		single_value = python_values[0]

		return single_value

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

	@checked_arguments
	def is_equal(self, equality: Equality) -> bool:
		"""
		Return whether this Array and another one have the same shape and the same values.

		Two missing values at the same position are equal.

		.. versionadded:: 0.1.0

		Parameters
		----------
		equality
			The other Array, and whether the types must also be the same.

		Returns
		-------
		bool
			True when both Arrays are equal.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> integers = ndp.Array.from_list([1, 2])
		>>> decimals = ndp.Array.from_list([1.0, 2.0])
		>>> integers.is_equal(ndp.Equality(other=decimals))
		True
		"""
		other = cast(object, equality.other)
		if not isinstance(other, ArrayData):
			raise InvalidTypeError(EQUALITY_TARGET, EQUALITY_EXPECTED, other)

		other_values = other._values
		is_equal = are_equal(self._values, other_values, equality.types)

		return is_equal
