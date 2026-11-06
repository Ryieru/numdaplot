"""
Merging of the cells of a map too small to give each of them a pixel.

.. versionadded:: 0.1.0
"""

import numpy
from numpy.typing import NDArray

MINIMUM_BAND_PIXELS = 2


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

	band_numbers = numpy.arange(band_count)
	first_cells = band_numbers * cell_count // band_count
	merged_cells = numpy.maximum.reduceat(cells, first_cells, axis=axis)

	return merged_cells
