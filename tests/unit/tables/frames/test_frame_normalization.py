"""
Unit tests of the normalization of DataFrames into Table columns.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.unsupported_index_error import UnsupportedIndexError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.frame_normalization import (
	convert_column_dtype,
	convert_decimals,
	convert_numpy_column,
	convert_to_type,
	infer_object_column,
	normalize_categories,
	normalize_column,
	normalize_frame,
	require_plain_index,
)

MIXED_FRAME = pandas.DataFrame({"count": [1, 2], "city": ["Pau", "Lyon"]})
EXPECTED_MIXED_DTYPE_NAMES = ["Int64", "string"]
CITY_INDEX = ["Paris", "Lyon"]
PRICES = {"price": [1.5, 8.0]}
NUMBER_NAMES_FRAME = pandas.DataFrame([[1, 2]])
REPEATED_NAMES_FRAME = pandas.DataFrame([[1, 2]], columns=["price", "price"])
SHUFFLED_INDEX = [1, 0]
FIXED_OFFSET_DATES = pandas.Series(pandas.to_datetime(["2026-01-31 10:00+01:00"]))
COMPLEX_NUMBERS = pandas.Series([1 + 2j])
CANONICAL_DECIMALS = pandas.Series([1.5])
NULLABLE_DECIMALS = pandas.Series([1.5, None], dtype="Float64")
DECIMAL_DTYPE_NAME = "float64"
MILLISECOND_DATES = pandas.Series(numpy.array(["2026-01-31T08:30"], dtype="datetime64[ms]"))
DATETIME_DTYPE_NAME = "datetime64[ns]"
SECOND_DURATIONS = pandas.Series(numpy.array([5], dtype="timedelta64[s]"))
DURATION_DTYPE_NAME = "timedelta64[ns]"
# Some versions of the pandas stubs do not know the na_value parameter of StringDtype.
NAN_TEXT_DTYPE = cast(Any, pandas).StringDtype(na_value=numpy.nan)
NAN_TEXTS = pandas.Series(["a"], dtype=NAN_TEXT_DTYPE)
TEXT_DTYPE_NAME = "string"
SMALL_INTEGERS = pandas.Series(numpy.array([1, 2], dtype=numpy.int16))
SMALL_INTEGER_DTYPE_NAME = "Int16"
BOOLEANS = pandas.Series([True, False])
BOOLEAN_DTYPE_NAME = "boolean"
OBJECT_INTEGERS = pandas.Series([1, None, 3], dtype=object)
EXPECTED_OBJECT_INTEGERS = [1, pandas.NA, 3]
OBJECT_MIXED = pandas.Series([1, "a", None], dtype=object)
EXPECTED_OBJECT_MIXED = ["1", "a", pandas.NA]
OBJECT_DECIMALS = pandas.Series([1, 2.5], dtype=object)
NUMBER_CATEGORIES = pandas.Series([1, 2], dtype="category")
EXPECTED_TEXT_CATEGORIES = ["1", "2"]
TEXT_CATEGORIES = pandas.Series(["a", "b"], dtype="category")


def find_dtype_names(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the dtype name of each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		Any DataFrame.

	Returns
	-------
	list[str]
		The dtype names, in order.
	"""
	dtype_names = [str(dtype) for dtype in frame.dtypes]

	return dtype_names


def test_normalize_frame_stores_each_column_with_its_table_dtype() -> None:
	"""
	Check the dtypes of integers and texts after normalization.

	.. versionadded:: 0.1.0
	"""
	normalized_frame = normalize_frame(MIXED_FRAME)

	dtype_names = find_dtype_names(normalized_frame)
	assert dtype_names == EXPECTED_MIXED_DTYPE_NAMES


def test_normalize_frame_rejects_a_number_as_column_name() -> None:
	"""
	Check that pandas default column names raise InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		normalize_frame(NUMBER_NAMES_FRAME)


def test_normalize_frame_rejects_a_repeated_column_name() -> None:
	"""
	Check that two columns of the same name raise DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		normalize_frame(REPEATED_NAMES_FRAME)


