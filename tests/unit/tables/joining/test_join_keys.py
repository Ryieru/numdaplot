"""
Unit tests of the checks and the alignment of the keys of a join.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

import numdaplot as ndp
from numdaplot.tables.joining.join_keys import (
	align_key_frames,
	convert_key_column,
	find_key_type,
	find_shared_key_type,
	require_key_types,
	require_other_keys,
	require_same_time_zone,
)

KEYS = ["id"]
INTEGER_FRAME = pandas.DataFrame({"id": pandas.Series([1, 2], dtype="Int64"), "dep": ["75", "69"]})
DECIMAL_FRAME = pandas.DataFrame({"id": [1.0, 2.5]})
EXPECTED_DECIMAL_KEYS = [1.0, 2.0]
OTHER_NAMES = ["num_acc", "age"]
MISSING_KEYS = ["Num_Acc"]
INT32_IDS = pandas.Series([1], dtype="Int32", name="id")
INT64_IDS = pandas.Series([1], dtype="Int64", name="id")
UINT64_IDS = pandas.Series([1], dtype="UInt64", name="id")
TEXT_IDS = pandas.Series(["a"], dtype="string", name="id")
CATEGORY_IDS = pandas.Series(["a"], dtype="category", name="id")
OTHER_CATEGORY_IDS = pandas.Series(["b"], dtype="category", name="id")
DAYS = pandas.Series(pandas.to_datetime(["2026-01-01"]), name="day").astype("datetime64[s]")
UTC_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"]), name="time").dt.tz_localize("UTC")
PARIS_TIMES = UTC_TIMES.dt.tz_convert("Europe/Paris")
NAIVE_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"]), name="time")
MISSING_INTEGERS = pandas.Series([1, None], dtype="Int64")
EXPECTED_MISSING_DECIMALS = [1.0]
OTHER_TABLE_NAME = "the other Table"
EXPECTED_ZONE_NAMES = ["UTC", "Europe/Paris"]
DECIMAL_DTYPE_NAME = "float64"
TEXT_DTYPE_NAME = "string"


def test_align_key_frames_converts_both_sides_to_one_type() -> None:
	"""
	Check that integer and decimal keys both become decimals.

	.. versionadded:: 0.1.0
	"""
	key_frame, other_key_frame = align_key_frames(INTEGER_FRAME, DECIMAL_FRAME, KEYS, ndp.KeyTypes.SAME_FAMILY)

	key_column = key_frame["id"]
	key_list = key_column.tolist()
	other_key_column = other_key_frame["id"]
	assert key_list == EXPECTED_DECIMAL_KEYS
	assert key_column.dtype == other_key_column.dtype


def test_align_key_frames_keeps_only_the_keys() -> None:
	"""
	Check that the other columns are left out.

	.. versionadded:: 0.1.0
	"""
	key_frame, _ = align_key_frames(INTEGER_FRAME, DECIMAL_FRAME, KEYS, ndp.KeyTypes.SAME_FAMILY)

	key_names = key_frame.columns.tolist()
	assert key_names == KEYS


def test_align_key_frames_rejects_a_key_missing_from_the_joined_table() -> None:
	"""
	Check that a key the joined Table does not have raises ColumnNotFoundError without Table name.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		align_key_frames(DECIMAL_FRAME, INTEGER_FRAME, ["dep"], ndp.KeyTypes.SAME_FAMILY)

	assert error_info.value.table_name is None


