"""
Comparison of the columns of two Tables.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.arrays.equality.equality_check import match_types
from numdaplot.arrays.equality.type_match import TypeMatch
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_missing, find_column_type, read_present_values
from numdaplot.column_storage.time_zones import find_column_time_zone


def are_frames_equal(left: pandas.DataFrame, right: pandas.DataFrame, types: TypeMatch) -> bool:
	"""
	Return whether two Tables have the same columns, in the same order, holding the same values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The columns of the first Table.
	right
		The columns of the second Table.
	types
		Whether the type of each column must also be the same.

	Returns
	-------
	bool
		True when the column names, the number of rows and every column are equal.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.frame_equality import are_frames_equal
	>>> integers = pandas.DataFrame({"price": pandas.array([1, 2], dtype="Int64")})
	>>> decimals = pandas.DataFrame({"price": [1.0, 2.0]})
	>>> are_frames_equal(integers, decimals, ndp.TypeMatch.IGNORED)
	True
	"""
	left_names = list(left.columns)
	right_names = list(right.columns)
	if left_names != right_names:
		return False

	left_row_count = len(left)
	right_row_count = len(right)
	if left_row_count != right_row_count:
		return False

	for column_name in left_names:
		left_column = left[column_name]
		right_column = right[column_name]
		same_column = are_columns_equal(left_column, right_column, types)
		if not same_column:
			return False

	return True


def are_columns_equal(left: Column, right: Column, types: TypeMatch) -> bool:
	"""
	Return whether two columns of the same length hold the same values at the same rows.

	Two missing values at the same row are equal. Values of types that cannot be compared,
	such as numbers and texts, are never equal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The first column.
	right
		The second column, as long as the first one.
	types
		Whether the types must also be the same.

	Returns
	-------
	bool
		True when the missing values are at the same rows and the present values are equal. Datetime columns
		in different time zones are never equal, even for the same instants.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.frame_equality import are_columns_equal
	>>> left = pandas.Series([1.5, None])
	>>> right = pandas.Series([1.5, None])
	>>> are_columns_equal(left, right, ndp.TypeMatch.STRICT)
	True
	"""
	left_type = find_column_type(left)
	right_type = find_column_type(right)
	types_match = match_types(left_type, right_type, types)
	if not types_match:
		return False

	left_time_zone = find_column_time_zone(left)
	right_time_zone = find_column_time_zone(right)
	if left_time_zone != right_time_zone:
		return False

	left_missing = find_column_missing(left)
	right_missing = find_column_missing(right)
	same_missing = numpy.array_equal(left_missing, right_missing)
	if not same_missing:
		return False

	left_values = read_present_values(left)
	right_values = read_present_values(right)
	same_values = left_values == right_values
	all_equal = numpy.all(same_values)
	is_equal = bool(all_equal)

	return is_equal
