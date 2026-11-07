"""
Unit tests of TableJoining.

.. versionadded:: 0.1.0
"""

import numdaplot as ndp
from numdaplot.tables.table_joining import TableJoining

IDS = ndp.Array.from_list([1, 2])
DEPARTMENTS = ndp.Array.from_list(["75", "69"])
ACCIDENTS = ndp.Table.from_arrays({"id": IDS, "dep": DEPARTMENTS})
USER_IDS = ndp.Array.from_list([1])
AGES = ndp.Array.from_list([34])
USERS = ndp.Table.from_arrays({"id": USER_IDS, "age": AGES})
EXPECTED_ROW_COUNT = 1
EXPECTED_COLUMN_NAMES = ["id", "dep", "age"]
ORIGINAL_COLUMN_NAMES = ["id", "dep"]
KEYS = ["id"]


def test_table_joining_is_a_base_of_table() -> None:
	"""
	Check that Table has the join method.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ndp.Table, TableJoining)


def test_join_returns_a_new_table_of_the_matching_rows() -> None:
	"""
	Check that join returns a Table, both Tables staying as they were.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=USERS, keys=KEYS)

	joined_table = ACCIDENTS.join(join)

	assert isinstance(joined_table, ndp.Table)
	assert joined_table.row_count == EXPECTED_ROW_COUNT
	assert joined_table.column_names == EXPECTED_COLUMN_NAMES
	assert ACCIDENTS.column_names == ORIGINAL_COLUMN_NAMES
