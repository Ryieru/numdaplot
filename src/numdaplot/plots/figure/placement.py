"""
A Plot placed in the grid of a Figure, and the checks of its place.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.cell_out_of_range_error import CellOutOfRangeError
from numdaplot.errors.occupied_cell_error import OccupiedCellError
from numdaplot.plots.figure.cell import Cell
from numdaplot.plots.figure.layout import Layout
from numdaplot.plots.plot import Plot


@dataclass(frozen=True, eq=False)
class Placement:
	"""
	A Plot and the cells it covers in a Figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	plot
		The Plot placed.
	cell
		Its first cell and the number of cells it spans.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.figure.placement import Placement
	>>> plot = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]))
	>>> Placement(plot, ndp.Cell(row=0, column=1)).cell.column
	1
	"""

	plot: Plot
	cell: Cell


def require_cell_inside(cell: Cell, layout: Layout) -> None:
	"""
	Check that every cell a Plot covers is inside the grid of a Figure.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cell
		The first cell and the spans of the Plot.
	layout
		The grid of the Figure.

	Raises
	------
	CellOutOfRangeError
		When the first cell is before row or column 0, or a cell it spans is after the last row or column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.figure.placement import require_cell_inside
	>>> try:
	... 	require_cell_inside(ndp.Cell(row=1, column=0, column_span=3), ndp.Layout(rows=2, columns=2))
	... except ndp.CellOutOfRangeError as error:
	... 	print(error)
	Cell (1, 0) is outside a Layout of 2 rows and 2 columns.
	"""
	row_end = cell.row + cell.row_span
	column_end = cell.column + cell.column_span
	starts_before = cell.row < 0 or cell.column < 0
	ends_after = row_end > layout.rows or column_end > layout.columns
	is_outside = starts_before or ends_after
	if is_outside:
		raise CellOutOfRangeError(cell.row, cell.column, layout.rows, layout.columns)


def require_free_cells(cell: Cell, placements: list[Placement]) -> None:
	"""
	Check that no cell a Plot covers already holds another Plot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cell
		The first cell and the spans of the Plot placed.
	placements
		The Plots already in the Figure.

	Raises
	------
	OccupiedCellError
		At the first cell, row by row, already covered by another Plot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.figure.placement import Placement, require_free_cells
	>>> plot = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]))
	>>> wide_placement = Placement(plot, ndp.Cell(row=0, column=0, column_span=2))
	>>> try:
	... 	require_free_cells(ndp.Cell(row=0, column=1), [wide_placement])
	... except ndp.OccupiedCellError as error:
	... 	print(error)
	Cell (0, 1) already holds a Plot.
	"""
	covered_cells = set[tuple[int, int]]()

	for placement in placements:
		placement_cells = list_covered_cells(placement.cell)
		covered_cells.update(placement_cells)

	new_cells = list_covered_cells(cell)

	for row, column in new_cells:
		if (row, column) in covered_cells:
			raise OccupiedCellError(row, column)


def list_covered_cells(cell: Cell) -> list[tuple[int, int]]:
	"""
	Return the row and the column of every cell a Plot covers, row by row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	cell
		The first cell and the spans of the Plot.

	Returns
	-------
	list[tuple[int, int]]
		The covered cells.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.figure.placement import list_covered_cells
	>>> list_covered_cells(ndp.Cell(row=1, column=0, column_span=2))
	[(1, 0), (1, 1)]
	"""
	row_end = cell.row + cell.row_span
	column_end = cell.column + cell.column_span
	rows = range(cell.row, row_end)
	columns = range(cell.column, column_end)
	covered_cells = [(row, column) for row in rows for column in columns]

	return covered_cells
