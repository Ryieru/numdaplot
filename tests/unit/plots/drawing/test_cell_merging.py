"""
Unit tests of the merging of the cells of a map.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.plots.drawing.cell_merging import find_band_count, merge_cells

ROW_AXIS = 0
COLUMN_AXIS = 1
AXIS_PIXELS = 369.6
EXPECTED_BAND_COUNT = 184
TINY_AXIS_PIXELS = 1.0
LOOSE_BAND_COUNT = 10
BAND_COUNT = 2
TALL_CELLS = numpy.array([[0.0], [1.0], [0.0], [0.0]])
WIDE_CELLS = numpy.array([[0.0, 0.0, 0.0, 1.0]])
EXPECTED_MERGED_ROWS = [[1.0], [0.0]]
EXPECTED_MERGED_COLUMNS = [[0.0, 1.0]]


def test_find_band_count_gives_each_band_two_pixels() -> None:
	"""
	Check the number of bands of an axis.

	.. versionadded:: 0.1.0
	"""
	band_count = find_band_count(AXIS_PIXELS)

	assert band_count == EXPECTED_BAND_COUNT


def test_find_band_count_keeps_one_band_on_a_tiny_axis() -> None:
	"""
	Check that an axis of a pixel still shows one band.

	.. versionadded:: 0.1.0
	"""
	band_count = find_band_count(TINY_AXIS_PIXELS)

	assert band_count == 1


def test_merge_cells_keeps_the_marked_cells_of_merged_rows() -> None:
	"""
	Check that a band of rows keeps the highest value of its cells.

	.. versionadded:: 0.1.0
	"""
	merged_cells = merge_cells(TALL_CELLS, BAND_COUNT, ROW_AXIS)

	assert merged_cells.tolist() == EXPECTED_MERGED_ROWS


def test_merge_cells_merges_columns() -> None:
	"""
	Check that a band of columns keeps the highest value of its cells.

	.. versionadded:: 0.1.0
	"""
	merged_cells = merge_cells(WIDE_CELLS, BAND_COUNT, COLUMN_AXIS)

	assert merged_cells.tolist() == EXPECTED_MERGED_COLUMNS


def test_merge_cells_gives_the_same_cells_when_they_fit() -> None:
	"""
	Check that cells fitting in the bands are left as they are.

	.. versionadded:: 0.1.0
	"""
	merged_cells = merge_cells(TALL_CELLS, LOOSE_BAND_COUNT, ROW_AXIS)

	assert merged_cells is TALL_CELLS
