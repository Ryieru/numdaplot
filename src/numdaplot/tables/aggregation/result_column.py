"""
Columns holding the results of statistics.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.calculation.statistic_values import compute_statistic
from numdaplot.errors.empty_array_error import EmptyArrayError
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column, build_column_with_missing

MISSING_RESULT = numpy.nan


def compute_cell(present_values: NDArray[Any], statistic: Statistic) -> NDArray[Any] | None:
	"""
	Return a statistic of present values, or nothing when it needs a value and there is none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	present_values
		One-dimensional values without missing value.
	statistic
		Any statistic of numdaplot.

	Returns
	-------
	NDArray or None
		The result as a one-value array, ``None`` when the statistic needs a value and there is none.

	Raises
	------
	IncompatibleTypesError
		When the statistic does not apply to the type of the values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.result_column import compute_cell
	>>> compute_cell(numpy.array([], dtype=float), ndp.Mean()) is None
	True
	"""
	try:
		result = compute_statistic(present_values, statistic, None)
	except EmptyArrayError:
		return None

	return result


def build_result_column(results: list[NDArray[Any] | None]) -> Column:
	"""
	Return a Table column holding one result per row, missing where there is no result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	results
		One one-value array per row, or ``None`` for a missing result.

	Returns
	-------
	Column
		The column, ``FLOAT64`` when no row has a result.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.aggregation.result_column import build_result_column
	>>> build_result_column([numpy.array([2]), None]).tolist()
	[2, <NA>]
	"""
	missing_results = [result is None for result in results]
	missing = numpy.array(missing_results, dtype=numpy.bool_)
	present_results = [result for result in results if result is not None]
	if present_results == []:
		result_count = len(results)
		missing_values = numpy.full(result_count, MISSING_RESULT)
		missing_column = build_column(missing_values)
		return missing_column

	present_values = numpy.concatenate(present_results)
	result_column = build_column_with_missing(present_values, missing)

	return result_column
