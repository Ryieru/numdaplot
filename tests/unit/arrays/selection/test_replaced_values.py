"""
Unit tests of replace_region and require_storable.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.selection.replaced_values import replace_region, require_storable
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.types.value_conversion_error import ValueConversionError
from numdaplot.positions.index import Index
from numdaplot.positions.region import Region

GRID = [[1, 2], [3, 4]]
FIRST_ROW = Region(rows=Index(0))
NEW_VALUE = 0
EXPECTED_ROW_REPLACED_GRID = [[0, 0], [3, 4]]
NEW_ROW = [[9, 8]]
EXPECTED_NEW_ROW_GRID = [[9, 8], [3, 4]]
FLAT_NEW_ROW = [9, 8]
DECIMAL_VALUE = 1.5
INT8_DTYPE = "int8"
TOO_LARGE_INT8 = 300
DECIMALS = [1.5]


def test_replace_region_writes_a_single_value_everywhere_in_the_region() -> None:
	"""
	Check that a single value replaces a whole row.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID)

	replaced_values = replace_region(grid, FIRST_ROW, NEW_VALUE)

	replaced_rows = replaced_values.tolist()
	assert replaced_rows == EXPECTED_ROW_REPLACED_GRID


def test_replace_region_writes_values_of_the_region_shape() -> None:
	"""
	Check that values of the shape of the region replace it position by position.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID)
	new_row = numpy.array(NEW_ROW)

	replaced_values = replace_region(grid, FIRST_ROW, new_row)

	replaced_rows = replaced_values.tolist()
	assert replaced_rows == EXPECTED_NEW_ROW_GRID


def test_replace_region_leaves_the_original_values_unchanged() -> None:
	"""
	Check that the replacement works on a copy.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID)

	replace_region(grid, FIRST_ROW, NEW_VALUE)

	grid_rows = grid.tolist()
	assert grid_rows == GRID


def test_replace_region_rejects_values_of_another_shape() -> None:
	"""
	Check that a flat row cannot replace a two-dimensional row.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID)
	flat_row = numpy.array(FLAT_NEW_ROW)

	with pytest.raises(ShapeMismatchError):
		replace_region(grid, FIRST_ROW, flat_row)


def test_replace_region_rejects_a_value_out_of_range() -> None:
	"""
	Check that 300 cannot be written in INT8 values.

	.. versionadded:: 0.1.0
	"""
	small_integers = numpy.array(GRID, dtype=INT8_DTYPE)

	with pytest.raises(ValueConversionError):
		replace_region(small_integers, FIRST_ROW, TOO_LARGE_INT8)


def test_require_storable_accepts_an_integer_in_decimals() -> None:
	"""
	Check that an integer can be stored among decimals.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	require_storable(NEW_VALUE, decimals)


def test_require_storable_rejects_a_decimal_in_integers() -> None:
	"""
	Check that a decimal cannot be stored among integers.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID)

	with pytest.raises(ValueConversionError):
		require_storable(DECIMAL_VALUE, grid)
