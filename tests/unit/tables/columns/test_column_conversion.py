"""
Unit tests of the conversion of Table columns to another type.

.. versionadded:: 0.1.0
"""

import math
from typing import Any

import numpy
import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.columns.boolean_rule import BooleanRule
from numdaplot.tables.columns.conversion import Conversion
from numdaplot.tables.columns.converted_column import (
	convert_column,
	convert_plain_column,
	convert_times,
	read_plain_column,
	write_plain_column,
)
from numdaplot.tables.columns.number_conversion import (
	convert_numbers,
	find_lost_values,
	parse_numbers,
	require_no_failed_value,
	require_no_lost_value,
	store_numbers,
)
from numdaplot.tables.columns.text_conversion import parse_booleans
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.time_zones import find_column_time_zone

INTEGERS = pandas.Series([1, None, 3], dtype="Int64")
EXPECTED_DECIMALS = [1.0, None, 3.0]
EXPECTED_INTEGER_TEXTS = ["1", pandas.NA, "3"]
BOOLEANS = pandas.Series([True, None], dtype="boolean")
EXPECTED_BOOLEAN_TEXTS = ["True", pandas.NA]
CATEGORY_DTYPE_NAME = "category"
TEXT_INTEGERS = pandas.Series(["1", None, "3"], dtype="string")
EXPECTED_PARSED_INTEGERS = [1, pandas.NA, 3]
TEXT_BOOLEANS = pandas.Series(["TRUE", " false "], dtype="string")
EXPECTED_PARSED_BOOLEANS = [True, False]
EXPECTED_TRUE_NUMBER = 1.0
ZERO_ONE_INTEGERS = pandas.Series([1, None, 0], dtype="Int64")
EXPECTED_INTEGER_BOOLEANS = [True, pandas.NA, False]
TWO_AND_ZERO = pandas.Series([2, 0], dtype="Int64")
EXPECTED_NONZERO_BOOLEANS = [True, False]
EXPECTED_CATEGORY_TEXTS = ["True", pandas.NA]
DATES = pandas.Series(numpy.array(["2026-01-31"], dtype="datetime64[s]"))
WHOLE_DECIMALS = pandas.Series([2.0, None])
EXPECTED_WHOLE_INTEGERS = [2, pandas.NA]
FRACTIONAL_DECIMALS = pandas.Series([2.0, 2.5])
FRACTIONAL_VALUE = 2.5
LARGE_INTEGERS = pandas.Series([300], dtype="Int64")
LARGE_VALUE = 300
NUMBER_TEXTS = pandas.Series(["12", "abc"], dtype="string")
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
REJECTED_TEXT = "abc"
DECIMAL_TEXTS = pandas.Series(["2.5"], dtype="string")
REJECTED_DECIMAL_TEXT = "2.5"
WORD_TEXTS = pandas.Series(["yes"], dtype="string")
REJECTED_WORD = "yes"
DECIMAL_VALUES = numpy.array([2.0, 2.5])
STORED_INTEGERS = numpy.array([2, 2])
EXPECTED_LOST = [False, True]
HUGE_DECIMALS = numpy.array([1e300])
SMALL_DECIMALS = numpy.array([numpy.inf], dtype=numpy.float32)
EXPECTED_OVERFLOW = [True]
FAILED_VALUES = numpy.array(["12", "abc"])
FAILED_MASK = numpy.array([False, True])
NO_FAILURE = numpy.array([False, False])
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
	conversion = Conversion(column=CONVERTED_NAME, dtype=target_type)
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


def test_convert_numbers_stores_whole_decimals_as_integers() -> None:
	"""
	Check that 2.0 becomes 2, the missing value staying missing.

	.. versionadded:: 0.1.0
	"""
	column = convert_numbers(WHOLE_DECIMALS, Type.INT64)

	values = column.tolist()
	assert values == EXPECTED_WHOLE_INTEGERS


