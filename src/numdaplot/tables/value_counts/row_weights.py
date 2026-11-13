"""
Weights of the rows of a Table, read from a column of numbers.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.invalid_weight_error import InvalidWeightError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.types.value_family import ValueFamily, find_family

WEIGHTS_OPERATION = "ValueCount weights"
LOWEST_WEIGHT = 0.0


@dataclass(frozen=True, eq=False)
class WeightedRows:
	"""
	The rows of a Table that count, with the weight of each, or every row counting once.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The rows that count, numbered from 0.
	weights
		The weight of each of these rows, or None when every row counts once.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.value_counts.row_weights import WeightedRows
	>>> WeightedRows(pandas.DataFrame({"sex": [1, 2]}), None).weights is None
	True
	"""

	frame: pandas.DataFrame
	weights: NDArray[numpy.float64] | None


def select_weighted_rows(frame: pandas.DataFrame, weights_name: str | None) -> WeightedRows:
	"""
	Return the rows of a Table with their weights, the rows without weight left out.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	weights_name
		The column of weights, or None when every row counts once.

	Returns
	-------
	WeightedRows
		Every row without weights, else the rows whose weight is present, numbered from 0, and their weights.

	Raises
	------
	ColumnNotFoundError
		When the column of weights does not exist.
	IncompatibleTypesError
		When the column of weights does not hold numbers.
	InvalidWeightError
		When a weight is negative.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.value_counts.row_weights import select_weighted_rows
	>>> frame = pandas.DataFrame({"sex": [1, 2, 2], "weight": [300.0, None, 100.0]})
	>>> select_weighted_rows(frame, "weight").weights
	array([300., 100.])
	"""
	if weights_name is None:
		unweighted_rows = WeightedRows(frame, None)
		return unweighted_rows

	all_weights = read_row_weights(frame, weights_name)
	has_weight = ~numpy.isnan(all_weights)
	kept_frame = frame[has_weight]
	numbered_frame = kept_frame.reset_index(drop=True)
	kept_weights = all_weights[has_weight]
	weighted_rows = WeightedRows(numbered_frame, kept_weights)

	return weighted_rows


def read_row_weights(frame: pandas.DataFrame, weights_name: str) -> NDArray[numpy.float64]:
	"""
	Return the weight of each row of a Table, read from a column of numbers.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	weights_name
		The column of weights.

	Returns
	-------
	NDArray[numpy.float64]
		One weight per row, NaN where the weight is missing.

	Raises
	------
	ColumnNotFoundError
		When the column does not exist.
	IncompatibleTypesError
		When the column does not hold numbers.
	InvalidWeightError
		When a weight is negative.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.value_counts.row_weights import read_row_weights
	>>> read_row_weights(pandas.DataFrame({"weight": pandas.Series([3, None], dtype="Int64")}), "weight")
	array([ 3., nan])
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	require_known_columns([weights_name], column_names)
	weight_column = frame[weights_name]
	require_number_weights(weight_column, weights_name)
	weights = weight_column.to_numpy(dtype=numpy.float64, na_value=numpy.nan)
	require_positive_weights(weights, weights_name)

	return weights


def require_number_weights(weight_column: Column, weights_name: str) -> None:
	"""
	Check that a column of weights holds numbers.

	.. versionadded:: 0.2.0

	Parameters
	----------
	weight_column
		The column of weights.
	weights_name
		Its name, given in the error.

	Raises
	------
	IncompatibleTypesError
		When the column does not hold numbers.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.value_counts.row_weights import require_number_weights
	>>> try:
	... 	require_number_weights(pandas.Series(["high"], dtype="string"), "weight")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply ValueCount weights to the TEXT column 'weight'.
	"""
	column_type = find_column_type(weight_column)
	column_family = find_family(column_type)
	if column_family == ValueFamily.NUMBER:
		return

	type_error = IncompatibleTypesError(WEIGHTS_OPERATION, [column_type.name])
	type_error.name_column(weights_name)
	raise type_error


def require_positive_weights(weights: NDArray[numpy.float64], weights_name: str) -> None:
	"""
	Check that no weight is negative, a missing weight being left aside.

	.. versionadded:: 0.2.0

	Parameters
	----------
	weights
		The weights, NaN where a weight is missing.
	weights_name
		The name of their column, given in the error.

	Raises
	------
	InvalidWeightError
		At the first negative weight.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.value_counts.row_weights import require_positive_weights
	>>> try:
	... 	require_positive_weights(numpy.array([2.0, numpy.nan, -1.0]), "weight")
	... except ndp.InvalidWeightError as error:
	... 	print(error)
	Expected weights of at least 0 in the column 'weight', got -1.0.
	"""
	is_negative = weights < LOWEST_WEIGHT
	has_negative = bool(is_negative.any())
	if not has_negative:
		return

	negative_weights = weights[is_negative]
	first_negative = float(negative_weights[0])
	raise InvalidWeightError(first_negative, weights_name)
