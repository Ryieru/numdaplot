"""
Unit tests of the conversion of Table columns to another type.

.. versionadded:: 0.1.0
"""

import math
from typing import Any

import numpy
import pandas
import pytest

from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_type
from numdaplot.column_storage.time_zones import find_column_time_zone
from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.conversions.converted_column import (
	convert_column,
	convert_plain_column,
	convert_times,
	read_plain_column,
	write_plain_column,
)
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.types.type import Type

INTEGERS = pandas.Series([1, None, 3], dtype="Int64")
EXPECTED_DECIMALS = [1.0, None, 3.0]
EXPECTED_INTEGER_TEXTS = ["1", pandas.NA, "3"]
BOOLEANS = pandas.Series([True, None], dtype="boolean")
EXPECTED_BOOLEAN_TEXTS = ["True", pandas.NA]
CATEGORY_DTYPE_NAME = "category"
TEXT_INTEGERS = pandas.Series(["1", None, "3"], dtype="string")
EXPECTED_PARSED_INTEGERS = [1, pandas.NA, 3]
ARRAY_INTEGER_CONVERSION = ArrayConversion(dtype=Type.INT64)
TEXT_BOOLEANS = pandas.Series(["TRUE", " false "], dtype="string")
EXPECTED_PARSED_BOOLEANS = [True, False]
EXPECTED_TRUE_NUMBER = 1.0
ZERO_ONE_INTEGERS = pandas.Series([1, None, 0], dtype="Int64")
EXPECTED_INTEGER_BOOLEANS = [True, pandas.NA, False]
TWO_AND_ZERO = pandas.Series([2, 0], dtype="Int64")
EXPECTED_NONZERO_BOOLEANS = [True, False]
EXPECTED_CATEGORY_TEXTS = ["True", pandas.NA]
DATES = pandas.Series(numpy.array(["2026-01-31"], dtype="datetime64[s]"))
CONVERTED_NAME = "value"
UTC_ZONE = TimeZone("UTC")
ATTRIBUTE_UTC = TimeZoneChange(mode=TimeZoneMode.ATTRIBUTE, zone=UTC_ZONE)
DATE_TEXTS = pandas.Series(["2026-01-31"], dtype="string")
DATETIMES = pandas.Series(numpy.array(["2026-01-31T10:30"], dtype="datetime64[ns]"))
DURATIONS = pandas.Series(numpy.array([36], dtype="timedelta64[h]").astype("timedelta64[ns]"))
TIME_CONVERSIONS = [
	(DATES, Type.TEXT),
	(DATES, Type.CATEGORY),
	(DATES, Type.DATETIME),
	(DATETIMES, Type.DATE),
	(DURATIONS, Type.TEXT),
	(DURATIONS, Type.CATEGORY),
]
CLOCK_TEXTS = pandas.Series(["15:35"], dtype="string")
TIME_STORAGE_NAME = "timedelta64[us]"
STORED_TIMES = pandas.Series(numpy.array([56100000000], dtype="timedelta64[us]"))
EXPECTED_TIME_TEXTS = ["15:35:00"]


def convert_to(column: Column, target_type: Type) -> Column:
	"""
	Return a column converted to a type, without format nor time zone change.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The column to convert.
	target_type
		Its new type.

	Returns
	-------
	Column
		The converted column.
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=target_type)
	converted_column = convert_column(column, conversion)

	return converted_column


def read_values(column: Column) -> list[Any]:
	"""
	Return the values of a column, with None for a missing decimal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		Any column.

	Returns
	-------
	list[Any]
		The values.
	"""
	raw_values = column.tolist()
	missing = column.isna()
	missing_flags = missing.tolist()
	values = [None if is_missing else value for value, is_missing in zip(raw_values, missing_flags, strict=True)]

	return values


def test_convert_column_converts_integers_to_decimals() -> None:
	"""
	Check that INT64 becomes FLOAT64 with NaN at the missing value.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(INTEGERS, Type.FLOAT64)

	values = read_values(column)
	assert values == EXPECTED_DECIMALS


