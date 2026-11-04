"""
Functional tests of the Figures placing several Plots on a grid.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

import struct
from pathlib import Path

import pytest

import numdaplot as ndp

PRICES = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
LINE_PLOT = ndp.plot_line(PRICES, ndp.LineChart(), ndp.Style(title="Line"))
BAR_PLOT = ndp.plot_bar(PRICES, ndp.BarChart(), ndp.Style(title="Bars"))
BOX_PLOT = ndp.plot_box(PRICES, ndp.BoxChart(), ndp.Style(title="Box"))
LAYOUT = ndp.Layout(rows=2, columns=2)
PNG_SIZE_START = 16
PNG_SIZE_END = 24
PNG_SIZE_LAYOUT = ">II"
EXPECTED_PIXELS = (960, 720)


def build_figure() -> ndp.Figure:
	"""
	Return a Figure with a wide line Plot on top, and bars and a box below.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Figure
		The Figure of three Plots.
	"""
	figure = ndp.Figure(LAYOUT, title="Prices")
	figure = figure.place(LINE_PLOT, ndp.Cell(row=0, column=0, column_span=2))
	figure = figure.place(BAR_PLOT, ndp.Cell(row=1, column=0))
	figure = figure.place(BOX_PLOT, ndp.Cell(row=1, column=1))

	return figure


def test_a_figure_draws_each_plot_with_its_style_in_its_cells() -> None:
	"""
	Check one subfigure per Plot with its own title, and the title of the Figure.

	.. versionadded:: 0.1.0
	"""
	figure = build_figure()

	matplotlib_figure = figure.to_matplotlib()

	plot_titles = [subfigure.axes[0].get_title() for subfigure in matplotlib_figure.subfigs]
	assert plot_titles == ["Line", "Bars", "Box"]
	assert matplotlib_figure.get_suptitle() == "Prices"


def test_a_wide_plot_spans_the_cells_it_covers() -> None:
	"""
	Check that the wide Plot covers the whole width, and a Plot below it at most half.

	.. versionadded:: 0.1.0
	"""
	matplotlib_figure = build_figure().to_matplotlib()
	matplotlib_figure.draw_without_rendering()

	top, bottom_left, _ = matplotlib_figure.subfigs
	top_width = top.bbox.width
	figure_width = matplotlib_figure.bbox.width
	half_width = figure_width / 2
	assert top_width == pytest.approx(figure_width)
	assert bottom_left.bbox.width <= half_width


def test_a_figure_is_saved_at_the_size_of_its_cells(tmp_path: Path) -> None:
	"""
	Check that a 2 by 2 Figure is saved at 4.8 by 3.6 inches per cell, at 100 dots per inch.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / "prices.png"

	build_figure().save(image_path)

	image_bytes = image_path.read_bytes()
	size_bytes = image_bytes[PNG_SIZE_START:PNG_SIZE_END]
	pixel_size = struct.unpack(PNG_SIZE_LAYOUT, size_bytes)
	assert pixel_size == EXPECTED_PIXELS


def test_a_figure_refuses_a_plot_on_an_occupied_cell() -> None:
	"""
	Check that a cell covered by the wide Plot raises OccupiedCellError.

	.. versionadded:: 0.1.0
	"""
	figure = build_figure()

	with pytest.raises(ndp.NumdaplotError, match=r"Cell \(0, 1\)"):
		figure.place(BAR_PLOT, ndp.Cell(row=0, column=1))
