"""
Unit tests of SortKey, TableSorting and the sort of the rows of a Table.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.tables.sorting.sort_key import SortKey
from numdaplot.tables.sorting.sorted_frame import sort_frame
from numdaplot.tables.sorting.table_sorting import TableSorting

SALES = pandas.DataFrame(
	{
		"city": pandas.Series(["Pau", "Lyon", "Pau", "Lyon"], dtype="string"),
		"price": [1.0, None, 3.0, 2.0],
		"order": [1, 2, 3, 4],
	}
)
BY_CITY = SortKey(column="city")
BY_PRICE_DESCENDING = SortKey(column="price", order=Order.DESCENDING)
BY_PRICE_MISSING_FIRST = SortKey(column="price", missing=MissingPosition.FIRST)
EXPECTED_CITY_THEN_PRICE = [4, 2, 3, 1]
EXPECTED_MISSING_FIRST = [2, 1, 4, 3]
EXPECTED_STABLE_ORDER = [2, 4, 1, 3]
EXPECTED_ROW_NUMBERS = [0, 1, 2, 3]


def read_orders(frame: pandas.DataFrame) -> list[int]:
	"""
	Return the order column of sorted rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The sorted rows.

	Returns
	-------
	list[int]
		The original order of each row.
	"""
	order_column = frame["order"]
	orders = order_column.tolist()

	return orders


def test_sort_key_sorts_ascending_with_missing_values_last_by_default() -> None:
	"""
	Check the default order and place of missing values.

	.. versionadded:: 0.1.0
	"""
	key = SortKey(column="price")

	assert key.order == Order.ASCENDING
	assert key.missing == MissingPosition.LAST


def test_sorting_rejects_no_key() -> None:
	"""
	Check that an empty list raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		TableSorting(keys=[])


def test_sorting_rejects_two_keys_on_the_same_column() -> None:
	"""
	Check that two keys on price raise DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		TableSorting(keys=[BY_PRICE_DESCENDING, BY_PRICE_MISSING_FIRST])


def test_sort_frame_sorts_by_each_key_in_order() -> None:
	"""
	Check that rows are sorted by city, then by price descending, missing prices last.

	.. versionadded:: 0.1.0
	"""
	sorting = TableSorting(keys=[BY_CITY, BY_PRICE_DESCENDING])

	sorted_frame = sort_frame(SALES, sorting)

	orders = read_orders(sorted_frame)
	assert orders == EXPECTED_CITY_THEN_PRICE


def test_sort_frame_places_missing_values_first_when_asked() -> None:
	"""
	Check that a missing price comes first with MissingPosition.FIRST.

	.. versionadded:: 0.1.0
	"""
	sorting = TableSorting(keys=[BY_PRICE_MISSING_FIRST])

	sorted_frame = sort_frame(SALES, sorting)

	orders = read_orders(sorted_frame)
	assert orders == EXPECTED_MISSING_FIRST


def test_sort_frame_keeps_the_order_of_equal_rows() -> None:
	"""
	Check that rows of the same city keep their order.

	.. versionadded:: 0.1.0
	"""
	sorting = TableSorting(keys=[BY_CITY])

	sorted_frame = sort_frame(SALES, sorting)

	orders = read_orders(sorted_frame)
	assert orders == EXPECTED_STABLE_ORDER


def test_sort_frame_numbers_the_rows_from_zero() -> None:
	"""
	Check that sorted rows are renumbered.

	.. versionadded:: 0.1.0
	"""
	sorting = TableSorting(keys=[BY_PRICE_DESCENDING])

	sorted_frame = sort_frame(SALES, sorting)

	row_numbers = sorted_frame.index.tolist()
	assert row_numbers == EXPECTED_ROW_NUMBERS


def test_sort_frame_rejects_an_unknown_column() -> None:
	"""
	Check that a key on an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	sorting = TableSorting(keys=[SortKey(column="prise")])

	with pytest.raises(ColumnNotFoundError):
		sort_frame(SALES, sorting)