@pytest.mark.parametrize(
	("column", "expected_texts"),
	[
		(INTEGERS, EXPECTED_INTEGER_TEXTS),
		(BOOLEANS, EXPECTED_BOOLEAN_TEXTS),
	],
)
def test_convert_column_writes_numbers_and_booleans_as_texts(column: Column, expected_texts: list[Any]) -> None:
	"""
	Check the texts of integers and booleans.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		An integer or boolean column.
	expected_texts
		Its texts.
	"""
	text_column = convert_to(column, Type.TEXT)

	texts = text_column.tolist()
	assert texts == expected_texts


def test_convert_column_makes_categories_of_numbers() -> None:
	"""
	Check that integers become a category column.

	.. versionadded:: 0.1.0
	"""
	category_column = convert_to(INTEGERS, Type.CATEGORY)

	dtype_name = str(category_column.dtype)
	assert dtype_name == CATEGORY_DTYPE_NAME


def test_convert_column_reads_texts_as_integers() -> None:
	"""
	Check that texts of integers become INT64.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(TEXT_INTEGERS, Type.INT64)

	values = column.tolist()
	assert values == EXPECTED_PARSED_INTEGERS


def test_convert_column_accepts_an_array_conversion() -> None:
	"""
	Check that the settings of an Array, which have no time zone change, convert a column too.

	.. versionadded:: 0.2.0
	"""
	column = convert_column(TEXT_INTEGERS, ARRAY_INTEGER_CONVERSION)

	values = column.tolist()
	assert values == EXPECTED_PARSED_INTEGERS


def test_convert_column_reads_texts_as_booleans() -> None:
	"""
	Check that true and false texts become BOOL.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(TEXT_BOOLEANS, Type.BOOL)

	values = column.tolist()
	assert values == EXPECTED_PARSED_BOOLEANS


def test_convert_column_copies_a_column_of_the_same_type() -> None:
	"""
	Check that converting to the same type gives a copy.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(INTEGERS, Type.INT64)

	assert column is not INTEGERS


@pytest.mark.parametrize(
	("column", "target_type"),
	[
		(BOOLEANS, Type.DATE),
		(DATES, Type.INT64),
		(DATES, Type.BOOL),
		(INTEGERS, Type.DATE),
	],
)
def test_convert_column_rejects_a_conversion_that_is_not_accepted(column: Column, target_type: Type) -> None:
	"""
	Check that conversions of booleans to dates, of dates to numbers or booleans and of numbers to dates raise.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The column to convert.
	target_type
		The refused type.
	"""
	with pytest.raises(IncompatibleTypesError):
		convert_to(column, target_type)


def test_convert_column_reads_texts_as_dates_by_default() -> None:
	"""
	Check that texts become dates read year, month, day without format.

	.. versionadded:: 0.1.0
	"""
	dates = convert_to(DATE_TEXTS, Type.DATE)

	date_type = find_column_type(dates)
	assert date_type == Type.DATE


@pytest.mark.parametrize(("column", "target_type"), TIME_CONVERSIONS)
def test_convert_column_converts_dates_datetimes_and_durations(column: Column, target_type: Type) -> None:
	"""
	Check dates to texts, categories and datetimes, and durations to texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The column to convert.
	target_type
		Its new type.
	"""
	converted_column = convert_to(column, target_type)

	converted_type = find_column_type(converted_column)
	assert converted_type == target_type


def test_convert_column_changes_the_time_zone() -> None:
	"""
	Check that a time zone change gives a column in the zone.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATETIME, timezone=ATTRIBUTE_UTC)

	zone_column = convert_column(DATETIMES, conversion)

	time_zone = find_column_time_zone(zone_column)
	assert time_zone == UTC_ZONE


