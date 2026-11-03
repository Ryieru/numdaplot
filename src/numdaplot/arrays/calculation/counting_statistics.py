"""
Statistics counting the values of an Array: count, distinct count, most frequent value and its count.

Each function ignores missing values and reduces the whole Array when ``axis`` is ``None``.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.statistics.statistic import Statistic

LAST_AXIS = -1
NO_VALUE_COUNT = 0


def compute_count(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the number of present values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``Count`` statistic.

	Returns
	-------
	Any
		A single count, or one count per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.counting_statistics import compute_count
	>>> compute_count(numpy.array([1.0, numpy.nan]), None, ndp.Count())
	np.int64(1)
	"""
	missing = find_missing(values)
	present = ~missing
	present_count = numpy.sum(present, axis=axis)

	return present_count


def compute_count_distinct(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the number of distinct present values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``CountDistinct`` statistic.

	Returns
	-------
	Any
		A single count, or one count per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.counting_statistics import compute_count_distinct
	>>> compute_count_distinct(numpy.array([1, 1, 2]), None, ndp.CountDistinct())
	2
	"""
	distinct_counts = apply_to_each_slice(values, axis, count_distinct_values)

	return distinct_counts


def compute_most_frequent(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the present value appearing the most often, the lowest one in case of a tie.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array, at least one present value per slice.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``MostFrequent`` statistic.

	Returns
	-------
	Any
		A single value, or one value per reduced slice.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.counting_statistics import compute_most_frequent
	>>> compute_most_frequent(numpy.array([3, 1, 3]), None, ndp.MostFrequent())
	np.int64(3)
	"""
	most_frequent_values = apply_to_each_slice(values, axis, find_most_frequent_value)

	return most_frequent_values


def compute_most_frequent_count(values: NDArray[Any], axis: int | None, statistic: Statistic) -> Any:
	"""
	Return the number of times the most frequent present value appears.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic
		The ``MostFrequentCount`` statistic.

	Returns
	-------
	Any
		A single count, or one count per reduced slice. 0 when there is no present value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.counting_statistics import compute_most_frequent_count
	>>> compute_most_frequent_count(numpy.array([3, 1, 3]), None, ndp.MostFrequentCount())
	np.int64(2)
	"""
	most_frequent_counts = apply_to_each_slice(values, axis, count_most_frequent_value)

	return most_frequent_counts


def apply_to_each_slice(values: NDArray[Any], axis: int | None, slice_function: Callable[[NDArray[Any]], Any]) -> Any:
	"""
	Return the result of a function applied to the whole Array, or to each slice along an axis.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	slice_function
		The function reducing one-dimensional values to a single result.

	Returns
	-------
	Any
		A single result, or an array of one result per slice.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.counting_statistics import apply_to_each_slice
	>>> apply_to_each_slice(numpy.array([[1, 2], [3, 4]]), 0, numpy.max)
	array([3, 4])
	"""
	if axis is None:
		flat_values = values.reshape(LAST_AXIS)
		single_result = slice_function(flat_values)
		return single_result

	slices = numpy.moveaxis(values, axis, LAST_AXIS)
	slice_results = [slice_function(values_slice) for values_slice in slices]
	results = numpy.array(slice_results)

	return results


def find_present_values(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return the present values, in a single dimension.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.

	Returns
	-------
	NDArray
		Every value that is not missing.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.counting_statistics import find_present_values
	>>> find_present_values(numpy.array([1.0, numpy.nan]))
	array([1.])
	"""
	missing = find_missing(values)
	present = ~missing
	present_values = values[present]

	return present_values


def count_distinct_values(values: NDArray[Any]) -> int:
	"""
	Return the number of distinct present values of one-dimensional values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		One-dimensional values.

	Returns
	-------
	int
		The number of distinct present values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.counting_statistics import count_distinct_values
	>>> count_distinct_values(numpy.array(["a", "b", "a"]))
	2
	"""
	present_values = find_present_values(values)
	distinct_values = numpy.unique(present_values)
	distinct_count = distinct_values.size

	return distinct_count


def find_most_frequent_value(values: NDArray[Any]) -> Any:
	"""
	Return the present value appearing the most often, the lowest one in case of a tie.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		One-dimensional values, at least one of them present.

	Returns
	-------
	Any
		The most frequent value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.counting_statistics import find_most_frequent_value
	>>> find_most_frequent_value(numpy.array([2, 1, 2, 1]))
	np.int64(1)
	"""
	present_values = find_present_values(values)
	distinct_values, counts = numpy.unique(present_values, return_counts=True)
	most_frequent_position = numpy.argmax(counts)
	most_frequent_value = distinct_values[most_frequent_position]

	return most_frequent_value


def count_most_frequent_value(values: NDArray[Any]) -> Any:
	"""
	Return the number of times the most frequent present value appears.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		One-dimensional values.

	Returns
	-------
	Any
		The highest count, 0 when there is no present value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.counting_statistics import count_most_frequent_value
	>>> count_most_frequent_value(numpy.array([2, 1, 2]))
	np.int64(2)
	"""
	present_values = find_present_values(values)
	if present_values.size == 0:
		return NO_VALUE_COUNT

	_, counts = numpy.unique(present_values, return_counts=True)
	highest_count = numpy.max(counts)

	return highest_count
