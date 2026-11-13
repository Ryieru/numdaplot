"""
Drawing of a Figure: its title and the Plots in their cells.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from matplotlib.figure import FigureBase

from numdaplot.plots.drawing.plot_theme import BACKGROUND_COLOR
from numdaplot.plots.drawing.size_inches import convert_size_to_inches
from numdaplot.plots.figure.layout import Layout
from numdaplot.plots.figure.placement import Placement
from numdaplot.plots.style.size import Size

CELL_WIDTH = 4.8
CELL_HEIGHT = 3.6


def draw_figure(target: FigureBase, layout: Layout, placements: list[Placement], title: str | None) -> None:
	"""
	Draw the title of a Figure and each of its Plots on the cells it covers, the empty cells staying blank.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target
		An empty matplotlib figure.
	layout
		The grid of the Figure.
	placements
		The Plots and their cells.
	title
		The title above the grid, or None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from matplotlib.figure import Figure
	>>> from numdaplot.plots.figure.figure_drawing import draw_figure
	>>> from numdaplot.plots.figure.placement import Placement
	>>> plot = ndp.Plot.line(ndp.Array.from_list([12.0, 15.5]))
	>>> figure = Figure()
	>>> draw_figure(figure, ndp.Layout(rows=1, columns=2), [Placement(plot, ndp.Cell(row=0, column=1))], "Sales")
	>>> len(figure.subfigs), figure.get_suptitle()
	(1, 'Sales')
	"""
	target.set_facecolor(BACKGROUND_COLOR)
	if title is not None:
		target.suptitle(title)

	cell_grid = target.add_gridspec(layout.rows, layout.columns)

	for placement in placements:
		cell = placement.cell
		row_end = cell.row + cell.row_span
		column_end = cell.column + cell.column_span
		cell_area = cell_grid[cell.row : row_end, cell.column : column_end]
		subfigure = target.add_subfigure(cell_area)
		# A Plot of a Figure is drawn by its own private drawing.
		placement.plot._draw_on(subfigure)  # pyright: ignore[reportPrivateUsage]


def choose_figure_size(layout: Layout, size: Size | None) -> tuple[float, float]:
	"""
	Return the width and the height of a Figure in inches.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layout
		The grid of the Figure.
	size
		The size chosen, or None for 4.8 by 3.6 inches per cell.

	Returns
	-------
	tuple[float, float]
		The width and the height.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.figure.figure_drawing import choose_figure_size
	>>> choose_figure_size(ndp.Layout(rows=2, columns=3), None)
	(14.399999999999999, 7.2)
	"""
	if size is not None:
		chosen_size = convert_size_to_inches(size)
		return chosen_size

	width = CELL_WIDTH * layout.columns
	height = CELL_HEIGHT * layout.rows

	return width, height
