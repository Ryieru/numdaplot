"""
Unit tests of build_region_index, find_positions and require_valid_positions.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.selection.region_index import build_region_index, find_positions, require_valid_positions
from numdaplot.errors.positions.dimension_error import DimensionError
from numdaplot.errors.positions.invalid_position_error import InvalidPositionError
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError
from numdaplot.positions.first import First
from numdaplot.positions.index import Index
from numdaplot.positions.last import Last
from numdaplot.positions.range import Range
from numdaplot.positions.region import Region

SIZE = 5
LAST_POSITION = -1
EVERY_POSITION = [0, 1, 2, 3, 4]
EVEN_POSITIONS = Range(start=0, stop=4, step=2)
EXPECTED_EVEN_POSITIONS = [0, 2, 4]
LINE_DIMENSIONS = (3,)
GRID_DIMENSIONS = (2, 3)
CUBE_DIMENSIONS = (2, 2, 2)
LAST_ROW = Region(rows=Index(LAST_POSITION))
EXPECTED_LINE_INDEX = [[-1]]
GRID_REGION = Region(rows=Index(0), columns=Range(start=1, stop=2))
EXPECTED_GRID_ROWS = [[0]]
EXPECTED_GRID_COLUMNS = [[1, 2]]
COLUMN_REGION = Region(columns=Index(0))
NAMED_REGION = Region(columns=["total"])
WHOLE_POSITIONS = [0, -5, 4]
OUTSIDE_POSITIONS = [0, 5]
DECIMAL_POSITIONS = [0.5]
FIRST_COUNT = 2
EXPECTED_FIRST_POSITIONS = [0, 1]
EXPECTED_LAST_POSITIONS = [3, 4]
LARGE_COUNT = 9


def test_find_positions_takes_every_position_without_selector() -> None:
	"""
	Check that no selector means every position.

	.. versionadded:: 0.1.0
	"""
	positions = find_positions(None, SIZE)

	position_list = positions.tolist()
	assert position_list == EVERY_POSITION


def test_find_positions_keeps_a_single_index_as_a_list() -> None:
	"""
	Check that an Index gives a one-position array, so its dimension is kept.

	.. versionadded:: 0.1.0
	"""
	positions = find_positions(Index(LAST_POSITION), SIZE)

	position_list = positions.tolist()
	assert position_list == [LAST_POSITION]


def test_find_positions_reads_a_range_with_its_stop() -> None:
	"""
	Check that a Range gives its positions, stop included.

	.. versionadded:: 0.1.0
	"""
	positions = find_positions(EVEN_POSITIONS, SIZE)

	position_list = positions.tolist()
	assert position_list == EXPECTED_EVEN_POSITIONS


def test_find_positions_takes_the_first_positions() -> None:
	"""
	Check that First gives the positions from the start.

	.. versionadded:: 0.2.0
	"""
	positions = find_positions(First(FIRST_COUNT), SIZE)

	position_list = positions.tolist()
	assert position_list == EXPECTED_FIRST_POSITIONS


def test_find_positions_takes_the_last_positions() -> None:
	"""
	Check that Last gives the positions of the end, in order.

	.. versionadded:: 0.2.0
	"""
	positions = find_positions(Last(FIRST_COUNT), SIZE)

	position_list = positions.tolist()
	assert position_list == EXPECTED_LAST_POSITIONS


def test_find_positions_takes_every_position_of_a_shorter_dimension() -> None:
	"""
	Check that First and Last larger than the dimension give every position, without error.

	.. versionadded:: 0.2.0
	"""
	first_positions = find_positions(First(LARGE_COUNT), SIZE)
	last_positions = find_positions(Last(LARGE_COUNT), SIZE)

	first_list = first_positions.tolist()
	last_list = last_positions.tolist()
	assert first_list == EVERY_POSITION
	assert last_list == EVERY_POSITION


def test_require_valid_positions_accepts_positions_inside_the_dimension() -> None:
	"""
	Check that positions from -size to size - 1 are accepted.

	.. versionadded:: 0.1.0
	"""
	positions = numpy.array(WHOLE_POSITIONS)

	require_valid_positions(positions, SIZE)


def test_require_valid_positions_accepts_no_position() -> None:
	"""
	Check that an empty selection of positions is accepted.

	.. versionadded:: 0.1.0
	"""
	positions = numpy.array([], dtype=int)

	require_valid_positions(positions, SIZE)


def test_require_valid_positions_rejects_a_position_outside_the_dimension() -> None:
	"""
	Check that the position equal to the size is rejected.

	.. versionadded:: 0.1.0
	"""
	positions = numpy.array(OUTSIDE_POSITIONS)

	with pytest.raises(InvalidPositionError):
		require_valid_positions(positions, SIZE)


def test_require_valid_positions_rejects_a_decimal_position() -> None:
	"""
	Check that a position that is not a whole number is rejected.

	.. versionadded:: 0.1.0
	"""
	positions = numpy.array(DECIMAL_POSITIONS)

	with pytest.raises(InvalidPositionError):
		require_valid_positions(positions, SIZE)


def test_build_region_index_selects_rows_of_a_line() -> None:
	"""
	Check that a one-dimensional Array only uses the rows.

	.. versionadded:: 0.1.0
	"""
	region_index = build_region_index(LAST_ROW, LINE_DIMENSIONS)

	index_lists = [positions.tolist() for positions in region_index]
	assert index_lists == EXPECTED_LINE_INDEX


def test_build_region_index_crosses_rows_and_columns_of_a_grid() -> None:
	"""
	Check that a two-dimensional Array crosses the rows with the columns.

	.. versionadded:: 0.1.0
	"""
	row_index, column_index = build_region_index(GRID_REGION, GRID_DIMENSIONS)

	row_lists = row_index.tolist()
	column_lists = column_index.tolist()
	assert row_lists == EXPECTED_GRID_ROWS
	assert column_lists == EXPECTED_GRID_COLUMNS


def test_build_region_index_rejects_columns_on_a_line() -> None:
	"""
	Check that columns given for a one-dimensional Array raise DimensionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DimensionError):
		build_region_index(COLUMN_REGION, LINE_DIMENSIONS)


def test_build_region_index_rejects_three_dimensions() -> None:
	"""
	Check that a three-dimensional Array raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DimensionError):
		build_region_index(LAST_ROW, CUBE_DIMENSIONS)


def test_build_region_index_refuses_column_names() -> None:
	"""
	Check that column names, which only a Table has, are refused.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		build_region_index(NAMED_REGION, GRID_DIMENSIONS)
