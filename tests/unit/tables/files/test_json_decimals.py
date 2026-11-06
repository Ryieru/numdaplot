"""
Unit tests of the exact writing of decimal columns in a JSON file.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.files.json_decimals import (
	has_decimal_column,
	is_decimal_column,
	read_decimals,
	require_finite_values,
	write_decimal_cells,
	write_exact_objects,
	write_other_cells,
	write_rounded_texts,
	write_shortest_texts,
)

THIRD = 1 / 3
NO_ROW_FRAME = pandas.DataFrame({"price": pandas.Series([], dtype="float64")})
SINGLE_DTYPE = "float32"
FIRST_INFINITE = float("-inf")


def test_has_decimal_column_finds_a_decimal_column() -> None:
	"""
	Check a frame with decimals.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"count": [1], "price": [1.5]})

	has_decimal = has_decimal_column(frame)

	assert has_decimal is True


def test_has_decimal_column_is_false_without_decimals() -> None:
	"""
	Check a frame without decimals.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"count": [1]})

	has_decimal = has_decimal_column(frame)

	assert has_decimal is False


def test_require_finite_values_accepts_missing_values() -> None:
	"""
	Check that NaN is not an infinite value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([numpy.nan, 1.5])

	require_finite_values(values)


def test_require_finite_values_names_the_first_infinite_value() -> None:
	"""
	Check the rejected value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([1.5, FIRST_INFINITE, numpy.inf])

	with pytest.raises(ValueConversionError) as error_info:
		require_finite_values(values)

	assert error_info.value.rejected_value == FIRST_INFINITE


def test_write_shortest_texts_writes_every_digit_of_a_double() -> None:
	"""
	Check a ``FLOAT64`` value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([THIRD])

	texts = write_shortest_texts(values)

	assert texts == [repr(THIRD)]


def test_write_shortest_texts_writes_null_for_a_missing_single() -> None:
	"""
	Check a missing ``FLOAT32`` value beside a present one.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([numpy.nan, 0.1], dtype=SINGLE_DTYPE)

	texts = write_shortest_texts(values)

	assert texts == ["null", "0.1"]


def test_write_rounded_texts_keeps_the_zeros() -> None:
	"""
	Check the number of decimals, and a missing value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([1.5, numpy.nan])

	texts = write_rounded_texts(values, 3)

	assert texts == ["1.500", "null"]


def test_write_decimal_cells_escapes_the_name() -> None:
	"""
	Check a column name that needs an escape, and a letter that does not.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([1.5])

	cells = write_decimal_cells(column, 'pr"ié', None)

	assert cells == ['"pr\\"ié":1.5']


def test_write_decimal_cells_names_the_column_of_an_infinite_value() -> None:
	"""
	Check the column named by the error.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([numpy.inf], name="price")

	with pytest.raises(ValueConversionError) as error_info:
		write_decimal_cells(column, "price", None)

	assert error_info.value.column_name == "price"


def test_write_other_cells_keeps_a_line_break_in_a_text() -> None:
	"""
	Check that a text with a line break stays in its row.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"city": ["a\nb", "c"]})

	cells = write_other_cells(frame)

	assert cells == ['"city":"a\\nb"', '"city":"c"']


def test_write_exact_objects_keeps_the_order_of_the_columns() -> None:
	"""
	Check decimals before, between and after other columns.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"a": [1.5], "b": [1], "c": ["x"], "d": [2.5], "e": [2]})

	objects = write_exact_objects(frame, None)

	assert objects == ['{"a":1.5,"b":1,"c":"x","d":2.5,"e":2}']


def test_write_exact_objects_gives_no_object_without_row() -> None:
	"""
	Check a frame without row.

	.. versionadded:: 0.1.0
	"""
	objects = write_exact_objects(NO_ROW_FRAME, None)

	assert objects == []


def test_is_decimal_column_finds_nullable_decimals() -> None:
	"""
	Check the decimals a Table stores.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([1.5], dtype="Float32")

	is_decimal = is_decimal_column(column)

	assert is_decimal is True


def test_read_decimals_keeps_the_number_of_bits() -> None:
	"""
	Check a 32 bit column with a missing value.

	.. versionadded:: 0.1.0
	"""
	column = pandas.Series([0.5, None], dtype="Float32")

	values = read_decimals(column)

	assert values.dtype == numpy.dtype(SINGLE_DTYPE)
	assert numpy.isnan(values[1])
