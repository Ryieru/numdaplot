"""
Normalization of a pandas DataFrame into the storage of a Table.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from pandas.api.types import infer_dtype

from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.pandas_mapping import TYPES_BY_PANDAS_NAME, from_pandas_dtype, to_pandas_dtype
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_index_error import UnsupportedIndexError
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.time_zones import normalize_time_zone_column

INFERRED_TYPES = {
	"integer": Type.INT64,
	"floating": Type.FLOAT64,
	"mixed-integer-float": Type.FLOAT64,
	"decimal": Type.FLOAT64,
	"boolean": Type.BOOL,
}
INTEGER_KINDS = frozenset({"i", "u"})
BOOLEAN_KIND = "b"
DECIMAL_KIND = "f"
DATETIME_KIND = "M"
DURATION_KIND = "m"
TEXT_INFERRED_KINDS = frozenset({"string", "empty"})
DATETIME_DTYPE = "datetime64[ns]"
DURATION_DTYPE = "timedelta64[ns]"
PYTHON_OBJECT_DTYPE = numpy.dtype(object)


def normalize_frame(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a DataFrame stored the way a Table stores its columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		Any DataFrame, read from a file or given by the user. It is not changed.

	Returns
	-------
	pandas.DataFrame
		A new DataFrame numbered from 0, whose columns use the dtypes given by ``to_pandas_dtype``.

	Raises
	------
	InvalidColumnNameError
		When a column name is not a non-empty text.
	DuplicateColumnError
		When a column name appears twice.
	UnsupportedIndexError
		When the index holds anything else than the row numbers 0, 1, 2...
	UnsupportedTypeError
		When a column has a type numdaplot does not support, such as complex numbers.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import normalize_frame
	>>> normalize_frame(pandas.DataFrame({"count": [1, 2]})).dtypes.tolist()
	[Int64Dtype()]
	"""
	raw_names = list(frame.columns)
	require_column_names(raw_names)
	require_plain_index(frame.index)
	column_names = [str(raw_name) for raw_name in raw_names]
	normalized_columns = dict[str, Column]()

	for column_name in column_names:
		column = frame[column_name]
		normalized_column = normalize_column(column)
		normalized_columns[column_name] = normalized_column

	row_count = len(frame)
	row_numbers = pandas.RangeIndex(row_count)
	normalized_frame = pandas.DataFrame(normalized_columns, index=row_numbers)

	return normalized_frame


def require_plain_index(index: pandas.Index) -> None:
	"""
	Check that an index only holds the row numbers 0, 1, 2...

	.. versionadded:: 0.1.0

	Parameters
	----------
	index
		The index of a DataFrame.

	Raises
	------
	UnsupportedIndexError
		When the index holds other values, such as city names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import require_plain_index
	>>> try:
	... 	require_plain_index(pandas.Index(["Paris", "Lyon"]))
	... except ndp.UnsupportedIndexError as error:
	... 	print(error)
	A Table has no index, call reset_index() on the pandas DataFrame first to keep its index as a column.
	"""
	row_count = len(index)
	row_numbers = pandas.RangeIndex(row_count)
	is_plain = index.equals(row_numbers)
	if not is_plain:
		raise UnsupportedIndexError()


def normalize_column(column: Column) -> Column:
	"""
	Return a column stored with the pandas dtype of its numdaplot type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		Any pandas column.

	Returns
	-------
	pandas.Series
		The column itself when its dtype is already one a Table uses, otherwise a converted copy.
		Python objects become integers, decimals or booleans when they all are, and texts otherwise.

	Raises
	------
	UnsupportedTypeError
		When the column has a type numdaplot does not support, such as complex numbers or
		datetimes in a fixed offset instead of a time zone.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import normalize_column
	>>> text_column = normalize_column(pandas.Series(["a", None], dtype=object))
	>>> str(text_column.dtype)
	'string'
	"""
	dtype_name = str(column.dtype)
	if dtype_name in TYPES_BY_PANDAS_NAME:
		stored_column = normalize_categories(column)
		return stored_column

	converted_column = convert_column_dtype(column)
	from_pandas_dtype(converted_column.dtype)

	return converted_column


