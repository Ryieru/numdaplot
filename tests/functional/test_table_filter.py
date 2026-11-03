"""
Functional tests of the selection of the rows and columns of a Table.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

import numdaplot as ndp

SALES = pandas.DataFrame(
	{
		"city": pandas.Series(["Paris", "Lyon", "Pau", None], dtype="string"),
		"price": [120.0, 80.0, None, 150.0],
	}
)
HIGH_LIMIT = 100.0
EXPECTED_EXPENSIVE_PRICES = [120.0, 150.0]
EXPECTED_EXPENSIVE_OR_PAU = [0, 2, 3]
EXPECTED_EXPENSIVE_IN_PARIS = [120.0]
EXPECTED_MISSING_PRICE_ROWS = 1
EXPECTED_ROWS_WITH_A_HOLE = 2
ROW_NUMBERS = [0, 1, 2, 3]
EXPECTED_LAST_PRICE = 150.0
EXPECTED_TAKEN_NAMES = ["price", "city"]


def build_sales() -> ndp.Table:
	"""
	Return a Table of four sales with a missing city and a missing price.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The sales.
	"""
	sales = ndp.Table.from_pandas(SALES)

	return sales


def read_prices(table: ndp.Table) -> list[float]:
	"""
	Return the prices of a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		A Table with a price column.

	Returns
	-------
	list[float]
		The prices.
	"""
	prices = table.column("price")
	price_list = prices.to_list()

	return price_list


def test_a_filter_keeps_the_rows_satisfying_its_condition() -> None:
	"""
	Check that prices above 100 are kept, the missing price is not.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	expensive = ndp.Condition(rule=ndp.Greater(HIGH_LIMIT), columns=["price"])

	expensive_sales = sales.filter(ndp.Filter(conditions=[expensive]))

	prices = read_prices(expensive_sales)
	assert prices == EXPECTED_EXPENSIVE_PRICES


def test_conditions_combine_with_all_or_any() -> None:
	"""
	Check expensive sales in Paris with ALL, and expensive sales or sales in Pau with ANY.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	row_numbers = ndp.Array.from_list(ROW_NUMBERS)
	sales_with_rows = sales.add_column(ndp.NewColumn(name="row", values=row_numbers))
	expensive = ndp.Condition(rule=ndp.Greater(HIGH_LIMIT), columns=["price"])
	in_paris = ndp.Condition(rule=ndp.Equal("Paris"), columns=["city"])
	in_pau = ndp.Condition(rule=ndp.Equal("Pau"), columns=["city"])

	expensive_in_paris = sales_with_rows.filter(ndp.Filter(conditions=[expensive, in_paris]))
	expensive_or_pau = sales_with_rows.filter(ndp.Filter(conditions=[expensive, in_pau], mode=ndp.FilterMode.ANY))

	paris_prices = read_prices(expensive_in_paris)
	kept_rows = expensive_or_pau.column("row")
	row_list = kept_rows.to_list()
	assert paris_prices == EXPECTED_EXPENSIVE_IN_PARIS
	assert row_list == EXPECTED_EXPENSIVE_OR_PAU


def test_missing_values_are_found_with_is_missing() -> None:
	"""
	Check one sale without price, and two rows with a hole in some column.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	missing_price = ndp.Condition(rule=ndp.IsMissing(), columns=["price"])
	any_hole = ndp.Condition(rule=ndp.IsMissing())

	without_price = sales.filter(ndp.Filter(conditions=[missing_price]))
	with_a_hole = sales.filter(ndp.Filter(conditions=[any_hole]))

	assert without_price.row_count == EXPECTED_MISSING_PRICE_ROWS
	assert with_a_hole.row_count == EXPECTED_ROWS_WITH_A_HOLE


def test_a_rule_over_every_column_must_apply_to_every_column() -> None:
	"""
	Check that a number rule without columns raises IncompatibleTypesError on a Table with texts.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	above_limit = ndp.Condition(rule=ndp.Greater(HIGH_LIMIT))

	with pytest.raises(ndp.IncompatibleTypesError):
		sales.filter(ndp.Filter(conditions=[above_limit]))


def test_take_chooses_rows_and_columns_by_position_and_name() -> None:
	"""
	Check the last price, and columns taken in the order of the region.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()

	last_price = sales.take(ndp.Region(rows=ndp.Index(-1), columns=["price"]))
	reordered = sales.take(ndp.Region(columns=["price", "city"]))

	last_price_value = last_price.to_value()
	assert last_price_value == EXPECTED_LAST_PRICE
	assert reordered.column_names == EXPECTED_TAKEN_NAMES