def test_normalize_frame_rejects_an_index_of_names() -> None:
	"""
	Check that an index of city names raises UnsupportedIndexError.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame(PRICES, index=CITY_INDEX)

	with pytest.raises(UnsupportedIndexError):
		normalize_frame(frame)


def test_require_plain_index_rejects_shuffled_row_numbers() -> None:
	"""
	Check that row numbers out of order raise UnsupportedIndexError.

	.. versionadded:: 0.1.0
	"""
	index = pandas.Index(SHUFFLED_INDEX)

	with pytest.raises(UnsupportedIndexError):
		require_plain_index(index)


def test_normalize_column_keeps_a_column_already_stored_for_a_table() -> None:
	"""
	Check that a float64 column is returned as it is.

	.. versionadded:: 0.1.0
	"""
	column = normalize_column(CANONICAL_DECIMALS)

	assert column is CANONICAL_DECIMALS


@pytest.mark.parametrize("column", [FIXED_OFFSET_DATES, COMPLEX_NUMBERS])
def test_normalize_column_rejects_an_unsupported_type(column: Column) -> None:
	"""
	Check that datetimes in a fixed offset and complex numbers raise UnsupportedTypeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of an unsupported type.
	"""
	with pytest.raises(UnsupportedTypeError):
		normalize_column(column)


@pytest.mark.parametrize(
	("column", "expected_dtype_name"),
	[
		(MILLISECOND_DATES, DATETIME_DTYPE_NAME),
		(SECOND_DURATIONS, DURATION_DTYPE_NAME),
		(NAN_TEXTS, TEXT_DTYPE_NAME),
		(NULLABLE_DECIMALS, DECIMAL_DTYPE_NAME),
	],
)
def test_convert_column_dtype_uses_the_table_dtype(column: Column, expected_dtype_name: str) -> None:
	"""
	Check the dtype of converted datetimes, durations, texts and decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column whose dtype a Table does not use.
	expected_dtype_name
		The dtype a Table uses for it.
	"""
	converted_column = convert_column_dtype(column)

	dtype_name = str(converted_column.dtype)
	assert dtype_name == expected_dtype_name


def test_convert_decimals_marks_missing_values_with_nan() -> None:
	"""
	Check that pd.NA becomes NaN.

	.. versionadded:: 0.1.0
	"""
	column = convert_decimals(NULLABLE_DECIMALS)

	missing = column.isna()
	missing_list = missing.tolist()
	assert missing_list == [False, True]


@pytest.mark.parametrize(
	("column", "expected_dtype_name"),
	[
		(SMALL_INTEGERS, SMALL_INTEGER_DTYPE_NAME),
		(BOOLEANS, BOOLEAN_DTYPE_NAME),
	],
)
def test_convert_numpy_column_uses_dtypes_accepting_missing_values(
	column: Column,
	expected_dtype_name: str,
) -> None:
	"""
	Check that numpy integers and booleans become nullable pandas dtypes of the same size.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A numpy integer or boolean column.
	expected_dtype_name
		The nullable dtype name.
	"""
	converted_column = convert_numpy_column(column)

	dtype_name = str(converted_column.dtype)
	assert dtype_name == expected_dtype_name


def test_convert_numpy_column_keeps_another_kind_unchanged() -> None:
	"""
	Check that a complex column is returned as it is, for the final type check to reject it.

	.. versionadded:: 0.1.0
	"""
	column = convert_numpy_column(COMPLEX_NUMBERS)

	assert column is COMPLEX_NUMBERS


def test_infer_object_column_reads_integers_with_missing_values() -> None:
	"""
	Check that Python integers and None become INT64 with a missing value.

	.. versionadded:: 0.1.0
	"""
	column = infer_object_column(OBJECT_INTEGERS)

	values = column.tolist()
	assert values == EXPECTED_OBJECT_INTEGERS


def test_infer_object_column_writes_mixed_values_as_texts() -> None:
	"""
	Check that an integer and a text become two texts.

	.. versionadded:: 0.1.0
	"""
	column = infer_object_column(OBJECT_MIXED)

	values = column.tolist()
	assert values == EXPECTED_OBJECT_MIXED


def test_infer_object_column_reads_integers_and_decimals_as_decimals() -> None:
	"""
	Check that an integer and a decimal become FLOAT64.

	.. versionadded:: 0.1.0
	"""
	column = infer_object_column(OBJECT_DECIMALS)

	dtype_name = str(column.dtype)
	assert dtype_name == DECIMAL_DTYPE_NAME


def test_normalize_categories_writes_number_categories_as_texts() -> None:
	"""
	Check that categories of numbers become categories of texts.

	.. versionadded:: 0.1.0
	"""
	column = normalize_categories(NUMBER_CATEGORIES)

	values = column.tolist()
	assert values == EXPECTED_TEXT_CATEGORIES


def test_normalize_categories_keeps_text_categories() -> None:
	"""
	Check that categories of texts are returned as they are.

	.. versionadded:: 0.1.0
	"""
	column = normalize_categories(TEXT_CATEGORIES)

	assert column is TEXT_CATEGORIES


def test_convert_to_type_uses_the_pandas_dtype_of_the_type() -> None:
	"""
	Check that integers converted to TEXT become texts.

	.. versionadded:: 0.1.0
	"""
	column = convert_to_type(SMALL_INTEGERS, Type.TEXT)

	dtype_name = str(column.dtype)
	assert dtype_name == TEXT_DTYPE_NAME
