"""
Functional tests of the creation of Tables and of reading their values.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

import numdaplot as ndp

CITY_INDEX = ["Paris", "Lyon"]
PRICES = [120.0, 80.0]
OBJECT_COUNTS = [2, None]
EXPECTED_OBJECT_TYPES = {"count": ndp.Type.INT64}
CHANGED_PRICE = 1.0
EXPECTED_PRICE_TOTAL = 200.0
COUNTS_WITH_HOLE = pandas.Series([2, None], dtype="Int64")
CATEGORIES = ["b", "a"]
EXPECTED_COLUMN_NAMES = ["city", "price"]
EXPECTED_COLUMN_COUNT = 2
PRICE_COLUMN_ONLY = ["price"]
EXPECTED_KEPT_COLUMN_COUNT = 1
PRICE_THRESHOLD = 100.0
EXPECTED_SALES_SHAPE = ndp.Shape([2, 2])
EXPECTED_EXPENSIVE_PRICES_SHAPE = ndp.Shape([1, 1])
SINGLE_PRICE = [9.5]
INTEGER_COUNTS = [1, 2]
DECIMAL_COUNTS = [1.0, 2.0]
EXPECTED_MISSING_COUNTS = [False, True]


def test_a_dataframe_with_a_meaningful_index_is_refused() -> None:
	"""
	Check that a DataFrame indexed by city raises UnsupportedIndexError, and works after reset_index.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"price": PRICES}, index=CITY_INDEX)
	reset_frame = frame.reset_index(names="city")

	with pytest.raises(ndp.UnsupportedIndexError):
		ndp.Table.from_pandas(frame)

	sales = ndp.Table.from_pandas(reset_frame)
	assert sales.column_names == EXPECTED_COLUMN_NAMES


def test_a_table_counts_its_columns_as_they_change() -> None:
	"""
	Check that column_count follows the columns kept by choose_columns.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"city": CITY_INDEX, "price": PRICES})
	sales = ndp.Table.from_pandas(frame)
	price_choice = ndp.ColumnChoice(columns=PRICE_COLUMN_ONLY)

	prices_only = sales.choose_columns(price_choice)

	assert sales.column_count == EXPECTED_COLUMN_COUNT
	assert prices_only.column_count == EXPECTED_KEPT_COLUMN_COUNT


def test_a_table_shape_follows_its_rows_and_columns() -> None:
	"""
	Check that shape follows the rows kept by filter and the columns kept by choose_columns.

	.. versionadded:: 0.2.0
	"""
	frame = pandas.DataFrame({"city": CITY_INDEX, "price": PRICES})
	sales = ndp.Table.from_pandas(frame)
	expensive_condition = ndp.Condition(rule=ndp.Greater(PRICE_THRESHOLD), columns=PRICE_COLUMN_ONLY)
	price_choice = ndp.ColumnChoice(columns=PRICE_COLUMN_ONLY)

	expensive_sales = sales.filter(ndp.Filter(conditions=[expensive_condition]))
	expensive_prices = expensive_sales.choose_columns(price_choice)

	assert sales.shape == EXPECTED_SALES_SHAPE
	assert expensive_prices.shape == EXPECTED_EXPENSIVE_PRICES_SHAPE


def test_python_objects_of_a_dataframe_get_their_type() -> None:
	"""
	Check that Python integers and None become an INT64 column.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"count": pandas.Series(OBJECT_COUNTS, dtype=object)})

	table = ndp.Table.from_pandas(frame)

	assert table.column_types == EXPECTED_OBJECT_TYPES


def test_a_table_keeps_its_values_when_its_dataframe_changes() -> None:
	"""
	Check that changing the DataFrame given to from_pandas, or returned by to_pandas, changes nothing.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"price": PRICES})
	sales = ndp.Table.from_pandas(frame)
	returned_frame = sales.to_pandas()

	frame.loc[0, "price"] = CHANGED_PRICE
	returned_frame.loc[1, "price"] = CHANGED_PRICE

	prices = sales.column("price")
	total = prices.compute(ndp.Sum())
	total_value = total.to_value()
	assert total_value == EXPECTED_PRICE_TOTAL


def test_a_column_with_missing_integers_must_be_converted_to_become_an_array() -> None:
	"""
	Check that column refuses missing integers, and works once converted to FLOAT64.

	.. versionadded:: 0.1.0
	"""
	frame = pandas.DataFrame({"count": COUNTS_WITH_HOLE})
	table = ndp.Table.from_pandas(frame)
	decimal_table = table.convert(ndp.TableConversion(column="count", dtype=ndp.Type.FLOAT64))

	with pytest.raises(ndp.UnsupportedMissingError):
		table.column("count")

	counts = decimal_table.column("count")
	is_missing = counts.check(ndp.IsMissing())
	missing_list = is_missing.to_list()
	assert missing_list == EXPECTED_MISSING_COUNTS


def test_a_category_column_becomes_a_text_array() -> None:
	"""
	Check that column gives a TEXT Array for a category column.

	.. versionadded:: 0.1.0
	"""
	letters = ndp.Array.from_list(CATEGORIES)
	table = ndp.Table.from_arrays({"letter": letters})
	category_table = table.convert(ndp.TableConversion(column="letter", dtype=ndp.Type.CATEGORY))

	letter_array = category_table.column("letter")

	assert letter_array.dtype == ndp.Type.TEXT


def test_arrays_of_different_lengths_are_refused() -> None:
	"""
	Check that from_arrays raises ShapeMismatchError for two lengths.

	.. versionadded:: 0.1.0
	"""
	cities = ndp.Array.from_list(CITY_INDEX)
	prices = ndp.Array.from_list(SINGLE_PRICE)

	with pytest.raises(ndp.ShapeMismatchError):
		ndp.Table.from_arrays({"city": cities, "price": prices})


def test_a_table_of_one_value_gives_its_value() -> None:
	"""
	Check that to_value reads the single value, and refuses more values.

	.. versionadded:: 0.1.0
	"""
	single_price_array = ndp.Array.from_list(SINGLE_PRICE)
	price_array = ndp.Array.from_list(PRICES)
	single_price = ndp.Table.from_arrays({"price": single_price_array})
	prices = ndp.Table.from_arrays({"price": price_array})

	value = single_price.to_value()

	assert value == SINGLE_PRICE[0]
	with pytest.raises(ndp.NotSingleValueError):
		prices.to_value()


def test_two_tables_compare_with_or_without_their_types() -> None:
	"""
	Check that integers and decimals of the same values are equal only when types are ignored.

	.. versionadded:: 0.1.0
	"""
	integer_counts = ndp.Array.from_list(INTEGER_COUNTS)
	decimal_counts = ndp.Array.from_list(DECIMAL_COUNTS)
	integers = ndp.Table.from_arrays({"count": integer_counts})
	decimals = ndp.Table.from_arrays({"count": decimal_counts})

	ignoring_types = integers.is_equal(ndp.Equality(other=decimals))
	comparing_types = integers.is_equal(ndp.Equality(other=decimals, types=ndp.TypeMatch.STRICT))

	assert ignoring_types
	assert not comparing_types
