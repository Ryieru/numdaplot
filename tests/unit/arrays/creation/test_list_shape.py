"""
Unit tests of find_list_shape and flatten_list.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.list_shape import find_list_shape, flatten_list
from numdaplot.errors.irregular_list_error import IrregularListError

FLAT_VALUES = list[object]([1, 2, 3])
GRID_VALUES = list[object]([[1, 2, 3], [4, 5, 6]])
CUBE_VALUES = list[object]([[[1], [2]], [[3], [4]]])
EMPTY_VALUES = list[object]()
RAGGED_VALUES = list[object]([[1, 2], [3]])
MIXED_LEVEL_VALUES = list[object]([[1, 2], 3])
FLAT_DIMENSIONS = (3,)
GRID_DIMENSIONS = (2, 3)
CUBE_DIMENSIONS = (2, 2, 1)
EMPTY_DIMENSIONS = (0,)
FLATTENED_GRID = [1, 2, 3, 4, 5, 6]


def test_find_list_shape_counts_a_flat_list() -> None:
	"""
	Check that a flat list has one dimension.

	.. versionadded:: 0.1.0
	"""
	dimensions = find_list_shape(FLAT_VALUES)

	assert dimensions == FLAT_DIMENSIONS


def test_find_list_shape_counts_rows_and_columns() -> None:
	"""
	Check that a list of rows gives rows then columns.

	.. versionadded:: 0.1.0
	"""
	dimensions = find_list_shape(GRID_VALUES)

	assert dimensions == GRID_DIMENSIONS


def test_find_list_shape_counts_any_depth() -> None:
	"""
	Check that three nesting levels give three dimensions.

	.. versionadded:: 0.1.0
	"""
	dimensions = find_list_shape(CUBE_VALUES)

	assert dimensions == CUBE_DIMENSIONS


def test_find_list_shape_gives_an_empty_dimension_for_an_empty_list() -> None:
	"""
	Check that an empty list has one dimension of size 0.

	.. versionadded:: 0.1.0
	"""
	dimensions = find_list_shape(EMPTY_VALUES)

	assert dimensions == EMPTY_DIMENSIONS


def test_find_list_shape_rejects_rows_of_different_lengths() -> None:
	"""
	Check that ragged rows raise IrregularListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IrregularListError):
		find_list_shape(RAGGED_VALUES)


def test_find_list_shape_rejects_lists_mixed_with_single_values() -> None:
	"""
	Check that a level mixing a list and a value raises IrregularListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IrregularListError):
		find_list_shape(MIXED_LEVEL_VALUES)


def test_flatten_list_reads_rows_in_order() -> None:
	"""
	Check that nested values come out row after row.

	.. versionadded:: 0.1.0
	"""
	single_values = flatten_list(GRID_VALUES)

	assert single_values == FLATTENED_GRID
