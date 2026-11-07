"""
Merging of the cells of a map too small to give each of them a pixel.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable

import numpy
from matplotlib.axes import Axes
from numpy.typing import NDArray

type CellMerger = Callable[[NDArray[numpy.float64], int, int], NDArray[numpy.float64]]
"""A function merging cells along an axis into at most a number of bands.

.. versionadded:: 0.1.0
"""

MINIMUM_BAND_PIXELS = 2
# Below this share of the pixels before the layout, each cell keeps at least one pixel afterwards.
FITTING_SHARE = 0.75
ROW_AXIS = 0
COLUMN_AXIS = 1
HALF_CELL = 0.5


def find_band_count(length_pixels: float) -> int:
	"""
	Return how many bands of cells an axis can show, each one staying visible once the layout narrows the axes.

	The layout keeps more than half of the length of the axes, so a band of 2 pixels keeps at least 1 pixel.

	.. versionadded:: 0.1.0

	Parameters
	----------
	length_pixels
		The length of the axis before the layout, in pixels.

	Returns
	-------
	int
		The number of bands, at least 1.

	Examples
	--------
	>>> from numdaplot.plots.drawing.cell_merging import find_band_count
	>>> find_band_count(369.6)
	184
	"""
	band_count = int(length_pixels // MINIMUM_BAND_PIXELS)
	shown_band_count = max(band_count, 1)

	return shown_band_count


def merge_cells(cells: NDArray[numpy.float64], band_count: int, axis: int) -> NDArray[numpy.float64]:
	"""
	Return the cells merged along an axis into bands, each one keeping the highest value of its cells.

	Matplotlib only keeps one cell per pixel when it shrinks an image, which would lose most of the marked cells.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cells
		The cells, in two dimensions.
	band_count
		The most bands kept.
	axis
		The axis merged, 0 for the rows and 1 for the columns.

	Returns
	-------
	NDArray[numpy.float64]
		The merged cells, or the same cells when they fit in the bands.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.cell_merging import merge_cells
	>>> merge_cells(numpy.array([[0.0], [1.0], [0.0], [0.0]]), 2, 0).tolist()
	[[1.0], [0.0]]
	"""
	cell_count = cells.shape[axis]
	if cell_count <= band_count:
		return cells

	first_cells = find_first_cells(cell_count, band_count)
	merged_cells = numpy.maximum.reduceat(cells, first_cells, axis=axis)

	return merged_cells


def average_cells(cells: NDArray[numpy.float64], band_count: int, axis: int) -> NDArray[numpy.float64]:
	"""
	Return the cells merged along an axis into bands, each one showing the mean of the present values of its cells.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cells
		The cells, in two dimensions, NaN for a missing value.
	band_count
		The most bands kept.
	axis
		The axis merged, 0 for the rows and 1 for the columns.

	Returns
	-------
	NDArray[numpy.float64]
		The merged cells, NaN for a band without value, or the same cells when they fit in the bands.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.cell_merging import average_cells
	>>> average_cells(numpy.array([[1.0], [3.0], [numpy.nan], [numpy.nan]]), 2, 0).tolist()[0]
	[2.0]
	"""
	cell_count = cells.shape[axis]
	if cell_count <= band_count:
		return cells

	first_cells = find_first_cells(cell_count, band_count)
	is_present = ~numpy.isnan(cells)
	present_numbers = numpy.nan_to_num(cells)
	totals = numpy.add.reduceat(present_numbers, first_cells, axis=axis)
	present_counts = numpy.add.reduceat(is_present.astype(numpy.float64), first_cells, axis=axis)
	empty_bands = present_counts == 0
	divisors = numpy.where(empty_bands, numpy.nan, present_counts)
	averaged_cells = totals / divisors

	return averaged_cells


def find_first_cells(cell_count: int, band_count: int) -> NDArray[numpy.intp]:
	"""
	Return the position of the first cell of each band, the bands sharing the cells evenly.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cell_count
		The number of cells, above the number of bands.
	band_count
		The number of bands.

	Returns
	-------
	NDArray[numpy.intp]
		One position per band.

	Examples
	--------
	>>> from numdaplot.plots.drawing.cell_merging import find_first_cells
	>>> find_first_cells(10, 4).tolist()
	[0, 2, 5, 7]
	"""
	band_numbers = numpy.arange(band_count, dtype=numpy.intp)
	first_cells = band_numbers * cell_count // band_count

	return first_cells


def fit_cells_to_axes(grid: NDArray[numpy.float64], axes: Axes, merge: CellMerger) -> NDArray[numpy.float64]:
	"""
	Return the cells of a map merged along each direction where the axes have too few pixels for them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	grid
		The cells of the map.
	axes
		The matplotlib axes drawn on.
	merge
		What a band keeps of its cells: ``merge_cells`` or ``average_cells``.

	Returns
	-------
	NDArray[numpy.float64]
		The cells to draw, the same ones when they fit.

	Examples
	--------
	>>> import numpy
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.drawing.cell_merging import fit_cells_to_axes, merge_cells
	>>> axes = Figure().add_subplot()
	>>> fit_cells_to_axes(numpy.zeros((1000, 2)), axes, merge_cells).shape
	(184, 2)
	"""
	row_count, column_count = grid.shape
	shown_cells = grid
	if row_count > axes.bbox.height * FITTING_SHARE:
		row_band_count = find_band_count(axes.bbox.height)
		shown_cells = merge(shown_cells, row_band_count, ROW_AXIS)

	if column_count > axes.bbox.width * FITTING_SHARE:
		column_band_count = find_band_count(axes.bbox.width)
		shown_cells = merge(shown_cells, column_band_count, COLUMN_AXIS)

	return shown_cells


def find_cell_limits(grid: NDArray[numpy.float64]) -> tuple[float, float, float, float]:
	"""
	Return where an image of a map goes, so that each row and column keeps its own number once merged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	grid
		The cells of the map before they are merged.

	Returns
	-------
	tuple[float, float, float, float]
		The left, right, bottom and top limits, the first row being on top.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.drawing.cell_merging import find_cell_limits
	>>> find_cell_limits(numpy.zeros((3, 2)))
	(-0.5, 1.5, 2.5, -0.5)
	"""
	row_count, column_count = grid.shape
	cell_limits = (-HALF_CELL, column_count - HALF_CELL, row_count - HALF_CELL, -HALF_CELL)

	return cell_limits
