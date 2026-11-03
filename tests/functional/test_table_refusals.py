"""
Functional tests of the Python operations a Table refuses.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRICES = [1.5, 8.0]
EXPECTED_BRACKETS_MESSAGE = "Brackets on a Table is not available, use column, take or filter instead."
EXPECTED_ITERATION_MESSAGE = (
	"Iterating over a Table with for is not available, use for value in table.column(name).to_list() instead."
)


def build_prices() -> ndp.Table:
	"""
	Return a Table of two prices.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The prices.
	"""
	prices = ndp.Array.from_list(PRICES)
	table = ndp.Table.from_arrays({"price": prices})

	return table


def test_brackets_point_to_column_take_and_filter() -> None:
	"""
	Check the message of table["price"].

	.. versionadded:: 0.1.0
	"""
	table = build_prices()

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		table["price"]

	error_text = str(error_info.value)
	assert error_text == EXPECTED_BRACKETS_MESSAGE


def test_iteration_points_to_the_values_of_a_column() -> None:
	"""
	Check the message of a for loop over a Table, and that its suggestion works.

	.. versionadded:: 0.1.0
	"""
	table = build_prices()
	prices = table.column("price")
	price_list = prices.to_list()

	with pytest.raises(ndp.RefusedOperationError) as error_info:
		list(table)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_ITERATION_MESSAGE
	assert price_list == PRICES


def test_comparing_two_tables_goes_through_is_equal() -> None:
	"""
	Check that == raises RefusedOperationError while is_equal answers.

	.. versionadded:: 0.1.0
	"""
	table = build_prices()
	same_table = build_prices()

	with pytest.raises(ndp.RefusedOperationError):
		_ = table == same_table

	is_equal = table.is_equal(ndp.Equality(other=same_table))
	assert is_equal
