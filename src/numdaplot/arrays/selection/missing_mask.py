"""
Positions of the missing values of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

NAN_KINDS = frozenset({"f", "T"})
TIME_KINDS = frozenset({"M", "m"})


def find_missing(values: NDArray[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which values are missing: NaN for decimals and texts, NaT for dates, datetimes and durations.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each missing value. Always false for types that cannot be missing.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.selection.missing_mask import find_missing
	>>> find_missing(numpy.array([1.0, numpy.nan]))
	array([False,  True])
	"""
	value_kind = values.dtype.kind
	if value_kind in NAN_KINDS:
		missing_values = numpy.isnan(values)
		return missing_values

	if value_kind in TIME_KINDS:
		missing_times = numpy.isnat(values)
		return missing_times

	no_missing_value = numpy.zeros(values.shape, dtype=numpy.bool_)

	return no_missing_value
