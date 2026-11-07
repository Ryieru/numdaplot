"""
Checks and alignment of the key columns of a join.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.data_types.pandas_mapping import to_pandas_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
from numdaplot.tables.frames.time_zones import find_column_time_zone
from numdaplot.tables.joining.key_types import KeyTypes

OTHER_TABLE_NAME = "the other Table"
JOIN_OPERATION = "Join"
KEY_OPERATION = "Joining on {key_name!r}"
FLOAT_DTYPE = numpy.dtype(numpy.float64)


def align_key_frames(
	frame: pandas.DataFrame, other_frame: pandas.DataFrame, keys: list[str], key_types: KeyTypes
) -> tuple[pandas.DataFrame, pandas.DataFrame]:
	"""
	Return the key columns of both Tables of a join, each key converted to one type on both sides.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the joined Table.
	other_frame
		The columns of the other Table.
	keys
		The names of the key columns.
	key_types
		How close the types of each key must be.

	Returns
	-------
	tuple[pandas.DataFrame, pandas.DataFrame]
		The key columns of the joined Table and of the other Table, of the same types.

	Raises
	------
	ColumnNotFoundError
		When a key is missing from one of the Tables.
	IncompatibleTypesError
		When the two columns of a key are of different families, of different types with ``KeyTypes.SAME_TYPE``, or
		a date and a datetime.
	TimeZoneMismatchError
		When the two columns of a key hold datetimes of different time zones, or with and without one.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import align_key_frames
	>>> frame = pandas.DataFrame({"id": pandas.array([1, 2], dtype="Int64")})
	>>> other_frame = pandas.DataFrame({"id": [1.0, 2.5]})
	>>> key_frame, other_key_frame = align_key_frames(frame, other_frame, ["id"], ndp.KeyTypes.SAME_FAMILY)
	>>> key_frame["id"].tolist()
	[1.0, 2.0]
	"""
	column_names = frame.columns.tolist()
	other_names = other_frame.columns.tolist()
	require_known_columns(keys, column_names)
	require_other_keys(keys, other_names)
	key_columns = dict[str, Column]()
	other_key_columns = dict[str, Column]()

	for key_name in keys:
		column = frame[key_name]
		other_column = other_frame[key_name]
		key_type = find_key_type(column, other_column, key_types)
		key_column = convert_key_column(column, key_type)
		other_key_column = convert_key_column(other_column, key_type)
		key_columns[key_name] = key_column
		other_key_columns[key_name] = other_key_column

	key_frame = pandas.DataFrame(key_columns)
	other_key_frame = pandas.DataFrame(other_key_columns)

	return key_frame, other_key_frame


def require_other_keys(keys: list[str], other_names: list[str]) -> None:
	"""
	Check that the other Table of a join has every key column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	keys
		The names of the key columns.
	other_names
		The column names of the other Table.

	Raises
	------
	ColumnNotFoundError
		At the first key the other Table does not have, naming it.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import require_other_keys
	>>> try:
	... 	require_other_keys(["Num_Acc"], ["num_acc"])
	... except ndp.ColumnNotFoundError as error:
	... 	print(error)
	No column of the other Table is named 'Num_Acc'.
	"""
	known_names = set(other_names)

	for key_name in keys:
		if key_name not in known_names:
			raise ColumnNotFoundError(key_name, OTHER_TABLE_NAME)


def find_key_type(column: Column, other_column: Column, key_types: KeyTypes) -> Type:
	"""
	Return the type both columns of a key take for the join.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table.
	other_column
		The key column of the other Table.
	key_types
		How close their types must be.

	Returns
	-------
	Type
		Their type when they share it, except categories of different categories, which give ``TEXT``. Otherwise
		the number type holding both, or ``TEXT`` for a text and a category.

	Raises
	------
	IncompatibleTypesError
		When the columns are of different families, of different types with ``KeyTypes.SAME_TYPE``, or a date and
		a datetime.
	TimeZoneMismatchError
		When the columns hold datetimes of different time zones, or with and without one.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import find_key_type
	>>> integers = pandas.Series([1], dtype="Int32")
	>>> find_key_type(integers, pandas.Series([1], dtype="Int64"), ndp.KeyTypes.SAME_FAMILY)
	<Type.INT64: 4>
	"""
	column_type = find_column_type(column)
	other_type = find_column_type(other_column)
	require_key_types(column, column_type, other_type, key_types)
	require_same_time_zone(column, other_column)
	if column_type == other_type:
		shared_type = find_shared_key_type(column, other_column, column_type)
		return shared_type

	family = find_family(column_type)
	if family == ValueFamily.TEXT:
		return Type.TEXT

	numpy_dtype = to_numpy_dtype(column_type)
	other_numpy_dtype = to_numpy_dtype(other_type)
	common_numpy_dtype = numpy.result_type(numpy_dtype, other_numpy_dtype)
	common_type = from_numpy_dtype(common_numpy_dtype)

	return common_type


def require_key_types(column: Column, column_type: Type, other_type: Type, key_types: KeyTypes) -> None:
	"""
	Check that the two columns of a key can match.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table, named in the error message.
	column_type
		Its type.
	other_type
		The type of the key column of the other Table.
	key_types
		How close the types must be.

	Raises
	------
	IncompatibleTypesError
		When the types are of different families, different with ``KeyTypes.SAME_TYPE``, or a date and a datetime,
		whose family is the same.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import require_key_types
	>>> days = pandas.Series(pandas.to_datetime(["2026-01-01"]), name="day").astype("datetime64[s]")
	>>> try:
	... 	require_key_types(days, ndp.Type.DATE, ndp.Type.DATETIME, ndp.KeyTypes.SAME_FAMILY)
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Join to the DATE column 'day' and DATETIME.
	"""
	if column_type == other_type:
		return

	family = find_family(column_type)
	other_family = find_family(other_type)
	is_same_family = family == other_family
	is_moment = family == ValueFamily.MOMENT
	needs_same_type = key_types == KeyTypes.SAME_TYPE
	can_match = is_same_family and not is_moment and not needs_same_type
	if can_match:
		return

	with NamedColumnErrors(column):
		raise IncompatibleTypesError(JOIN_OPERATION, [column_type.name, other_type.name])


def require_same_time_zone(column: Column, other_column: Column) -> None:
	"""
	Check that the two columns of a key hold datetimes of the same time zone, or both without one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table, named in the error message.
	other_column
		The key column of the other Table.

	Raises
	------
	TimeZoneMismatchError
		When only one has a time zone, naming the state the other column needs, or their time zones differ: change
		them first with ``TimeZoneChange``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import require_same_time_zone
	>>> utc_times = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"]), name="time").dt.tz_localize("UTC")
	>>> try:
	... 	require_same_time_zone(utc_times, utc_times.dt.tz_convert("Europe/Paris"))
	... except ndp.TimeZoneMismatchError as error:
	... 	print(error)
	Joining on 'time' needs datetimes in one time zone, got UTC and Europe/Paris.
	"""
	time_zone = find_column_time_zone(column)
	other_time_zone = find_column_time_zone(other_column)
	if time_zone == other_time_zone:
		return

	operation = KEY_OPERATION.format(key_name=column.name)
	if time_zone is None:
		raise TimeZoneMismatchError(operation, False)

	if other_time_zone is None:
		raise TimeZoneMismatchError(operation, True)

	zone_names = [time_zone.name, other_time_zone.name]
	raise TimeZoneMismatchError(operation, True, zone_names)


def find_shared_key_type(column: Column, other_column: Column, key_type: Type) -> Type:
	"""
	Return the type of a key whose two columns have the same type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table.
	other_column
		The key column of the other Table.
	key_type
		Their type.

	Returns
	-------
	Type
		The type itself, or ``TEXT`` for two categories that do not have the same categories.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import find_shared_key_type
	>>> paris = pandas.Series(["Paris"], dtype="category")
	>>> find_shared_key_type(paris, pandas.Series(["Lyon"], dtype="category"), ndp.Type.CATEGORY)
	<Type.TEXT: 12>
	"""
	if key_type != Type.CATEGORY:
		return key_type

	categories = column.cat.categories
	other_categories = other_column.cat.categories
	has_same_categories = categories.equals(other_categories)
	if has_same_categories:
		return key_type

	return Type.TEXT


def convert_key_column(column: Column, key_type: Type) -> Column:
	"""
	Return a key column converted to the type both sides of the key take.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A key column.
	key_type
		The type of the key for the join.

	Returns
	-------
	Column
		The column itself when it has that type, otherwise a converted copy, missing values staying missing.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_keys import convert_key_column
	>>> convert_key_column(pandas.Series([1, None], dtype="Int64"), ndp.Type.FLOAT64).tolist()
	[1.0, nan]
	"""
	column_type = find_column_type(column)
	if column_type == key_type:
		return column

	if key_type == Type.FLOAT64:
		numbers = column.to_numpy(dtype=FLOAT_DTYPE, na_value=numpy.nan)
		number_column = pandas.Series(numbers, name=column.name)
		return number_column

	key_dtype = to_pandas_dtype(key_type)
	converted_column = column.astype(key_dtype)

	return converted_column
