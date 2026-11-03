"""
Unit tests of the conversion of Table columns to another type.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.columns.converted_column import convert_column
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
DATES = pandas.Series(numpy.array(["2026-01-31"], dtype="datetime64[s]"))
WHOLE_DECIMALS = pandas.Series([2.0, None])
EXPECTED_WHOLE_INTEGERS = [2, pandas.NA]
FRACTIONAL_DECIMALS = pandas.Series([2.0, 2.5])
FRACTIONAL_VALUE = 2.5
LARGE_INTEGERS = pandas.Series([300], dtype="Int64")
LARGE_VALUE = 300
NUMBER_TEXTS = pandas.Series(["12", "abc"], dtype="string")
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
	column = convert_column(INTEGERS, Type.FLOAT64)

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
	text_column = convert_column(column, Type.TEXT)

	texts = text_column.tolist()
	assert texts == expected_texts


def test_convert_column_makes_categories_of_numbers() -> None:
	"""
	Check that integers become a category column.

	.. versionadded:: 0.1.0
	"""
	category_column = convert_column(INTEGERS, Type.CATEGORY)

	dtype_name = str(category_column.dtype)
	assert dtype_name == CATEGORY_DTYPE_NAME


def test_convert_column_reads_texts_as_integers() -> None:
	"""
	Check that texts of integers become INT64.

	.. versionadded:: 0.1.0
	"""
	column = convert_column(TEXT_INTEGERS, Type.INT64)

	values = column.tolist()
	assert values == EXPECTED_PARSED_INTEGERS


def test_convert_column_reads_texts_as_booleans() -> None:
	"""
	Check that true and false texts become BOOL.

	.. versionadded:: 0.1.0
	"""
	column = convert_column(TEXT_BOOLEANS, Type.BOOL)

	values = column.tolist()
	assert values == EXPECTED_PARSED_BOOLEANS


def test_convert_column_copies_a_column_of_the_same_type() -> None:
	"""
	Check that converting to the same type gives a copy.

	.. versionadded:: 0.1.0
	"""
	column = convert_column(INTEGERS, Type.INT64)

	assert column is not INTEGERS


@pytest.mark.parametrize(
	("column", "target_type"),
	[
		(BOOLEANS, Type.INT64),
		(INTEGERS, Type.BOOL),
		(DATES, Type.TEXT),
		(TEXT_INTEGERS, Type.DATE),
	],
)
def test_convert_column_rejects_a_conversion_that_is_not_accepted(column: Column, target_type: Type) -> None:
	"""
	Check that booleans to numbers, numbers to booleans and date conversions raise IncompatibleTypesError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The column to convert.
	target_type
		The refused type.
	"""
	with pytest.raises(IncompatibleTypesError):
		convert_column(column, target_type)


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