def convert_column_dtype(column: Column) -> Column:
	"""
	Return a column converted to the dtype a Table uses for its kind of values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column whose dtype is not one a Table uses.

	Returns
	-------
	pandas.Series
		The converted column, or the column itself when no conversion applies.

	Raises
	------
	UnsupportedTypeError
		When the column holds datetimes in a fixed offset instead of a time zone.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import convert_column_dtype
	>>> convert_column_dtype(pandas.Series([1, 2], dtype=numpy.int32)).dtype
	Int32Dtype()
	"""
	column_dtype = column.dtype
	dtype_kind = column_dtype.kind
	if isinstance(column_dtype, pandas.DatetimeTZDtype):
		time_zone_column = normalize_time_zone_column(column)
		return time_zone_column

	if isinstance(column_dtype, pandas.StringDtype):
		text_column = convert_to_type(column, Type.TEXT)
		return text_column

	if dtype_kind == DECIMAL_KIND:
		decimal_column = convert_decimals(column)
		return decimal_column

	if dtype_kind == DATETIME_KIND:
		datetime_column = column.astype(DATETIME_DTYPE)
		return datetime_column

	if dtype_kind == DURATION_KIND:
		duration_column = column.astype(DURATION_DTYPE)
		return duration_column

	is_numpy_dtype = isinstance(column_dtype, numpy.dtype)
	if not is_numpy_dtype:
		return column

	converted_column = convert_numpy_column(column)

	return converted_column


def convert_decimals(column: Column) -> Column:
	"""
	Return a decimal column stored as numpy decimals, with NaN as missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A decimal column, such as the pandas ``Float64`` dtype that marks missing values with ``pd.NA``.

	Returns
	-------
	pandas.Series
		The column with the numpy decimal dtype of the same size.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import convert_decimals
	>>> convert_decimals(pandas.Series([1.5, None], dtype="Float64")).tolist()
	[1.5, nan]
	"""
	dtype_name = str(column.dtype)
	numpy_dtype_name = dtype_name.lower()
	decimal_values = column.to_numpy(dtype=numpy_dtype_name, na_value=numpy.nan)
	decimal_column = pandas.Series(decimal_values, index=column.index)

	return decimal_column


def convert_numpy_column(column: Column) -> Column:
	"""
	Return a numpy integer, boolean or object column stored with the dtype a Table uses.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column with a numpy dtype.

	Returns
	-------
	pandas.Series
		Integers and booleans in the pandas dtypes that accept missing values, Python objects
		as guessed by ``infer_object_column``, any other column unchanged.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import convert_numpy_column
	>>> convert_numpy_column(pandas.Series([True, False])).dtype
	BooleanDtype
	"""
	dtype_kind = column.dtype.kind
	if dtype_kind in INTEGER_KINDS:
		integer_dtype = cast(numpy.dtype[Any], column.dtype)
		integer_type = from_numpy_dtype(integer_dtype)
		integer_column = convert_to_type(column, integer_type)
		return integer_column

	if dtype_kind == BOOLEAN_KIND:
		boolean_column = convert_to_type(column, Type.BOOL)
		return boolean_column

	if column.dtype == PYTHON_OBJECT_DTYPE:
		object_column = infer_object_column(column)
		return object_column

	return column


def infer_object_column(column: Column) -> Column:
	"""
	Return a column of Python objects stored with the type its present values share.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of Python objects.

	Returns
	-------
	pandas.Series
		``INT64`` when every present value is an integer, ``FLOAT64`` for decimals or integers and decimals,
		``BOOL`` for booleans, and ``TEXT`` for anything else, each value then written as a text.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import infer_object_column
	>>> infer_object_column(pandas.Series([1, None, 3], dtype=object)).tolist()
	[1, <NA>, 3]
	"""
	inferred_kind = infer_dtype(column, skipna=True)
	target_type = INFERRED_TYPES.get(inferred_kind, Type.TEXT)
	converted_column = convert_to_type(column, target_type)

	return converted_column


def normalize_categories(column: Column) -> Column:
	"""
	Return a column whose categories, if it has any, are texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column stored with a dtype a Table uses.

	Returns
	-------
	pandas.Series
		The column itself, or a category column of texts when its categories are other values.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.frame_normalization import normalize_categories
	>>> categories = normalize_categories(pandas.Series([1, 2], dtype="category"))
	>>> categories.tolist()
	['1', '2']
	"""
	if not isinstance(column.dtype, pandas.CategoricalDtype):
		return column

	categories = column.cat.categories
	categories_kind = infer_dtype(categories, skipna=True)
	if categories_kind in TEXT_INFERRED_KINDS:
		return column

	text_column = convert_to_type(column, Type.TEXT)
	category_column = convert_to_type(text_column, Type.CATEGORY)

	return category_column


def convert_to_type(column: Column, data_type: Type) -> Column:
	"""
	Return a column converted to the pandas dtype of a numdaplot type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		Any column.
	data_type
		The numdaplot type to store the column as.

	Returns
	-------
	pandas.Series
		The converted column.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.frames.frame_normalization import convert_to_type
	>>> convert_to_type(pandas.Series([1, 2]), ndp.Type.TEXT).tolist()
	['1', '2']
	"""
	pandas_dtype = to_pandas_dtype(data_type)
	converted_column = column.astype(pandas_dtype)

	return converted_column
