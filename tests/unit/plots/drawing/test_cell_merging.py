"""
Unit tests of the merging of the cells of a map.

.. versionadded:: 0.1.0
"""

import numpy
from matplotlib.figure import Figure

from numdaplot.plots.drawing.cell_merging import (
	average_cells,
	find_band_count,
	find_cell_limits,
	find_first_cells,
	fit_cells_to_axes,
	merge_cells,
)

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
NUMBERED_CELLS = numpy.array([[1.0], [3.0], [numpy.nan], [numpy.nan]])
EXPECTED_MEAN_OF_FIRST_BAND = 2.0
CELL_COUNT = 10
FOUR_BANDS = 4
EXPECTED_FIRST_CELLS = [0, 2, 5, 7]
TALL_ROW_COUNT = 6000
MARKED_ROW = 4321
FITTING_ROW_COUNT = 250
WIDE_COLUMN_COUNT = 2000
EXPECTED_LIMITS = (-0.5, 1.5, 2.5, -0.5)


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


def test_average_cells_gives_the_mean_of_the_present_values() -> None:
	"""
	Check that a band shows the mean of its cells.

	.. versionadded:: 0.1.0
	"""
	averaged_cells = average_cells(NUMBERED_CELLS, BAND_COUNT, ROW_AXIS)

	assert averaged_cells[0, 0] == EXPECTED_MEAN_OF_FIRST_BAND


def test_average_cells_keeps_a_band_without_value_missing() -> None:
	"""
	Check that a band holding only missing values stays missing.

	.. versionadded:: 0.1.0
	"""
	averaged_cells = average_cells(NUMBERED_CELLS, BAND_COUNT, ROW_AXIS)

	assert numpy.isnan(averaged_cells[1, 0])


def test_average_cells_gives_the_same_cells_when_they_fit() -> None:
	"""
	Check that cells fitting in the bands are left as they are.

	.. versionadded:: 0.1.0
	"""
	averaged_cells = average_cells(NUMBERED_CELLS, LOOSE_BAND_COUNT, ROW_AXIS)

	assert averaged_cells is NUMBERED_CELLS


def test_find_first_cells_shares_the_cells_evenly() -> None:
	"""
	Check the first cell of each band.

	.. versionadded:: 0.1.0
	"""
	first_cells = find_first_cells(CELL_COUNT, FOUR_BANDS)

	assert first_cells.tolist() == EXPECTED_FIRST_CELLS


def test_fit_cells_to_axes_keeps_a_lone_marked_cell_of_a_tall_map() -> None:
	"""
	Check that merging the rows keeps a band marked for the only marked cell.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	grid = numpy.zeros((TALL_ROW_COUNT, BAND_COUNT))
	grid[MARKED_ROW, 1] = 1.0

	shown_cells = fit_cells_to_axes(grid, axes, merge_cells)

	assert shown_cells.shape[0] < TALL_ROW_COUNT
	assert shown_cells.sum() == 1.0


def test_fit_cells_to_axes_keeps_cells_that_fit() -> None:
	"""
	Check that a grid with enough pixels is not merged.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	grid = numpy.zeros((FITTING_ROW_COUNT, BAND_COUNT))

	shown_cells = fit_cells_to_axes(grid, axes, average_cells)

	assert shown_cells is grid


def test_fit_cells_to_axes_merges_too_many_columns() -> None:
	"""
	Check that columns are merged like rows.

	.. versionadded:: 0.1.0
	"""
	axes = Figure().add_subplot()
	grid = numpy.zeros((BAND_COUNT, WIDE_COLUMN_COUNT))

	shown_cells = fit_cells_to_axes(grid, axes, average_cells)

	assert shown_cells.shape[1] < WIDE_COLUMN_COUNT


def test_find_cell_limits_places_the_first_row_on_top() -> None:
	"""
	Check the limits of an image of 3 rows and 2 columns.

	.. versionadded:: 0.1.0
	"""
	cell_limits = find_cell_limits(numpy.zeros((3, BAND_COUNT)))

	assert cell_limits == EXPECTED_LIMITS
