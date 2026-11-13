"""
Division of counts into fractions of a whole.

.. versionadded:: 0.1.0
"""

import numpy
from numpy.typing import NDArray


def divide_counts(counts: NDArray[numpy.int64] | NDArray[numpy.float64], value_count: float) -> NDArray[numpy.float64]:
	"""
	Return the fraction of the values each count represents.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts decimal counts and a decimal total, such as sums of weights.

	Parameters
	----------
	counts
		Numbers of values, or sums of their weights.
	value_count
		The number of values behind each count, or the sum of their weights.

	Returns
	-------
	NDArray[numpy.float64]
		Each count divided by the number of values, NaN everywhere when there is no value or every weight is 0.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.measures.count_division import divide_counts
	>>> divide_counts(numpy.array([1, 2]), 4)
	array([0.25, 0.5 ])
	>>> divide_counts(numpy.array([0]), 0)
	array([nan])
	"""
	if value_count == 0:
		no_ratios = numpy.full(counts.shape, numpy.nan, dtype=numpy.float64)
		return no_ratios

	ratios = numpy.divide(counts, value_count, dtype=numpy.float64)

	return ratios
