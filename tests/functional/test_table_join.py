"""
Functional tests of the join of two Tables, as a user joins the files of road accidents.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime
from typing import Any

import pandas
import pytest

import numdaplot as ndp

ACCIDENT_IDS = pandas.Series([101, 102, None], dtype="Int64")
ACCIDENT_FRAME = pandas.DataFrame({"Num_Acc": ACCIDENT_IDS, "dep": ["75", "69", "13"]})
ACCIDENTS = ndp.Table.from_pandas(ACCIDENT_FRAME)
USER_FRAME = pandas.DataFrame(
	{"Num_Acc": pandas.Series([101, 101, 103, None], dtype="Int64"), "grav": pandas.Series([1, 3, 2, 4], dtype="Int64")}
)
USERS = ndp.Table.from_pandas(USER_FRAME)
KEYS = ["Num_Acc"]
EXPECTED_COLUMN_NAMES = ["Num_Acc", "dep", "grav"]
EXPECTED_INNER_IDS = [101, 101]
EXPECTED_LEFT_DEPARTMENTS = ["75", "75", "69", "13"]
EXPECTED_RIGHT_SEVERITIES = [1, 3, 2, 4]
EXPECTED_OUTER_ROW_COUNT = 6
EXPECTED_OUTER_DEPARTMENTS = ["75", "75", "69", "13", None, None]
EXPECTED_COLUMN_TYPES = {"Num_Acc": ndp.Type.INT64, "dep": ndp.Type.TEXT, "grav": ndp.Type.INT64}
DECIMAL_IDS = ndp.Array.from_list([101.0])
FLAGS = ndp.Array.from_list([True])
DECIMAL_USERS = ndp.Table.from_arrays({"Num_Acc": DECIMAL_IDS, "flag": FLAGS})
PARIS = ndp.Array.from_list(["75"])
DEATH_COUNTS_2024 = ndp.Array.from_list([40])
DEATH_COUNTS_2025 = ndp.Array.from_list([35])
DEATHS_2024 = ndp.Table.from_arrays({"dep": PARIS, "deaths": DEATH_COUNTS_2024})
DEATHS_2025 = ndp.Table.from_arrays({"dep": PARIS, "deaths": DEATH_COUNTS_2025})
YEARS = ndp.JoinSuffixes(left="_2024", right="_2025")
EXPECTED_YEAR_NAMES = ["dep", "deaths_2024", "deaths_2025"]
NEW_YEAR = ndp.Array.from_list([date(2026, 1, 1)])
NEW_YEAR_MIDNIGHT = ndp.Array.from_list([datetime(2026, 1, 1)])
DAYS = ndp.Table.from_arrays({"day": NEW_YEAR})
MOMENTS = ndp.Table.from_arrays({"day": NEW_YEAR_MIDNIGHT})
KEY_CHANGE = ndp.NameChange(old_name="Num_Acc", new_name="accident")
KEY_RENAMING = ndp.Renaming(changes=[KEY_CHANGE])
RENAMED_USERS = USERS.rename(KEY_RENAMING)


def read_column_values(table: ndp.Table, column_name: str) -> list[Any]:
	"""
	Return the values of a column of a Table, None where a value is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		A Table.
	column_name
		The name of one of its columns.

	Returns
	-------
	list[Any]
		The values, in the order of the rows.
	"""
	frame = table.to_pandas()
	column = frame[column_name]
	object_column = column.astype(object)
	raw_values = object_column.tolist()
	missing_values = column.isna()
	missing_flags = missing_values.tolist()
	value_pairs = zip(raw_values, missing_flags, strict=True)
	values = [None if is_missing else value for value, is_missing in value_pairs]

	return values


def test_an_inner_join_keeps_each_accident_once_per_user() -> None:
	"""
	Check that an accident with two users gives two rows, the missing key matching nothing.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=USERS, keys=KEYS)

	joined_table = ACCIDENTS.join(join)

	ids = read_column_values(joined_table, "Num_Acc")
	assert joined_table.column_names == EXPECTED_COLUMN_NAMES
	assert ids == EXPECTED_INNER_IDS


def test_a_left_join_keeps_every_accident_in_its_order() -> None:
	"""
	Check that the accidents without user keep their row, the accident with a missing key included.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=USERS, keys=KEYS, mode=ndp.JoinMode.LEFT)

	joined_table = ACCIDENTS.join(join)

	departments = read_column_values(joined_table, "dep")
	assert departments == EXPECTED_LEFT_DEPARTMENTS
	assert joined_table.column_types == EXPECTED_COLUMN_TYPES


def test_a_right_join_keeps_every_user() -> None:
	"""
	Check that every user is kept, the users without accident last.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=USERS, keys=KEYS, mode=ndp.JoinMode.RIGHT)

	joined_table = ACCIDENTS.join(join)

	severities = read_column_values(joined_table, "grav")
	assert severities == EXPECTED_RIGHT_SEVERITIES


def test_an_outer_join_keeps_every_row_of_both_tables() -> None:
	"""
	Check that the accidents come first, then the users without accident.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=USERS, keys=KEYS, mode=ndp.JoinMode.OUTER)

	joined_table = ACCIDENTS.join(join)

	departments = read_column_values(joined_table, "dep")
	assert joined_table.row_count == EXPECTED_OUTER_ROW_COUNT
	assert departments == EXPECTED_OUTER_DEPARTMENTS


def test_a_join_matches_integer_keys_with_decimal_keys() -> None:
	"""
	Check that integer and decimal keys of the same value match by default, the key becoming decimal.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=DECIMAL_USERS, keys=KEYS)

	joined_table = ACCIDENTS.join(join)

	key_type = joined_table.column_types["Num_Acc"]
	assert joined_table.row_count == 1
	assert key_type == ndp.Type.FLOAT64


def test_a_join_of_keys_of_the_same_type_only_rejects_other_types() -> None:
	"""
	Check that KeyTypes.SAME_TYPE refuses integer keys against decimal keys.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=DECIMAL_USERS, keys=KEYS, key_types=ndp.KeyTypes.SAME_TYPE)

	with pytest.raises(ndp.IncompatibleTypesError):
		ACCIDENTS.join(join)


def test_a_join_tells_apart_columns_both_tables_have_with_suffixes() -> None:
	"""
	Check that the columns both Tables have get the suffixes.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=DEATHS_2025, keys=["dep"], suffixes=YEARS)

	joined_table = DEATHS_2024.join(join)

	assert joined_table.column_names == EXPECTED_YEAR_NAMES


def test_a_join_rejects_columns_both_tables_have_without_suffixes() -> None:
	"""
	Check that a column both Tables have raises DuplicateColumnError without suffixes.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=DEATHS_2025, keys=["dep"])

	with pytest.raises(ndp.DuplicateColumnError):
		DEATHS_2024.join(join)


def test_a_join_rejects_a_key_the_other_table_does_not_have() -> None:
	"""
	Check that a key with another name in the other Table raises ColumnNotFoundError: rename it first.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=RENAMED_USERS, keys=KEYS)

	with pytest.raises(ndp.ColumnNotFoundError):
		ACCIDENTS.join(join)


def test_a_join_rejects_a_date_key_against_a_datetime_key() -> None:
	"""
	Check that dates never match datetimes.

	.. versionadded:: 0.1.0
	"""
	join = ndp.Join(other=MOMENTS, keys=["day"])

	with pytest.raises(ndp.IncompatibleTypesError):
		DAYS.join(join)
