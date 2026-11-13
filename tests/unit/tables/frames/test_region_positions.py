"""
Unit tests of the positions of a Region inside a Table.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_position_error import InvalidPositionError
from numdaplot.positions.first import First
from numdaplot.positions.index import Index
from numdaplot.positions.last import Last
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region
from numdaplot.tables.frames.region_positions import find_column_positions, take_region

FRAME = pandas.DataFrame({"city": ["Paris", "Lyon", "Pau"], "price": [1.5, 8.0, 3.0]})
COLUMN_NAMES = ["city", "price"]
LAST_ROW_PRICE = Region(rows=Index(-1), columns=["price"])
EXPECTED_LAST_PRICES = [3.0]
LAST_TWO_ROWS = Region(rows=Range(start=1, stop=2))
EXPECTED_ROW_NUMBERS = [0, 1]
OUTSIDE_ROW = Region(rows=Index(3))
EXPECTED_NAMED_POSITIONS = [1, 0]
EXPECTED_ALL_POSITIONS = [0, 1]
EXPECTED_SECOND_POSITION = [1]
EXPECTED_FIRST_POSITION = [0]


def read_positions(positions: numpy.ndarray[Any, Any]) -> list[int]:
	"""
	Return positions as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		numpy positions.

	Returns
	-------
	list[int]
		The positions.
	"""
	raw_positions = positions.tolist()
	position_list = cast(list[int], raw_positions)

	return position_list


def test_take_region_takes_the_rows_and_named_columns() -> None:
	"""
	Check that the last row of the price column is taken.

	.. versionadded:: 0.1.0
	"""
	region_frame = take_region(FRAME, LAST_ROW_PRICE)

	price_column = region_frame["price"]
	prices = price_column.tolist()
	column_names = region_frame.columns.tolist()
	assert prices == EXPECTED_LAST_PRICES
	assert column_names == ["price"]


def test_take_region_numbers_the_rows_from_zero() -> None:
	"""
	Check that taken rows are renumbered.

	.. versionadded:: 0.1.0
	"""
	region_frame = take_region(FRAME, LAST_TWO_ROWS)

	row_numbers = region_frame.index.tolist()
	assert row_numbers == EXPECTED_ROW_NUMBERS


def test_take_region_rejects_a_row_outside_the_table() -> None:
	"""
	Check that a fourth row of a three-row Table raises InvalidPositionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidPositionError):
		take_region(FRAME, OUTSIDE_ROW)


def test_find_column_positions_follows_the_order_of_the_names() -> None:
	"""
	Check that names give their positions in the order of the list.

	.. versionadded:: 0.1.0
	"""
	positions = find_column_positions(["price", "city"], COLUMN_NAMES)

	position_list = read_positions(positions)
	assert position_list == EXPECTED_NAMED_POSITIONS


def test_find_column_positions_gives_every_column_without_selector() -> None:
	"""
	Check that no selector gives every column.

	.. versionadded:: 0.1.0
	"""
	positions = find_column_positions(None, COLUMN_NAMES)

	position_list = read_positions(positions)
	assert position_list == EXPECTED_ALL_POSITIONS


def test_find_column_positions_accepts_a_position() -> None:
	"""
	Check that an Index gives its position.

	.. versionadded:: 0.1.0
	"""
	positions = find_column_positions(Index(-1), COLUMN_NAMES)

	position_list = read_positions(positions)
	assert position_list == [-1]


def test_find_column_positions_rejects_an_unknown_name() -> None:
	"""
	Check that an unknown name raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		find_column_positions(["prise"], COLUMN_NAMES)


def test_find_column_positions_rejects_a_repeated_name() -> None:
	"""
	Check that a repeated name raises DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateColumnError):
		find_column_positions(["price", "price"], COLUMN_NAMES)


def test_find_column_positions_takes_the_first_columns() -> None:
	"""
	Check that First chooses the columns from the start.

	.. versionadded:: 0.2.0
	"""
	positions = find_column_positions(First(1), COLUMN_NAMES)

	position_list = positions.tolist()
	assert position_list == EXPECTED_FIRST_POSITION


def test_find_column_positions_takes_the_last_columns() -> None:
	"""
	Check that Last chooses the columns of the end.

	.. versionadded:: 0.2.0
	"""
	positions = find_column_positions(Last(1), COLUMN_NAMES)

	position_list = positions.tolist()
	assert position_list == EXPECTED_SECOND_POSITION
