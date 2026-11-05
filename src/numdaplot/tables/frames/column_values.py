"""
Conversion between the pandas columns of a Table and numpy values.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.data_types.pandas_mapping import from_pandas_dtype, to_pandas_dtype
from numdaplot.data_types.type import Type
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.time_zones import find_column_time_zone, remove_utc_zone

MISSING_CAPABLE_TYPES = frozenset(
	{Type.FLOAT32, Type.FLOAT64, Type.TEXT, Type.CATEGORY, Type.DATE, Type.DATETIME, Type.DURATION}
)
TEXT_TYPES = frozenset({Type.TEXT, Type.CATEGORY})
PYTHON_OBJECT_DTYPE = numpy.dtype(object)
ARRAY_OPERATION = "An Array"


def find_column_type(column: Column) -> Type:
	"""
	Return the numdaplot type of a Table column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column stored with one of the dtypes given by ``to_pandas_dtype``.

	Returns
	-------
	Type
		The type of the column.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.column_values import find_column_type
	>>> find_column_type(pandas.Series([1.5], dtype="float64"))
	<Type.FLOAT64: 10>
	"""
	column_type = from_pandas_dtype(column.dtype)

	return column_type


def find_column_missing(column: Column) -> NDArray[numpy.bool_]:
	"""
	Return which values of a Table column are missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each missing value.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.column_values import find_column_missing
	>>> find_column_missing(pandas.Series([1, None], dtype="Int64"))
	array([False,  True])
	"""
	missing = column.isna()
	missing_values = missing.to_numpy(dtype=numpy.bool_)

	return missing_values


def convert_column_values(column: Column) -> NDArray[Any]:
	"""
	Return the numpy values of a Table column, whose integers and booleans have no missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column. Integers and booleans must have no missing value.

	Returns
	-------
	NDArray
		The values in the numpy dtype of an Array of the same type. Categories become texts, and datetimes
		with a time zone become their UTC clock time.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.column_values import convert_column_values
	>>> convert_column_values(pandas.Series([1, 2], dtype="Int64"))
	array([1, 2])
	"""
	column_type = find_column_type(column)
	time_zone = find_column_time_zone(column)
	if time_zone is not None:
		utc_column = remove_utc_zone(column)
		utc_values = convert_column_values(utc_column)
		return utc_values

	if column_type in TEXT_TYPES:
		object_values = column.to_numpy(dtype=PYTHON_OBJECT_DTYPE, na_value=numpy.nan)
		text_dtype = to_numpy_dtype(Type.TEXT)
		text_values = object_values.astype(text_dtype)
		return text_values

	numpy_dtype = to_numpy_dtype(column_type)
	numpy_values = column.to_numpy(dtype=numpy_dtype)

	return numpy_values


def read_present_values(column: Column) -> NDArray[Any]:
	"""
	Return the present values of a Table column, in numpy.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	NDArray
		Every value that is not missing, in order, in the numpy dtype of an Array of the same type.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.column_values import read_present_values
	>>> read_present_values(pandas.Series([1, None, 3], dtype="Int64"))
	array([1, 3])
	"""
	present_column = column.dropna()
	present_values = convert_column_values(present_column)

	return present_values


def read_array_values(column: Column) -> NDArray[Any]:
	"""
	Return every value of a Table column, in the numpy form an Array stores.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	NDArray
		The values, with NaN at the missing decimals and texts, and NaT at the missing dates, datetimes and durations.

	Raises
	------
	UnsupportedMissingError
		When an integer or boolean column has a missing value, which an Array cannot hold.
	TimeZoneMismatchError
		When the column holds datetimes with a time zone, which an Array cannot hold.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.column_values import read_array_values
	>>> read_array_values(pandas.Series([1.5, None], dtype="float64"))
	array([1.5, nan])
	"""
	column_type = find_column_type(column)
	time_zone = find_column_time_zone(column)
	if time_zone is not None:
		raise TimeZoneMismatchError(ARRAY_OPERATION, False)

	missing = find_column_missing(column)
	has_missing = bool(missing.any())
	rejects_missing = has_missing and column_type not in MISSING_CAPABLE_TYPES
	if rejects_missing:
		column_name = str(column.name)
		raise UnsupportedMissingError(column_type.name, column_name)

	array_values = convert_column_values(column)

	return array_values


def build_column(values: NDArray[Any]) -> Column:
	"""
	Return a Table column holding one-dimensional numpy values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		One-dimensional values in a numpy dtype numdaplot supports.

	Returns
	-------
	pandas.Series
		A column numbered from 0, stored with the pandas dtype of the type of the values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.frames.column_values import build_column
	>>> build_column(numpy.array([1, 2])).dtype
	Int64Dtype()
	"""
	value_type = from_numpy_dtype(values.dtype)
	pandas_dtype = to_pandas_dtype(value_type)
	column_values = values
	if value_type == Type.TEXT:
		column_values = values.astype(PYTHON_OBJECT_DTYPE)

	raw_column = pandas.Series(column_values)
	column = raw_column.astype(pandas_dtype)

	return column


def build_column_with_missing(present_values: NDArray[Any], missing: NDArray[numpy.bool_]) -> Column:
	"""
	Return a Table column holding present values, with missing values at given positions.

	.. versionadded:: 0.1.0

	Parameters
	----------
	present_values
		The present values, in order.
	missing
		True at each position of the column that is missing; there are as many False as present values.

	Returns
	-------
	pandas.Series
		A column numbered from 0, as long as ``missing``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.frames.column_values import build_column_with_missing
	>>> build_column_with_missing(numpy.array([1, 3]), numpy.array([False, True, False])).tolist()
	[1, <NA>, 3]
	"""
	present_column = build_column(present_values)
	row_count = missing.size
	all_positions = pandas.RangeIndex(row_count)
	present = ~missing
	present_positions = all_positions[present]
	present_column.index = present_positions
	column = present_column.reindex(all_positions)

	return column
