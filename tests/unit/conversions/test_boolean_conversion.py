"""
Unit tests of the conversion of Table columns between booleans and numbers.

.. versionadded:: 0.1.0
"""

import math

import numpy
import pandas
import pytest

from numdaplot.conversions.boolean_conversion import (
	convert_booleans_to_numbers,
	convert_numbers_to_booleans,
	require_zero_or_one,
)
from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.types.type import Type

BOOLEANS = pandas.Series([True, None, False], dtype="boolean")
EXPECTED_INTEGERS = [1, pandas.NA, 0]
ZERO_ONE_INTEGERS = pandas.Series([1, None, 0], dtype="Int64")
EXPECTED_BOOLEANS = [True, pandas.NA, False]
OTHER_INTEGERS = pandas.Series([1, 3, -1, 0], dtype="Int64")
EXPECTED_NONZERO_BOOLEANS = [True, True, True, False]
WHOLE_DECIMALS = pandas.Series([1.0, 0.0])
EXPECTED_WHOLE_BOOLEANS = [True, False]
INFINITE_DECIMALS = pandas.Series([1.0, math.inf])
EXPECTED_INFINITE_BOOLEANS = [True, True]
ZERO_ONE_NUMBERS = numpy.array([0, 1, 1])
OTHER_NUMBERS = numpy.array([1, 2, 5])
EXPECTED_REJECTED_MESSAGE = "Cannot store the INT64 value 2 as BOOL without losing information."
NUMBER_TYPES = [Type.INT8, Type.UINT8, Type.INT64, Type.FLOAT32, Type.FLOAT64]


@pytest.mark.parametrize("target_type", NUMBER_TYPES)
def test_convert_booleans_to_numbers_stores_the_number_type(target_type: Type) -> None:
	"""
	Check that booleans become any number type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target_type
		A number type.
	"""
	number_column = convert_booleans_to_numbers(BOOLEANS, target_type)

	column_type = find_column_type(number_column)
	assert column_type == target_type


def test_convert_booleans_to_numbers_gives_one_and_zero() -> None:
	"""
	Check that True gives 1, False gives 0 and a missing value stays missing.

	.. versionadded:: 0.1.0
	"""
	number_column = convert_booleans_to_numbers(BOOLEANS, Type.INT64)

	numbers = number_column.tolist()
	assert numbers == EXPECTED_INTEGERS


def test_convert_numbers_to_booleans_reads_zero_and_one() -> None:
	"""
	Check that ZERO_ONE gives False for 0, True for 1 and keeps missing values.

	.. versionadded:: 0.1.0
	"""
	boolean_column = convert_numbers_to_booleans(ZERO_ONE_INTEGERS, BooleanRule.ZERO_ONE)

	booleans = boolean_column.tolist()
	assert booleans == EXPECTED_BOOLEANS


def test_convert_numbers_to_booleans_reads_whole_decimals() -> None:
	"""
	Check that ZERO_ONE accepts 0.0 and 1.0.

	.. versionadded:: 0.1.0
	"""
	boolean_column = convert_numbers_to_booleans(WHOLE_DECIMALS, BooleanRule.ZERO_ONE)

	booleans = boolean_column.tolist()
	assert booleans == EXPECTED_WHOLE_BOOLEANS


@pytest.mark.parametrize("numbers", [OTHER_INTEGERS, INFINITE_DECIMALS])
def test_convert_numbers_to_booleans_rejects_other_numbers_with_zero_one(numbers: pandas.Series) -> None:
	"""
	Check that ZERO_ONE refuses any number but 0 and 1, infinite values included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		A column holding another number than 0 and 1.
	"""
	with pytest.raises(ValueConversionError):
		convert_numbers_to_booleans(numbers, BooleanRule.ZERO_ONE)


def test_convert_numbers_to_booleans_reads_every_other_number_as_true() -> None:
	"""
	Check that NONZERO_TRUE gives False for 0 only.

	.. versionadded:: 0.1.0
	"""
	boolean_column = convert_numbers_to_booleans(OTHER_INTEGERS, BooleanRule.NONZERO_TRUE)

	booleans = boolean_column.tolist()
	assert booleans == EXPECTED_NONZERO_BOOLEANS


def test_convert_numbers_to_booleans_reads_an_infinite_value_as_true() -> None:
	"""
	Check that NONZERO_TRUE gives True for an infinite value.

	.. versionadded:: 0.1.0
	"""
	boolean_column = convert_numbers_to_booleans(INFINITE_DECIMALS, BooleanRule.NONZERO_TRUE)

	booleans = boolean_column.tolist()
	assert booleans == EXPECTED_INFINITE_BOOLEANS


def test_require_zero_or_one_accepts_zeros_and_ones() -> None:
	"""
	Check that 0 and 1 raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_zero_or_one(ZERO_ONE_NUMBERS, Type.INT64)


def test_require_zero_or_one_names_the_first_other_number() -> None:
	"""
	Check the message naming the first number that is neither 0 nor 1.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		require_zero_or_one(OTHER_NUMBERS, Type.INT64)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_REJECTED_MESSAGE
