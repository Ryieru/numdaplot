"""
Unit tests of Figure.

.. versionadded:: 0.1.0
"""

# The matplotlib stubs leave the keyword arguments of most drawing methods untyped.
# pyright: reportUnknownMemberType=false

from pathlib import Path

import pytest

import numdaplot as ndp
from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure
from numdaplot.plots.figure import figure as figure_module

PLOT = ndp.Plot.line(ndp.Array.from_list([12.0, 15.5]), ndp.LineChart(), ndp.PlotStyle(title="Prices"))
LAYOUT = ndp.Layout(rows=1, columns=2)
LEFT = ndp.Cell(row=0, column=0)
RIGHT = ndp.Cell(row=0, column=1)
SHOW_FUNCTION_NAME = "show_drawing"
EXPECTED_INCHES = [9.6, 3.6]
CHOSEN_SIZE = ndp.Size(width=8, height=3)
EXPECTED_CHOSEN_INCHES = [8.0, 3.0]
OLD_CONTENT = "old"


def test_place_returns_a_new_figure_and_leaves_this_one_unchanged() -> None:
	"""
	Check that placing a Plot gives a new Figure and keeps the first one empty.

	.. versionadded:: 0.1.0
	"""
	figure = ndp.Figure(LAYOUT)

	placed_figure = figure.place(PLOT, LEFT)

	empty_count = len(figure.to_matplotlib().subfigs)
	placed_count = len(placed_figure.to_matplotlib().subfigs)
	assert placed_figure is not figure
	assert empty_count == 0
	assert placed_count == 1


def test_place_rejects_an_occupied_cell() -> None:
	"""
	Check that a cell already holding a Plot raises OccupiedCellError.

	.. versionadded:: 0.1.0
	"""
	figure = ndp.Figure(LAYOUT).place(PLOT, LEFT)

	with pytest.raises(ndp.OccupiedCellError):
		figure.place(PLOT, LEFT)


def test_place_rejects_a_cell_outside_the_layout() -> None:
	"""
	Check that a cell outside the grid raises CellOutOfRangeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.CellOutOfRangeError):
		ndp.Figure(LAYOUT).place(PLOT, ndp.Cell(row=1, column=0))


def test_to_matplotlib_has_the_size_of_its_cells_and_the_title() -> None:
	"""
	Check the default size and the title of the figure.

	.. versionadded:: 0.1.0
	"""
	figure = ndp.Figure(LAYOUT, ndp.FigureStyle(title="Shop")).place(PLOT, RIGHT)

	matplotlib_figure = figure.to_matplotlib()

	inches = matplotlib_figure.get_size_inches().tolist()
	assert inches == EXPECTED_INCHES
	assert matplotlib_figure.get_suptitle() == "Shop"


def test_to_matplotlib_takes_the_size_of_its_style() -> None:
	"""
	Check that the size of the FigureStyle replaces the size of the cells, and stays after a placement.

	.. versionadded:: 0.1.0
	"""
	style = ndp.FigureStyle(size=CHOSEN_SIZE)
	empty_figure = ndp.Figure(LAYOUT, style)
	figure = empty_figure.place(PLOT, LEFT)

	matplotlib_figure = figure.to_matplotlib()

	inches = matplotlib_figure.get_size_inches().tolist()
	assert inches == EXPECTED_CHOSEN_INCHES


def test_save_writes_the_figure_as_an_image(tmp_path: Path) -> None:
	"""
	Check that a Figure is written as an SVG file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / "shop.svg"
	figure = ndp.Figure(LAYOUT).place(PLOT, LEFT)

	figure.save(image_path)

	assert image_path.read_text().startswith("<?xml")


def test_save_refuses_to_overwrite_a_file_by_default(tmp_path: Path) -> None:
	"""
	Check that an existing file raises FileExistsError and keeps its content.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	image_path = tmp_path / "shop.png"
	image_path.write_text(OLD_CONTENT)

	with pytest.raises(ndp.FileExistsError):
		ndp.Figure(LAYOUT).save(image_path)

	assert image_path.read_text() == OLD_CONTENT


def test_show_hands_the_drawing_of_the_figure_to_the_display(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that show displays what the Figure draws, at its size.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the display with a fake.
	"""
	shown_drawings = list[FigureDrawing]()
	monkeypatch.setattr(figure_module, SHOW_FUNCTION_NAME, shown_drawings.append)
	figure = ndp.Figure(LAYOUT).place(PLOT, LEFT)

	figure.show()

	shown_figure = build_figure(shown_drawings[0])
	subfigure_count = len(shown_figure.subfigs)
	assert subfigure_count == 1
