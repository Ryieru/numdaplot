"""
Unit tests of the columns of the result of a join.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

import numdaplot as ndp
from numdaplot.tables.joining.joined_frame import join_frames, join_key_columns, take_rows

ACCIDENT_FRAME = pandas.DataFrame(
	{"id": pandas.Series([1, 2], dtype="Int64"), "dep": pandas.Series(["75", "69"], dtype="string")}
)
USER_IDS = ndp.Array.from_list([3, 1])
USER_AGES = ndp.Array.from_list([51, 34])
USERS = ndp.Table.from_arrays({"id": USER_IDS, "age": USER_AGES})
OUTER_JOIN = ndp.Join(other=USERS, keys=["id"], mode=ndp.JoinMode.OUTER)
EXPECTED_COLUMN_NAMES = ["id", "dep", "age"]
EXPECTED_IDS = [1, 2, 3]
EXPECTED_AGE_DTYPE = pandas.Int64Dtype()
KEY_FRAME = pandas.DataFrame({"id": [1.0, 2.0]})
OTHER_KEY_FRAME = pandas.DataFrame({"id": [3.0, 1.0]})
ROWS = numpy.array([0, 1, -1])
OTHER_ROWS = numpy.array([1, -1, 0])
EXPECTED_KEYS = [1.0, 2.0, 3.0]
AGE_FRAME = pandas.DataFrame({"age": pandas.Series([34, 51], dtype="Int64")})
TAKEN_ROWS = numpy.array([1, -1, 1])
EXPECTED_TAKEN_ROW_COUNT = 3
EXPECTED_TAKEN_INDEX = [0, 1, 2]
EXPECTED_MISSING_AGES = [False, True, False]


def test_join_frames_gives_the_keys_then_each_table() -> None:
	"""
	Check the order of the columns and of the rows of an outer join.

	.. versionadded:: 0.1.0
	"""
	joined_frame = join_frames(ACCIDENT_FRAME, OUTER_JOIN)

	column_names = joined_frame.columns.tolist()
	id_column = joined_frame["id"]
	id_list = id_column.tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert id_list == EXPECTED_IDS


def test_join_frames_keeps_the_type_of_a_column_gaining_missing_values() -> None:
	"""
	Check that an integer column with a row without match stays a nullable integer column.

	.. versionadded:: 0.1.0
	"""
	joined_frame = join_frames(ACCIDENT_FRAME, OUTER_JOIN)

	age_column = joined_frame["age"]
	missing_ages = age_column.isna()
	missing_list = missing_ages.tolist()
	assert age_column.dtype == EXPECTED_AGE_DTYPE
	assert missing_list == EXPECTED_MISSING_AGES


def test_join_key_columns_takes_the_other_key_where_the_joined_table_has_no_row() -> None:
	"""
	Check that each key comes from the joined Table, or from the other one for its unmatched rows.

	.. versionadded:: 0.1.0
	"""
	key_columns = join_key_columns(KEY_FRAME, OTHER_KEY_FRAME, ROWS, OTHER_ROWS)

	id_column = key_columns["id"]
	id_list = id_column.tolist()
	assert id_list == EXPECTED_KEYS


def test_take_rows_repeats_rows_and_adds_missing_rows() -> None:
	"""
	Check that a row can be taken twice, -1 giving a missing row, and that the rows are numbered from 0.

	.. versionadded:: 0.1.0
	"""
	taken_frame = take_rows(AGE_FRAME, TAKEN_ROWS)

	taken_row_count = len(taken_frame)
	age_column = taken_frame["age"]
	index_list = taken_frame.index.tolist()
	missing_ages = age_column.isna()
	missing_list = missing_ages.tolist()
	assert taken_row_count == EXPECTED_TAKEN_ROW_COUNT
	assert index_list == EXPECTED_TAKEN_INDEX
	assert missing_list == EXPECTED_MISSING_AGES
	assert age_column.dtype == EXPECTED_AGE_DTYPE
