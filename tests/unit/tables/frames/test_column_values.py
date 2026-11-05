"""
Unit tests of the conversion between Table columns and numpy values.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import (
	build_column,
	build_column_with_missing,
	convert_column_values,
	find_column_missing,
	find_column_type,
	read_array_values,
	read_present_values,
)

INTEGERS_WITH_MISSING = pandas.Series([1, None, 3], dtype="Int64")
EXPECTED_MISSING = [False, True, False]
EXPECTED_PRESENT_INTEGERS = [1, 3]
CATEGORIES = pandas.Series(["b", "a"], dtype="category")
EXPECTED_CATEGORY_TEXTS = ["b", "a"]
TEXT_KIND = "T"
DATES = pandas.Series(numpy.array(["2026-01-31", "NaT"], dtype="datetime64[s]"))
DAY_DTYPE = numpy.dtype("datetime64[D]")
DECIMALS_WITH_MISSING = pandas.Series([1.5, None])
EXPECTED_DECIMAL_COUNT = 2
TEXTS_WITH_MISSING = pandas.Series(["a", None], dtype="string")
CATEGORIES_WITH_MISSING = pandas.Series(["a", None], dtype="category")
BOOLEANS_WITH_MISSING = pandas.Series([True, None], dtype="boolean")
COLUMN_NAME = "age"
TEXT_VALUES = numpy.array(["a", "b"], dtype="T")
TEXT_DTYPE_NAME = "string"
INTEGER_VALUES = numpy.array([1, 3])
MISSING_POSITIONS = numpy.array([False, True, False])
EXPECTED_REBUILT_INTEGERS = [1, pandas.NA, 3]
NAIVE_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]")
PARIS_TIMES = NAIVE_TIMES.dt.tz_localize("Europe/Paris")
EXPECTED_UTC_VALUES = numpy.array(["2026-07-01T08:30"], dtype="datetime64[ns]")


def read_list(values: numpy.ndarray[Any, Any]) -> list[Any]:
	"""
	Return numpy values as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Any numpy values.

	Returns
	-------
	list[Any]
		The values.
	"""
	raw_values = values.tolist()
	value_list = cast(list[Any], raw_values)

	return value_list


def test_find_column_type_reads_the_type_of_the_dtype() -> None:
	"""
	Check that a nullable integer column is an INT64 column.

	.. versionadded:: 0.1.0
	"""
	column_type = find_column_type(INTEGERS_WITH_MISSING)

	assert column_type == Type.INT64


def test_find_column_missing_marks_the_missing_rows() -> None:
	"""
	Check the missing mask of an integer column.

	.. versionadded:: 0.1.0
	"""
	missing = find_column_missing(INTEGERS_WITH_MISSING)

	missing_list = read_list(missing)
	assert missing_list == EXPECTED_MISSING


def test_convert_column_values_gives_categories_as_texts() -> None:
	"""
	Check that a category column becomes variable-length texts.

	.. versionadded:: 0.1.0
	"""
	values = convert_column_values(CATEGORIES)

	text_list = read_list(values)
	assert values.dtype.kind == TEXT_KIND
	assert text_list == EXPECTED_CATEGORY_TEXTS


def test_convert_column_values_gives_dates_by_day() -> None:
	"""
	Check that a DATE column gives numpy dates by day.

	.. versionadded:: 0.1.0
	"""
	values = convert_column_values(DATES)

	assert values.dtype == DAY_DTYPE


def test_read_present_values_skips_missing_values() -> None:
	"""
	Check that only the present integers remain.

	.. versionadded:: 0.1.0
	"""
	values = read_present_values(INTEGERS_WITH_MISSING)

	value_list = read_list(values)
	assert value_list == EXPECTED_PRESENT_INTEGERS


def test_read_array_values_keeps_missing_decimals() -> None:
	"""
	Check that a decimal column keeps its NaN, which an Array can hold.

	.. versionadded:: 0.1.0
	"""
	values = read_array_values(DECIMALS_WITH_MISSING)

	missing = numpy.isnan(values)
	assert values.size == EXPECTED_DECIMAL_COUNT
	assert missing[1]


@pytest.mark.parametrize("column", [INTEGERS_WITH_MISSING, BOOLEANS_WITH_MISSING])
def test_read_array_values_rejects_missing_values_an_array_cannot_hold(column: Column) -> None:
	"""
	Check that integers or booleans with a missing value raise UnsupportedMissingError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column with a missing integer or boolean.
	"""
	with pytest.raises(UnsupportedMissingError):
		read_array_values(column)


def test_read_array_values_names_the_column_it_rejects() -> None:
	"""
	Check that the error gives the name of the column holding the missing values.

	.. versionadded:: 0.1.0
	"""
	named_column = INTEGERS_WITH_MISSING.rename(COLUMN_NAME)

	with pytest.raises(UnsupportedMissingError) as error_info:
		read_array_values(named_column)

	assert error_info.value.column_name == COLUMN_NAME


@pytest.mark.parametrize("column", [TEXTS_WITH_MISSING, CATEGORIES_WITH_MISSING])
def test_read_array_values_marks_missing_texts_and_categories_with_nan(column: Column) -> None:
	"""
	Check that texts and categories keep their missing value, marked with NaN.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column with a missing text or category.
	"""
	values = read_array_values(column)

	missing = numpy.isnan(values)
	assert missing.tolist() == [False, True]


def test_build_column_stores_texts_with_the_pandas_text_dtype() -> None:
	"""
	Check that numpy texts become a pandas text column.

	.. versionadded:: 0.1.0
	"""
	column = build_column(TEXT_VALUES)

	dtype_name = str(column.dtype)
	assert dtype_name == TEXT_DTYPE_NAME


def test_build_column_with_missing_places_the_missing_values() -> None:
	"""
	Check that present values fill the rows that are not missing.

	.. versionadded:: 0.1.0
	"""
	column = build_column_with_missing(INTEGER_VALUES, MISSING_POSITIONS)

	values = column.tolist()
	assert values == EXPECTED_REBUILT_INTEGERS


def test_convert_column_values_gives_the_utc_clock_time_of_a_zone_column() -> None:
	"""
	Check that 10:30 in Paris in summer gives 08:30.

	.. versionadded:: 0.1.0
	"""
	values = convert_column_values(PARIS_TIMES)

	same_values = numpy.array_equal(values, EXPECTED_UTC_VALUES)
	assert bool(same_values)


def test_read_array_values_rejects_a_zone_column() -> None:
	"""
	Check that a zone column raises TimeZoneMismatchError, an Array holding no zone.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeZoneMismatchError):
		read_array_values(PARIS_TIMES)
