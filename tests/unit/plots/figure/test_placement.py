"""
Unit tests of the place of a Plot in the grid of a Figure.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp
from numdaplot.plots.figure.placement import (
	Placement,
	list_covered_cells,
	require_cell_inside,
	require_free_cells,
)

LAYOUT = ndp.Layout(rows=2, columns=2)
PLOT = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]), ndp.LineChart())
WIDE_TOP = Placement(PLOT, ndp.Cell(row=0, column=0, column_span=2))
OUTSIDE_CELLS = [
	ndp.Cell(row=2, column=0),
	ndp.Cell(row=0, column=-1),
	ndp.Cell(row=1, column=1, row_span=2),
	ndp.Cell(row=0, column=1, column_span=2),
]


def test_require_cell_inside_accepts_the_last_cell() -> None:
	"""
	Check that the bottom right cell is inside.

	.. versionadded:: 0.1.0
	"""
	require_cell_inside(ndp.Cell(row=1, column=1), LAYOUT)


@pytest.mark.parametrize("cell", OUTSIDE_CELLS)
def test_require_cell_inside_rejects_a_cell_outside(cell: ndp.Cell) -> None:
	"""
	Check that a cell, or a cell it spans, outside the grid raises CellOutOfRangeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cell
		A cell going beyond the grid.
	"""
	with pytest.raises(ndp.CellOutOfRangeError):
		require_cell_inside(cell, LAYOUT)


def test_require_free_cells_accepts_a_free_cell() -> None:
	"""
	Check that a cell below a wide Plot is free.

	.. versionadded:: 0.1.0
	"""
	require_free_cells(ndp.Cell(row=1, column=1), [WIDE_TOP])


def test_require_free_cells_rejects_a_cell_covered_by_a_span() -> None:
	"""
	Check that the second cell of a wide Plot is occupied, and named in the error.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.OccupiedCellError, match=r"Cell \(0, 1\)"):
		require_free_cells(ndp.Cell(row=0, column=1), [WIDE_TOP])


def test_require_free_cells_accepts_an_empty_figure() -> None:
	"""
	Check that any cell of an empty Figure is free.

	.. versionadded:: 0.1.0
	"""
	require_free_cells(ndp.Cell(row=0, column=0, row_span=2, column_span=2), [])


def test_list_covered_cells_goes_row_by_row() -> None:
	"""
	Check the cells of a Plot spanning two rows and two columns.

	.. versionadded:: 0.1.0
	"""
	covered_cells = list_covered_cells(ndp.Cell(row=0, column=0, row_span=2, column_span=2))

	assert covered_cells == [(0, 0), (0, 1), (1, 0), (1, 1)]
