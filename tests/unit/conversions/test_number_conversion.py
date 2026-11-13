"""
Unit tests of the conversion of Table columns to number types.

.. versionadded:: 0.2.0
"""

import numpy
import pandas
import pytest

from numdaplot.conversions.number_conversion import (
	convert_numbers,
	find_lost_values,
	parse_numbers,
	require_no_failed_value,
	require_no_lost_value,
	store_numbers,
)
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.types.type import Type

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
DECIMAL_VALUES = numpy.array([2.0, 2.5])
STORED_INTEGERS = numpy.array([2, 2])
EXPECTED_LOST = [False, True]
HUGE_DECIMALS = numpy.array([1e300])
SMALL_DECIMALS = numpy.array([numpy.inf], dtype=numpy.float32)
EXPECTED_OVERFLOW = [True]
FAILED_VALUES = numpy.array(["12", "abc"])
FAILED_MASK = numpy.array([False, True])
NO_FAILURE = numpy.array([False, False])


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
