"""
Distinct values of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.selection.missing_mask import find_missing

SINGLE_MISSING_VALUE = slice(0, 1)


def find_unique_values(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return each distinct value once, sorted, with a single missing value at the end when there is one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array, of any number of dimensions.

	Returns
	-------
	NDArray
		The distinct values, in one dimension.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.layout.unique_values import find_unique_values
	>>> find_unique_values(numpy.array([[3.0, numpy.nan], [1.0, 3.0]]))
	array([ 1.,  3., nan])
	"""
	missing = find_missing(values)
	present = ~missing
	present_values = values[present]
	missing_values = values[missing]
	distinct_values = numpy.unique(present_values)
	single_missing_values = missing_values[SINGLE_MISSING_VALUE]
	parts = [distinct_values, single_missing_values]
	unique_values = numpy.concatenate(parts)

	return unique_values
