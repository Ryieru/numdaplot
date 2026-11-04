"""
Sorting of the values of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.arrays.axis_number import find_numpy_axis
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order

LAST_AXIS = -1


def sort_values(values: NDArray[Any], sorting: ArraySorting) -> NDArray[Any]:
	"""
	Return the values sorted inside each row, or inside each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	sorting
		The order, the axis and the place of missing values.

	Returns
	-------
	NDArray
		The sorted values, of the same shape.

	Raises
	------
	DimensionError
		When an axis is given for an Array that is not two-dimensional.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.layout.sorting_values import sort_values
	>>> sort_values(numpy.array([[3, 1], [2, 4]]), ndp.ArraySorting(axis=ndp.Axis.EACH_COLUMN))
	array([[2, 1],
	       [3, 4]])
	"""
	numpy_axis = find_numpy_axis(sorting.axis, values.ndim)
	if numpy_axis is None:
		numpy_axis = LAST_AXIS

	moved_values = numpy.moveaxis(values, numpy_axis, LAST_AXIS)
	slice_size = moved_values.shape[LAST_AXIS]
	slices = moved_values.reshape(LAST_AXIS, slice_size)
	sorted_slices = numpy.empty_like(slices)
	for i, values_slice in enumerate(slices):
		sorted_slices[i] = sort_slice(values_slice, sorting)

	sorted_moved_values = sorted_slices.reshape(moved_values.shape)
	sorted_values = numpy.moveaxis(sorted_moved_values, LAST_AXIS, numpy_axis)

	return sorted_values


def sort_slice(values: NDArray[Any], sorting: ArraySorting) -> NDArray[Any]:
	"""
	Return one-dimensional values sorted, with their missing values first or last.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		One-dimensional values.
	sorting
		The order and the place of missing values.

	Returns
	-------
	NDArray
		The sorted values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.layout.sorting_values import sort_slice
	>>> sort_slice(numpy.array([1.0, numpy.nan, 3.0]), ndp.ArraySorting(order=ndp.Order.DESCENDING))
	array([ 3.,  1., nan])
	"""
	missing = find_missing(values)
	present = ~missing
	present_values = values[present]
	missing_values = values[missing]
	ordered_values = numpy.sort(present_values)
	if sorting.order == Order.DESCENDING:
		ordered_values = ordered_values[::-1]

	parts = [ordered_values, missing_values]
	if sorting.missing == MissingPosition.FIRST:
		parts = [missing_values, ordered_values]

	sorted_values = numpy.concatenate(parts)

	return sorted_values
