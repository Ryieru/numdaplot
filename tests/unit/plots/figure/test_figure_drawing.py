"""
Unit tests of the drawing of a Figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from matplotlib.figure import Figure

import numdaplot as ndp
from numdaplot.plots.figure.figure_drawing import choose_figure_size, draw_figure
from numdaplot.plots.figure.placement import Placement

PLOT = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]), ndp.LineChart(), ndp.PlotStyle(title="Prices"))
LAYOUT = ndp.Layout(rows=2, columns=3)


def test_draw_figure_draws_each_plot_on_its_cells() -> None:
	"""
	Check one subfigure per Plot, holding the drawing of the Plot.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()
	placements = [Placement(PLOT, ndp.Cell(row=0, column=0)), Placement(PLOT, ndp.Cell(row=1, column=1))]

	draw_figure(figure, LAYOUT, placements, None)

	subfigure_count = len(figure.subfigs)
	first_title = figure.subfigs[0].axes[0].get_title()
	assert subfigure_count == 2
	assert first_title == "Prices"


def test_draw_figure_writes_the_title() -> None:
	"""
	Check that the title is drawn above the grid.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()

	draw_figure(figure, LAYOUT, [], "Shop")

	assert figure.get_suptitle() == "Shop"


def test_draw_figure_leaves_an_empty_figure_blank() -> None:
	"""
	Check that a Figure without Plot draws no axes and no title.

	.. versionadded:: 0.1.0
	"""
	figure = Figure()

	draw_figure(figure, LAYOUT, [], None)

	assert figure.axes == []
	assert figure.get_suptitle() == ""


def test_choose_figure_size_gives_each_cell_its_size() -> None:
	"""
	Check 4.8 by 3.6 inches per cell without chosen size.

	.. versionadded:: 0.1.0
	"""
	width, height = choose_figure_size(ndp.Layout(rows=2, columns=1), None)

	assert width == 4.8
	assert height == 7.2


def test_choose_figure_size_keeps_the_chosen_size() -> None:
	"""
	Check that a chosen size is used in inches.

	.. versionadded:: 0.1.0
	"""
	size_inches = choose_figure_size(LAYOUT, ndp.Size(width=10.0, height=5.0))

	assert size_inches == (10.0, 5.0)
