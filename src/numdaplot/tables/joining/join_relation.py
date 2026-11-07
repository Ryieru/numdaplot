"""
Check of the number of times each key appears in the Tables of a join.

.. versionadded:: 0.1.0
"""

from typing import Any

import pandas

from numdaplot.arrays.conversion.python_values import to_python_list
from numdaplot.errors.join_relation_error import JoinRelationError
from numdaplot.errors.repeated_key import RepeatedKey
from numdaplot.tables.frames.column_values import convert_column_values
from numdaplot.tables.joining.relation import Relation

UNIQUE_LEFT_RELATIONS = frozenset({Relation.ONE_TO_ONE, Relation.ONE_TO_MANY})
UNIQUE_RIGHT_RELATIONS = frozenset({Relation.ONE_TO_ONE, Relation.MANY_TO_ONE})
LEFT_TABLE_NAME = "the left Table"
RIGHT_TABLE_NAME = "the right Table"
RELATION_NAME = "Relation.{member_name}"
ROWS_AXIS = 1
EVERY_REPEAT = False
FIRST_ROW_COUNT = 1


def require_relation(key_frame: pandas.DataFrame, other_key_frame: pandas.DataFrame, relation: Relation) -> None:
	"""
	Check that each key appears at most once in the Tables where the relation of a join expects it once.

	The left Table is checked first, then the right Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of the left Table, the one joined.
	other_key_frame
		The key columns of the right Table, the other one.
	relation
		How many times each key may appear on each side.

	Raises
	------
	JoinRelationError
		At the first key repeated in a Table where the relation expects it once.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_relation import require_relation
	>>> key_frame = pandas.DataFrame({"id": pandas.Series([1], dtype="Int64")})
	>>> other_key_frame = pandas.DataFrame({"id": pandas.Series([1, 1], dtype="Int64")})
	>>> try:
	... 	require_relation(key_frame, other_key_frame, ndp.Relation.ONE_TO_ONE)
	... except ndp.JoinRelationError as error:
	... 	print(error)
	Expected each key of the right Table to appear once for Relation.ONE_TO_ONE, but 'id' 1 appears 2 times.
	"""
	if relation in UNIQUE_LEFT_RELATIONS:
		require_unique_keys(key_frame, relation, LEFT_TABLE_NAME)

	if relation in UNIQUE_RIGHT_RELATIONS:
		require_unique_keys(other_key_frame, relation, RIGHT_TABLE_NAME)


def require_unique_keys(key_frame: pandas.DataFrame, relation: Relation, table_name: str) -> None:
	"""
	Check that each key, or combination of keys, appears at most once in a Table, missing keys aside.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of a Table.
	relation
		The relation checked, named in the error message.
	table_name
		The Table checked, named in the error message.

	Raises
	------
	JoinRelationError
		At the first repeated key, in the order of the rows, with its number of rows.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.join_relation import require_unique_keys
	>>> key_frame = pandas.DataFrame({"id": pandas.Series([1, None, None], dtype="Int64")})
	>>> require_unique_keys(key_frame, ndp.Relation.ONE_TO_ONE, "the left Table")
	"""
	missing_keys = key_frame.isna()
	has_missing_key = missing_keys.any(axis=ROWS_AXIS)
	present_frame = key_frame[~has_missing_key]
	repeated_rows = present_frame.duplicated(keep=EVERY_REPEAT)
	has_repeat = bool(repeated_rows.any())
	if not has_repeat:
		return

	repeated_frame = present_frame[repeated_rows]
	first_repeat_frame = repeated_frame.iloc[:FIRST_ROW_COUNT]
	first_repeat = first_repeat_frame.iloc[0]
	matching_cells = present_frame == first_repeat
	matching_rows = matching_cells.all(axis=ROWS_AXIS)
	repeat_count = int(matching_rows.sum())
	key_names = key_frame.columns.tolist()
	key_values = read_key_values(first_repeat_frame)
	repeated_key = RepeatedKey(key_names, key_values, repeat_count)
	relation_name = RELATION_NAME.format(member_name=relation.name)
	raise JoinRelationError(relation_name, table_name, repeated_key)


def read_key_values(key_row_frame: pandas.DataFrame) -> list[Any]:
	"""
	Return the values of the single row of key columns as Python values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_row_frame
		One row of the key columns of a Table.

	Returns
	-------
	list[Any]
		The value of each key column, such as ``202500000001`` or ``datetime.date(2026, 1, 1)``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.joining.join_relation import read_key_values
	>>> seat = pandas.Series(["A"], dtype="string")
	>>> read_key_values(pandas.DataFrame({"id": pandas.Series([7], dtype="Int64"), "seat": seat}))
	[7, 'A']
	"""
	key_values = list[Any]()

	for _, column in key_row_frame.items():
		column_values = convert_column_values(column)
		python_values = to_python_list(column_values)
		key_values.append(python_values[0])

	return key_values
