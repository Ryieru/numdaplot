"""
Unit tests of the application of a function to columns of a Table.

.. versionadded:: 0.2.0
"""

from datetime import date
from typing import cast

import numpy
import pandas
import pytest

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.mapping.value_change import ValueChange
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import build_column_with_missing, find_column_missing, find_column_type
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.errors.dates.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.types.out_of_domain_error import OutOfDomainError
from numdaplot.math_functions.square_root import SquareRoot
from numdaplot.tables.columns.applied_columns import (
	apply_frame_columns,
	apply_to_column,
	map_present_values,
	require_column_without_time_zone,
)
from numdaplot.tables.columns.table_application import TableApplication
from numdaplot.types.type import Type

INTEGER_DTYPE = "Int64"
AREA_NAME = "area"
CITY_NAME = "city"
FRAME = pandas.DataFrame({AREA_NAME: [4.0, 9.0], CITY_NAME: ["Pau", "Dax"]})
EXPECTED_ROOTS = [2.0, 3.0]
EXPECTED_CITIES = ["Pau", "Dax"]
EXPECTED_COLUMN_NAMES = [AREA_NAME, CITY_NAME]
NEGATIVE_FRAME = pandas.DataFrame({AREA_NAME: [4.0, -1.0]})
ROOTS = TableApplication(function=SquareRoot(), columns=[AREA_NAME])
SQUARES_WITH_MISSING = pandas.Series([1, None, 9], dtype=INTEGER_DTYPE)
EXPECTED_ROOTS_WITH_MISSING = [1.0, None, 3.0]
DAYS = convert_list([date(2026, 3, 14), date(2026, 7, 1)], None)
DAY_MISSING = numpy.array([False, True, False])
EXPECTED_MONTHS = [3.0, None, 7.0]
MONTH = DatePart(unit=DatePartUnit.MONTH)
ANSWERS = numpy.array([1, 7, 9])
ANSWER_MISSING = numpy.array([False, False, True, False])
UNKNOWN_ANSWERS = ValueMapping(changes=[ValueChange(7, None)], others=Unmatched.KEEP)
EXPECTED_KNOWN_ANSWERS = [1, None, None, 9]
ONLY_UNKNOWN_ANSWERS = ValueMapping(changes=[ValueChange(1, None), ValueChange(7, None), ValueChange(9, None)])
EXPECTED_CLEARED_ANSWERS = [None, None, None, None]
ANSWER_LABELS = ValueMapping(changes=[ValueChange(1, "yes")], others=Unmatched.MISSING)
EXPECTED_ANSWER_LABELS = ["yes", None, None, None]
CODES = pandas.Series([1, 7], dtype=INTEGER_DTYPE)
EXPECTED_MAPPED_CODES = [1, None]
UTC_ZONE = "UTC"
PICKUP_NAME = "pickup"
PICKUP_TEXTS = ["2026-03-14 23:30"]
EXPECTED_ZONE_MESSAGE = "Applying a function to 'pickup' needs datetimes without a time zone."


def read_values(column: Column) -> list[object]:
	"""
	Return the values of a column, None for a missing one.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A column.

	Returns
	-------
	list[object]
		The values in order.
	"""
	missing = find_column_missing(column)
	raw_flags = missing.tolist()
	missing_flags = cast(list[bool], raw_flags)
	object_column = column.astype(object)
	raw_values = object_column.tolist()
	values = cast(list[object], raw_values)
	cleared_values = list[object]()

	for value, is_missing in zip(values, missing_flags, strict=True):
		if is_missing:
			cleared_values.append(None)
			continue

		cleared_values.append(value)

	return cleared_values


def build_zoned_pickups() -> Column:
	"""
	Return a column of datetimes with a time zone.

	.. versionadded:: 0.2.0

	Returns
	-------
	Column
		One UTC datetime, named pickup.
	"""
	naive_times = pandas.to_datetime(PICKUP_TEXTS)
	naive_column = pandas.Series(naive_times, name=PICKUP_NAME)
	zoned_column = naive_column.dt.tz_localize(UTC_ZONE)

	return zoned_column


def test_apply_frame_columns_replaces_the_listed_columns_at_their_place() -> None:
	"""
	Check that the listed column holds the results and keeps its place, the other columns unchanged.

	.. versionadded:: 0.2.0
	"""
	applied_frame = apply_frame_columns(FRAME, ROOTS)

	column_names = applied_frame.columns.tolist()
	roots = applied_frame[AREA_NAME].tolist()
	cities = applied_frame[CITY_NAME].tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert roots == EXPECTED_ROOTS
	assert cities == EXPECTED_CITIES