@pytest.mark.parametrize(
	("column", "target_type", "rejected_value"),
	[
		(FRACTIONAL_DECIMALS, Type.INT64, FRACTIONAL_VALUE),
		(LARGE_INTEGERS, Type.INT8, LARGE_VALUE),
	],
)
def test_convert_numbers_rejects_a_value_that_does_not_fit(
	column: Column,
	target_type: Type,
	rejected_value: float,
) -> None:
	"""
	Check that 2.5 to INT64 and 300 to INT8 raise ValueConversionError naming the value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The numbers.
	target_type
		The type they do not fit in.
	rejected_value
		The first number that does not fit.
	"""
	with pytest.raises(ValueConversionError) as error_info:
		convert_numbers(column, target_type)

	error = error_info.value
	assert error.rejected_value == rejected_value


@pytest.mark.parametrize(
	("column", "rejected_text"),
	[
		(NUMBER_TEXTS, REJECTED_TEXT),
		(DECIMAL_TEXTS, REJECTED_DECIMAL_TEXT),
	],
)
def test_parse_numbers_names_the_first_text_that_is_not_an_integer(column: Column, rejected_text: str) -> None:
	"""
	Check that a word, or a decimal read as an integer, raises ValueConversionError naming the text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The texts.
	rejected_text
		The first text that cannot be an integer.
	"""
	with pytest.raises(ValueConversionError) as error_info:
		parse_numbers(column, Type.INT64)

	error = error_info.value
	assert error.rejected_value == rejected_text


def test_parse_booleans_names_the_first_unknown_text() -> None:
	"""
	Check that a text other than true or false raises ValueConversionError naming it.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		parse_booleans(WORD_TEXTS)

	error = error_info.value
	assert error.rejected_value == REJECTED_WORD


def test_store_numbers_uses_the_numpy_dtype_of_the_type() -> None:
	"""
	Check the dtype of stored integers.

	.. versionadded:: 0.1.0
	"""
	stored_values = store_numbers(DECIMAL_VALUES, Type.INT16)

	assert stored_values.dtype == numpy.int16


def test_find_lost_values_marks_changed_integers() -> None:
	"""
	Check that 2.5 stored as 2 is lost.

	.. versionadded:: 0.1.0
	"""
	lost = find_lost_values(DECIMAL_VALUES, STORED_INTEGERS)

	lost_list = lost.tolist()
	assert lost_list == EXPECTED_LOST


def test_find_lost_values_marks_decimals_that_became_infinite() -> None:
	"""
	Check that a finite decimal too large for FLOAT32 is lost.

	.. versionadded:: 0.1.0
	"""
	lost = find_lost_values(HUGE_DECIMALS, SMALL_DECIMALS)

	lost_list = lost.tolist()
	assert lost_list == EXPECTED_OVERFLOW


def test_require_no_lost_value_accepts_unchanged_numbers() -> None:
	"""
	Check that numbers stored without change pass.

	.. versionadded:: 0.1.0
	"""
	require_no_lost_value(STORED_INTEGERS, STORED_INTEGERS, Type.INT64, Type.INT64)


def test_require_no_failed_value_accepts_no_failure() -> None:
	"""
	Check that a mask without failure passes.

	.. versionadded:: 0.1.0
	"""
	require_no_failed_value(FAILED_VALUES, NO_FAILURE, Type.TEXT, Type.INT64)


def test_require_no_failed_value_names_the_first_failure() -> None:
	"""
	Check that the first failed value is in the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		require_no_failed_value(FAILED_VALUES, FAILED_MASK, Type.TEXT, Type.INT64)

	error = error_info.value
	assert error.rejected_value == REJECTED_TEXT


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
	conversion = Conversion(column=CONVERTED_NAME, dtype=Type.DATETIME, timezone=ATTRIBUTE_UTC)

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
	conversion = Conversion(column=CONVERTED_NAME, dtype=Type.BOOL, booleans=BooleanRule.NONZERO_TRUE)

	column = convert_column(TWO_AND_ZERO, conversion)

	values = column.tolist()
	assert values == EXPECTED_NONZERO_BOOLEANS


def test_convert_plain_column_writes_booleans_as_texts() -> None:
	"""
	Check that a conversion to TEXT goes through the writing of the values.

	.. versionadded:: 0.1.0
	"""
	conversion = Conversion(column=CONVERTED_NAME, dtype=Type.TEXT)

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
	conversion = Conversion(column=CONVERTED_NAME, dtype=Type.DATE)

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
