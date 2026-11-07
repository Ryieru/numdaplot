"""
Columns of the result of a join of two Tables.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.tables.joining.join import Join
from numdaplot.tables.joining.join_keys import align_key_frames
from numdaplot.tables.joining.joined_names import name_joined_columns
from numdaplot.tables.joining.joined_rows import pair_rows
from numdaplot.tables.table_data import read_stored_frame

COLUMN_AXIS = 1


def join_frames(frame: pandas.DataFrame, join: Join) -> pandas.DataFrame:
	"""
	Return the columns of the join of the columns of a Table with the other Table of a join.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the joined Table.
	join
		The other Table, the keys and the settings of the join.

	Returns
	-------
	pandas.DataFrame
		The keys, then the other columns of the joined Table, then those of the other Table, one row per pair of
		rows, missing values where a Table has no row.

	Raises
	------
	ColumnNotFoundError
		When a key is missing from one of the Tables.
	IncompatibleTypesError
		When the two columns of a key cannot match.
	TimeZoneMismatchError
		When the two columns of a key hold datetimes of different time zones, or with and without one.
	DuplicateColumnError
		When both Tables have a column besides the keys and no suffixes are given, or a suffixed name is already
		taken.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.joined_frame import join_frames
	>>> users = ndp.Table.from_arrays({"id": ndp.Array.from_list([1, 3]), "age": ndp.Array.from_list([34, 51])})
	>>> frame = pandas.DataFrame({"id": pandas.array([1, 2], dtype="Int64")})
	>>> join_frames(frame, ndp.Join(other=users, keys=["id"], mode=ndp.JoinMode.LEFT))["age"].tolist()
	[34, <NA>]
	"""
	other_frame = read_stored_frame(join.other)
	key_frame, other_key_frame = align_key_frames(frame, other_frame, join.keys, join.key_types)
	column_names = frame.columns.tolist()
	other_names = other_frame.columns.tolist()
	joined_names, other_joined_names = name_joined_columns(column_names, other_names, join.keys, join.suffixes)
	rows, other_rows = pair_rows(key_frame, other_key_frame, join.mode)
	joined_keys = join_key_columns(key_frame, other_key_frame, rows, other_rows)
	kept_frame = frame.drop(columns=join.keys)
	other_kept_frame = other_frame.drop(columns=join.keys)
	joined_frame = take_rows(kept_frame, rows)
	other_joined_frame = take_rows(other_kept_frame, other_rows)
	joined_frame.columns = pandas.Index(joined_names)
	other_joined_frame.columns = pandas.Index(other_joined_names)
	result_frame = pandas.concat([joined_keys, joined_frame, other_joined_frame], axis=COLUMN_AXIS)

	return result_frame


def join_key_columns(
	key_frame: pandas.DataFrame,
	other_key_frame: pandas.DataFrame,
	rows: NDArray[numpy.intp],
	other_rows: NDArray[numpy.intp],
) -> pandas.DataFrame:
	"""
	Return one column per key: the key of the joined Table, or of the other Table where the joined one has no row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of the joined Table.
	other_key_frame
		The key columns of the other Table, of the same names and types.
	rows
		The row of the joined Table of each row of the result, -1 where it has none.
	other_rows
		The row of the other Table of each row of the result, -1 where it has none.

	Returns
	-------
	pandas.DataFrame
		The keys of each row of the result, numbered from 0.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.joining.joined_frame import join_key_columns
	>>> key_frame = pandas.DataFrame({"id": [1.0, 2.0]})
	>>> other_key_frame = pandas.DataFrame({"id": [3.0, 1.0]})
	>>> join_key_columns(key_frame, other_key_frame, numpy.array([0, 1, -1]), numpy.array([1, -1, 0]))["id"].tolist()
	[1.0, 2.0, 3.0]
	"""
	joined_keys = take_rows(key_frame, rows)
	other_joined_keys = take_rows(other_key_frame, other_rows)
	has_row = rows >= 0
	key_columns = dict[str, pandas.Series]()

	for key_name in key_frame.columns:
		key_column = joined_keys[key_name]
		other_key_column = other_joined_keys[key_name]
		combined_column = key_column.where(has_row, other_key_column)
		key_columns[key_name] = combined_column

	key_columns_frame = pandas.DataFrame(key_columns)

	return key_columns_frame


def take_rows(frame: pandas.DataFrame, rows: NDArray[numpy.intp]) -> pandas.DataFrame:
	"""
	Return the given rows of the columns of a Table, a row of missing values for each -1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table, rows numbered from 0.
	rows
		The row numbers taken, in order, possibly repeated, -1 for a row of missing values.

	Returns
	-------
	pandas.DataFrame
		The rows taken, numbered from 0, each column keeping its type.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.joining.joined_frame import take_rows
	>>> ages = pandas.DataFrame({"age": pandas.array([34, 51], dtype="Int64")})
	>>> take_rows(ages, numpy.array([1, -1]))["age"].tolist()
	[51, <NA>]
	"""
	taken_frame = frame.reindex(rows)
	numbered_frame = taken_frame.reset_index(drop=True)

	return numbered_frame