def test_apply_frame_columns_names_the_failing_column() -> None:
	"""
	Check that an error about a value names its column.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(OutOfDomainError) as error_info:
		apply_frame_columns(NEGATIVE_FRAME, ROOTS)

	assert error_info.value.column_name == AREA_NAME


def test_apply_to_column_applies_a_math_function_to_the_present_values() -> None:
	"""
	Check that a math function skips the missing values of an integer column, which stay missing.

	.. versionadded:: 0.2.0
	"""
	roots = apply_to_column(SQUARES_WITH_MISSING, SquareRoot())

	root_values = read_values(roots)
	assert root_values == EXPECTED_ROOTS_WITH_MISSING


def test_apply_to_column_applies_a_time_function_to_the_present_values() -> None:
	"""
	Check that a time function skips the missing values of a date column, which stay missing.

	.. versionadded:: 0.2.0
	"""
	days = build_column_with_missing(DAYS, DAY_MISSING)

	months = apply_to_column(days, MONTH)

	month_values = read_values(months)
	assert month_values == EXPECTED_MONTHS


def test_apply_to_column_maps_the_present_values() -> None:
	"""
	Check that a value mapping gives an integer column missing values without changing its type.

	.. versionadded:: 0.2.0
	"""
	mapped_codes = apply_to_column(CODES, UNKNOWN_ANSWERS)

	mapped_values = read_values(mapped_codes)
	mapped_type = find_column_type(mapped_codes)
	assert mapped_values == EXPECTED_MAPPED_CODES
	assert mapped_type == Type.INT64


def test_apply_to_column_rejects_datetimes_with_a_time_zone() -> None:
	"""
	Check that datetimes with a time zone raise TimeZoneMismatchError.

	.. versionadded:: 0.2.0
	"""
	pickups = build_zoned_pickups()

	with pytest.raises(TimeZoneMismatchError):
		apply_to_column(pickups, MONTH)


def test_map_present_values_adds_the_missing_values_of_the_mapping() -> None:
	"""
	Check that the missing values of the column and the None new values are both missing.

	.. versionadded:: 0.2.0
	"""
	mapped_column = map_present_values(ANSWERS, ANSWER_MISSING, UNKNOWN_ANSWERS)

	mapped_values = read_values(mapped_column)
	mapped_type = find_column_type(mapped_column)
	assert mapped_values == EXPECTED_KNOWN_ANSWERS
	assert mapped_type == Type.INT64


def test_map_present_values_keeps_the_type_when_every_new_value_is_missing() -> None:
	"""
	Check that a mapping giving only None keeps the integer type, every value missing.

	.. versionadded:: 0.2.0
	"""
	mapped_column = map_present_values(ANSWERS, ANSWER_MISSING, ONLY_UNKNOWN_ANSWERS)

	mapped_values = read_values(mapped_column)
	mapped_type = find_column_type(mapped_column)
	assert mapped_values == EXPECTED_CLEARED_ANSWERS
	assert mapped_type == Type.INT64


def test_map_present_values_gives_the_type_of_the_new_values() -> None:
	"""
	Check that text new values give a text column.

	.. versionadded:: 0.2.0
	"""
	mapped_column = map_present_values(ANSWERS, ANSWER_MISSING, ANSWER_LABELS)

	mapped_values = read_values(mapped_column)
	mapped_type = find_column_type(mapped_column)
	assert mapped_values == EXPECTED_ANSWER_LABELS
	assert mapped_type == Type.TEXT


def test_require_column_without_time_zone_accepts_datetimes_without_time_zone() -> None:
	"""
	Check that datetimes without time zone pass.

	.. versionadded:: 0.2.0
	"""
	pickups = build_zoned_pickups()
	naive_pickups = pickups.dt.tz_localize(None)

	require_column_without_time_zone(naive_pickups)


def test_require_column_without_time_zone_names_the_column() -> None:
	"""
	Check that datetimes with a time zone raise TimeZoneMismatchError naming the column.

	.. versionadded:: 0.2.0
	"""
	pickups = build_zoned_pickups()

	with pytest.raises(TimeZoneMismatchError) as error_info:
		require_column_without_time_zone(pickups)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_ZONE_MESSAGE