def test_require_other_keys_names_the_other_table() -> None:
	"""
	Check that a key the other Table does not have raises ColumnNotFoundError naming that Table.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.ColumnNotFoundError) as error_info:
		require_other_keys(MISSING_KEYS, OTHER_NAMES)

	assert error_info.value.table_name == OTHER_TABLE_NAME


@pytest.mark.parametrize(
	("column", "other_column", "expected_type"),
	[
		(INT32_IDS, INT64_IDS, ndp.Type.INT64),
		(INT64_IDS, UINT64_IDS, ndp.Type.FLOAT64),
		(TEXT_IDS, CATEGORY_IDS, ndp.Type.TEXT),
		(CATEGORY_IDS, CATEGORY_IDS, ndp.Type.CATEGORY),
	],
)
def test_find_key_type_holds_both_sides(
	column: pandas.Series, other_column: pandas.Series, expected_type: ndp.Type
) -> None:
	"""
	Check the type a key takes for each pair of types of one family.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table.
	other_column
		The key column of the other Table.
	expected_type
		The type of the key.
	"""
	key_type = find_key_type(column, other_column, ndp.KeyTypes.SAME_FAMILY)

	assert key_type == expected_type


def test_require_key_types_accepts_two_types_of_one_family() -> None:
	"""
	Check that integers and decimals match by default.

	.. versionadded:: 0.1.0
	"""
	require_key_types(INT64_IDS, ndp.Type.INT64, ndp.Type.FLOAT64, ndp.KeyTypes.SAME_FAMILY)


@pytest.mark.parametrize(
	("column_type", "other_type", "key_types"),
	[
		(ndp.Type.INT64, ndp.Type.FLOAT64, ndp.KeyTypes.SAME_TYPE),
		(ndp.Type.INT64, ndp.Type.TEXT, ndp.KeyTypes.SAME_FAMILY),
		(ndp.Type.DATE, ndp.Type.DATETIME, ndp.KeyTypes.SAME_FAMILY),
	],
)
def test_require_key_types_rejects_keys_that_cannot_match(
	column_type: ndp.Type, other_type: ndp.Type, key_types: ndp.KeyTypes
) -> None:
	"""
	Check that different types with SAME_TYPE, two families, and a date with a datetime raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_type
		The type of the key of the joined Table.
	other_type
		The type of the key of the other Table.
	key_types
		How close the types must be.
	"""
	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		require_key_types(INT64_IDS, column_type, other_type, key_types)

	assert error_info.value.column_name == INT64_IDS.name


def test_require_same_time_zone_accepts_the_same_zone() -> None:
	"""
	Check that two columns of the same time zone match.

	.. versionadded:: 0.1.0
	"""
	require_same_time_zone(UTC_TIMES, UTC_TIMES)


@pytest.mark.parametrize(
	("column", "other_column", "expects_time_zone"),
	[(UTC_TIMES, NAIVE_TIMES, True), (NAIVE_TIMES, UTC_TIMES, False), (UTC_TIMES, PARIS_TIMES, True)],
)
def test_require_same_time_zone_rejects_other_zones(
	column: pandas.Series, other_column: pandas.Series, expects_time_zone: bool
) -> None:
	"""
	Check that a missing or different time zone raises TimeZoneMismatchError, stating the state needed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The key column of the joined Table.
	other_column
		The key column of the other Table.
	expects_time_zone
		Whether the other column needs a time zone.
	"""
	with pytest.raises(ndp.TimeZoneMismatchError) as error_info:
		require_same_time_zone(column, other_column)

	assert error_info.value.expects_time_zone == expects_time_zone


def test_require_same_time_zone_names_two_different_zones() -> None:
	"""
	Check that two time zones are both named.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeZoneMismatchError) as error_info:
		require_same_time_zone(UTC_TIMES, PARIS_TIMES)

	assert error_info.value.zone_names == EXPECTED_ZONE_NAMES


def test_find_shared_key_type_keeps_a_type_other_than_category() -> None:
	"""
	Check that a shared type other than CATEGORY is kept.

	.. versionadded:: 0.1.0
	"""
	key_type = find_shared_key_type(DAYS, DAYS, ndp.Type.DATE)

	assert key_type == ndp.Type.DATE


def test_find_shared_key_type_reads_categories_of_different_categories_as_texts() -> None:
	"""
	Check that two categories of different categories give TEXT.

	.. versionadded:: 0.1.0
	"""
	key_type = find_shared_key_type(CATEGORY_IDS, OTHER_CATEGORY_IDS, ndp.Type.CATEGORY)

	assert key_type == ndp.Type.TEXT


def test_convert_key_column_keeps_a_column_of_the_key_type() -> None:
	"""
	Check that a column of the key type is returned as it is.

	.. versionadded:: 0.1.0
	"""
	key_column = convert_key_column(INT64_IDS, ndp.Type.INT64)

	assert key_column is INT64_IDS


def test_convert_key_column_keeps_missing_integers_missing_as_decimals() -> None:
	"""
	Check that integers become decimals, a missing integer becoming NaN.

	.. versionadded:: 0.1.0
	"""
	key_column = convert_key_column(MISSING_INTEGERS, ndp.Type.FLOAT64)

	present_keys = key_column.dropna()
	present_list = present_keys.tolist()
	assert present_list == EXPECTED_MISSING_DECIMALS
	assert key_column.dtype == DECIMAL_DTYPE_NAME


def test_convert_key_column_writes_categories_as_texts() -> None:
	"""
	Check that categories become texts.

	.. versionadded:: 0.1.0
	"""
	key_column = convert_key_column(CATEGORY_IDS, ndp.Type.TEXT)

	assert key_column.dtype == TEXT_DTYPE_NAME