def test_convert_column_converts_booleans_to_decimals() -> None:
	"""
	Check that True gives 1.0 and a missing boolean stays missing.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(BOOLEANS, Type.FLOAT64)

	values = column.tolist()
	true_number = values[0]
	missing_number = values[1]
	is_missing = math.isnan(missing_number)
	assert true_number == EXPECTED_TRUE_NUMBER
	assert is_missing


def test_convert_column_reads_zeros_and_ones_as_booleans_by_default() -> None:
	"""
	Check that a conversion of numbers to BOOL without boolean rule reads 0 and 1.

	.. versionadded:: 0.1.0
	"""
	column = convert_to(ZERO_ONE_INTEGERS, Type.BOOL)

	values = column.tolist()
	assert values == EXPECTED_INTEGER_BOOLEANS


def test_convert_column_rejects_another_number_than_zero_or_one_by_default() -> None:
	"""
	Check that a conversion of numbers to BOOL without boolean rule refuses 2.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		convert_to(TWO_AND_ZERO, Type.BOOL)


def test_convert_column_applies_the_given_boolean_rule() -> None:
	"""
	Check that NONZERO_TRUE reads 2 as True.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=Type.BOOL, booleans=BooleanRule.NONZERO_TRUE)

	column = convert_column(TWO_AND_ZERO, conversion)

	values = column.tolist()
	assert values == EXPECTED_NONZERO_BOOLEANS


def test_convert_plain_column_writes_booleans_as_texts() -> None:
	"""
	Check that a conversion to TEXT goes through the writing of the values.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=Type.TEXT)

	column = convert_plain_column(BOOLEANS, Type.BOOL, conversion)

	values = column.tolist()
	assert values == EXPECTED_BOOLEAN_TEXTS


def test_write_plain_column_writes_booleans_as_categories() -> None:
	"""
	Check that booleans become categories written as Python writes them.

	.. versionadded:: 0.1.0
	"""
	column = write_plain_column(BOOLEANS, Type.BOOL, Type.CATEGORY)

	dtype_name = str(column.dtype)
	values = column.tolist()
	assert dtype_name == CATEGORY_DTYPE_NAME
	assert values == EXPECTED_CATEGORY_TEXTS


def test_write_plain_column_rejects_dates() -> None:
	"""
	Check that a column of another family than numbers, booleans and texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		write_plain_column(DATES, Type.DATE, Type.TEXT)


def test_read_plain_column_rejects_booleans_read_as_dates() -> None:
	"""
	Check that a conversion of booleans to dates raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	conversion = TableConversion(columns=[CONVERTED_NAME], dtype=Type.DATE)

	with pytest.raises(IncompatibleTypesError):
		read_plain_column(BOOLEANS, Type.BOOL, conversion)


def test_convert_times_reads_texts_as_times() -> None:
	"""
	Check the conversion of texts to TIME.

	.. versionadded:: 0.1.0
	"""
	time_column = convert_times(CLOCK_TEXTS, Type.TEXT, Type.TIME, None)

	assert time_column is not None
	assert str(time_column.dtype) == TIME_STORAGE_NAME


def test_convert_times_writes_times_as_texts() -> None:
	"""
	Check the conversion of TIME to TEXT.

	.. versionadded:: 0.1.0
	"""
	text_column = convert_times(STORED_TIMES, Type.TIME, Type.TEXT, None)

	assert text_column is not None
	texts = text_column.tolist()
	assert texts == EXPECTED_TIME_TEXTS


@pytest.mark.parametrize(
	("source_type", "target_type"), [(Type.DATE, Type.TIME), (Type.TIME, Type.DATETIME), (Type.TIME, Type.DURATION)]
)
def test_convert_times_gives_none_for_a_refused_conversion(source_type: Type, target_type: Type) -> None:
	"""
	Check that dates to times, and times to datetimes or durations, are not converted here.

	.. versionadded:: 0.1.0

	Parameters
	----------
	source_type
		The type of the column.
	target_type
		The new type.
	"""
	converted_column = convert_times(STORED_TIMES, source_type, target_type, None)

	assert converted_column is None
