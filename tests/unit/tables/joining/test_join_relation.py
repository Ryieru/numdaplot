"""
Unit tests of the check of the relation of a join.

.. versionadded:: 0.1.0
"""

from datetime import date

import pandas
import pytest

import numdaplot as ndp
from numdaplot.tables.joining.join_relation import read_key_values, require_relation, require_unique_keys

UNIQUE_KEYS = pandas.DataFrame({"id": pandas.Series([1, 2], dtype="Int64")})
REPEATED_KEYS = pandas.DataFrame({"id": pandas.Series([1, 2, 1, 1], dtype="Int64")})
MISSING_REPEATED_KEYS = pandas.DataFrame({"id": pandas.Series([1, None, None], dtype="Int64")})
COMBINED_KEYS = pandas.DataFrame(
	{"id": pandas.Series([1, 1, 2], dtype="Int64"), "seat": pandas.Series(["A", "B", "A"], dtype="string")}
)
REPEATED_COMBINED_KEYS = pandas.DataFrame(
	{"id": pandas.Series([1, 1], dtype="Int64"), "seat": pandas.Series(["A", "A"], dtype="string")}
)
LEFT_TABLE_NAME = "the left Table"
RIGHT_TABLE_NAME = "the right Table"
EXPECTED_REPEAT_COUNT = 3
EXPECTED_REPEATED_VALUES = [1]
DATE_ROW = pandas.DataFrame({"day": pandas.Series(pandas.to_datetime(["2026-01-01"])).astype("datetime64[s]")})
EXPECTED_DATE_VALUES = [date(2026, 1, 1)]
INTEGER_ROW = pandas.DataFrame({"id": pandas.Series([7], dtype="Int64"), "seat": pandas.Series(["A"], dtype="string")})
EXPECTED_INTEGER_VALUES = [7, "A"]


@pytest.mark.parametrize("relation", list(ndp.Relation))
def test_require_relation_accepts_unique_keys_on_both_sides(relation: ndp.Relation) -> None:
	"""
	Check that every relation accepts keys appearing once on both sides.

	.. versionadded:: 0.1.0

	Parameters
	----------
	relation
		The relation checked.
	"""
	require_relation(UNIQUE_KEYS, UNIQUE_KEYS, relation)


def test_require_relation_checks_nothing_for_many_to_many() -> None:
	"""
	Check that MANY_TO_MANY accepts repeated keys on both sides.

	.. versionadded:: 0.1.0
	"""
	require_relation(REPEATED_KEYS, REPEATED_KEYS, ndp.Relation.MANY_TO_MANY)


@pytest.mark.parametrize(
	("key_frame", "other_key_frame", "relation", "expected_table_name"),
	[
		(REPEATED_KEYS, UNIQUE_KEYS, ndp.Relation.ONE_TO_MANY, LEFT_TABLE_NAME),
		(UNIQUE_KEYS, REPEATED_KEYS, ndp.Relation.MANY_TO_ONE, RIGHT_TABLE_NAME),
		(REPEATED_KEYS, REPEATED_KEYS, ndp.Relation.ONE_TO_ONE, LEFT_TABLE_NAME),
		(UNIQUE_KEYS, REPEATED_KEYS, ndp.Relation.ONE_TO_ONE, RIGHT_TABLE_NAME),
	],
)
def test_require_relation_names_the_first_table_repeating_a_key(
	key_frame: pandas.DataFrame, other_key_frame: pandas.DataFrame, relation: ndp.Relation, expected_table_name: str
) -> None:
	"""
	Check that each relation checks its sides, the left Table first.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The keys of the left Table.
	other_key_frame
		The keys of the right Table.
	relation
		The relation checked.
	expected_table_name
		The Table named by the error.
	"""
	with pytest.raises(ndp.JoinRelationError) as error_info:
		require_relation(key_frame, other_key_frame, relation)

	assert error_info.value.table_name == expected_table_name


def test_require_relation_accepts_repeats_on_the_right_for_one_to_many() -> None:
	"""
	Check that ONE_TO_MANY leaves the right Table unchecked.

	.. versionadded:: 0.1.0
	"""
	require_relation(UNIQUE_KEYS, REPEATED_KEYS, ndp.Relation.ONE_TO_MANY)


def test_require_relation_accepts_repeats_on_the_left_for_many_to_one() -> None:
	"""
	Check that MANY_TO_ONE leaves the left Table unchecked.

	.. versionadded:: 0.1.0
	"""
	require_relation(REPEATED_KEYS, UNIQUE_KEYS, ndp.Relation.MANY_TO_ONE)


def test_require_unique_keys_counts_the_rows_of_the_first_repeat() -> None:
	"""
	Check the values and the number of rows of the first repeated key.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.JoinRelationError) as error_info:
		require_unique_keys(REPEATED_KEYS, ndp.Relation.ONE_TO_ONE, LEFT_TABLE_NAME)

	repeated_key = error_info.value.repeated_key
	assert repeated_key.key_values == EXPECTED_REPEATED_VALUES
	assert repeated_key.count == EXPECTED_REPEAT_COUNT


def test_require_unique_keys_ignores_missing_keys() -> None:
	"""
	Check that two missing keys are not a repeat, as they never match.

	.. versionadded:: 0.1.0
	"""
	require_unique_keys(MISSING_REPEATED_KEYS, ndp.Relation.ONE_TO_ONE, LEFT_TABLE_NAME)


def test_require_unique_keys_checks_the_combination_of_several_keys() -> None:
	"""
	Check that two keys are unique together even when one of them repeats.

	.. versionadded:: 0.1.0
	"""
	require_unique_keys(COMBINED_KEYS, ndp.Relation.ONE_TO_ONE, LEFT_TABLE_NAME)


def test_require_unique_keys_rejects_a_repeated_combination() -> None:
	"""
	Check that a repeated combination raises JoinRelationError naming both keys.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.JoinRelationError) as error_info:
		require_unique_keys(REPEATED_COMBINED_KEYS, ndp.Relation.ONE_TO_ONE, LEFT_TABLE_NAME)

	key_names = error_info.value.repeated_key.key_names
	expected_names = REPEATED_COMBINED_KEYS.columns.tolist()
	assert key_names == expected_names


@pytest.mark.parametrize(
	("key_row_frame", "expected_values"),
	[(DATE_ROW, EXPECTED_DATE_VALUES), (INTEGER_ROW, EXPECTED_INTEGER_VALUES)],
)
def test_read_key_values_gives_python_values(key_row_frame: pandas.DataFrame, expected_values: list[object]) -> None:
	"""
	Check that dates and nullable integers become Python values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_row_frame
		One row of key columns.
	expected_values
		The Python values.
	"""
	key_values = read_key_values(key_row_frame)

	assert key_values == expected_values
