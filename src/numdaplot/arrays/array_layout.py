"""
Changes of the layout of an Array: shape, order and distinct values.

.. versionadded:: 0.1.0
"""

import math
from typing import Self

from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.arrays.layout.sorting_values import sort_values
from numdaplot.arrays.layout.unique_values import find_unique_values
from numdaplot.arrays.shape import Shape
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError

FLAT_DIMENSIONS = (-1,)


class ArrayLayout(ArrayData):
	"""
	Changes of the layout of an Array: ``reshape``, ``transpose``, ``flatten``, ``sort`` and ``unique``.

	.. versionadded:: 0.1.0
	"""

	def reshape(self, shape: Shape) -> Self:
		"""
		Return the same values arranged in another shape, in reading order.

		.. versionadded:: 0.1.0

		Parameters
		----------
		shape
			The new shape, holding exactly as many values as the Array.

		Returns
		-------
		Self
			A new Array.

		Raises
		------
		ShapeMismatchError
			When the new shape holds another number of values.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([1, 2, 3, 4, 5, 6]).reshape(ndp.Shape((2, 3)))
		Array([[1, 2, 3],
		       [4, 5, 6]], dtype=INT64)
		"""
		new_size = math.prod(shape.dimensions)
		if new_size != self._values.size:
			raise ShapeMismatchError(self._values.shape, shape.dimensions)

		reshaped_values = self._values.reshape(shape.dimensions)
		reshaped_array = self._wrap(reshaped_values)

		return reshaped_array

	def transpose(self) -> Self:
		"""
		Return the Array with its rows turned into columns.

		A one-dimensional Array stays the same. With more dimensions, their order is reversed.

		.. versionadded:: 0.1.0

		Returns
		-------
		Self
			A new Array.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2, 3], [4, 5, 6]]).transpose()
		Array([[1, 4],
		       [2, 5],
		       [3, 6]], dtype=INT64)
		"""
		transposed_values = self._values.transpose()
		transposed_array = self._wrap(transposed_values)

		return transposed_array

	def flatten(self) -> Self:
		"""
		Return the values in a single dimension, in reading order.

		.. versionadded:: 0.1.0

		Returns
		-------
		Self
			A new one-dimensional Array.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([[1, 2], [3, 4]]).flatten()
		Array([1, 2, 3, 4], dtype=INT64)
		"""
		flat_values = self._values.reshape(FLAT_DIMENSIONS)
		flat_array = self._wrap(flat_values)

		return flat_array

	def sort(self, sorting: ArraySorting) -> Self:
		"""
		Return the values sorted inside each row, or inside each column.

		.. versionadded:: 0.1.0

		Parameters
		----------
		sorting
			The order, the axis and the place of missing values. Without axis, each row is sorted,
			which sorts a one-dimensional Array as a whole.

		Returns
		-------
		Self
			A new Array of the same shape.

		Raises
		------
		DimensionError
			When an axis is given for an Array that is not two-dimensional.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list([3.0, None, 1.0]).sort(ndp.ArraySorting(order=ndp.Order.DESCENDING))
		Array([ 3.,  1., nan], dtype=FLOAT64)
		"""
		sorted_values = sort_values(self._values, sorting)
		sorted_array = self._wrap(sorted_values)

		return sorted_array

	def unique(self) -> Self:
		"""
		Return each distinct value once, sorted, with a single missing value at the end when there is one.

		.. versionadded:: 0.1.0

		Returns
		-------
		Self
			A new one-dimensional Array.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.Array.from_list(["b", "a", "b"]).unique()
		Array(['a', 'b'], dtype=TEXT)
		"""
		unique_values = find_unique_values(self._values)
		unique_array = self._wrap(unique_values)

		return unique_array
