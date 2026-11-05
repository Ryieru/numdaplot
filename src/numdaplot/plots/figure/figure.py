"""
Several Plots placed on a grid of cells.

.. versionadded:: 0.1.0
"""

from typing import Self

from matplotlib.figure import Figure as MatplotlibFigure
from matplotlib.figure import FigureBase

from numdaplot.plots.drawing.plot_drawing import FigureDrawing, build_figure
from numdaplot.plots.figure.cell import Cell
from numdaplot.plots.figure.figure_drawing import choose_figure_size, draw_figure
from numdaplot.plots.figure.figure_style import FigureStyle
from numdaplot.plots.figure.layout import Layout
from numdaplot.plots.figure.placement import Placement, require_cell_inside, require_free_cells
from numdaplot.plots.output.image_saving import write_image
from numdaplot.plots.output.plot_display import show_drawing
from numdaplot.plots.plot import Plot
from numdaplot.plots.style.image_options import ImageOptions
from numdaplot.settings.argument_types import checked_arguments
from numdaplot.tables.conflict import Conflict
from numdaplot.tables.files.file_paths import FilePath


class Figure:
	"""
	Several Plots placed on a grid of cells, shown and saved as one image.

	A Figure is immutable: ``place`` returns a new Figure. Each Plot keeps its own axes and its own PlotStyle,
	except its size: the Figure gives it the size of its cells. A cell without Plot stays blank.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layout
		The grid of cells.
	style
		The title and the size of the Figure, the default ``FigureStyle`` when omitted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> months = ndp.Array.from_list(["Jan", "Feb", "Mar", "Apr"])
	>>> sales = ndp.Array.from_list([120.0, 150.0, 90.0, 170.0])
	>>> visits = ndp.Array.from_list([900.0, 1100.0, 800.0, 1300.0])
	>>> shop = ndp.Table.from_arrays({"month": months, "sales": sales, "visits": visits})
	>>> sales_plot = ndp.plot_bar(shop, ndp.BarChart(x="month", y=["sales"]))
	>>> visits_plot = ndp.plot_line(shop, ndp.LineChart(x="month", y=["visits"]))
	>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=2), ndp.FigureStyle(title="Shop"))
	>>> figure = figure.place(sales_plot, ndp.Cell(row=0, column=0))
	>>> figure = figure.place(visits_plot, ndp.Cell(row=0, column=1))
	>>> figure.show()
	"""

	@checked_arguments
	def __init__(self, layout: Layout, style: FigureStyle | None = None) -> None:
		"""
		Keep the grid and the style of an empty Figure.

		.. versionadded:: 0.1.0

		Parameters
		----------
		layout
			The grid of cells.
		style
			The title and the size of the Figure, the default ``FigureStyle`` when omitted.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		"""
		if style is None:
			style = FigureStyle()

		self._layout = layout
		self._style = style
		self._placements = list[Placement]()

	@checked_arguments
	def place(self, plot: Plot, cell: Cell) -> Self:
		"""
		Return a new Figure with a Plot placed on a cell, and on the cells it spans.

		.. versionadded:: 0.1.0

		Parameters
		----------
		plot
			The Plot placed, which keeps its PlotStyle but takes the size of its cells.
		cell
			Its first cell, from row 0 and column 0, and the number of cells it spans.

		Returns
		-------
		Self
			A new Figure; this one is left unchanged.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		CellOutOfRangeError
			When a cell covered is outside the Layout.
		OccupiedCellError
			When a cell covered already holds a Plot.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
		>>> plot = ndp.plot_line(prices, style=ndp.PlotStyle(title="Prices"))
		>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=2))
		>>> placed_figure = figure.place(plot, ndp.Cell(row=0, column=1))
		>>> placed_figure.show()
		"""
		require_cell_inside(cell, self._layout)
		require_free_cells(cell, self._placements)
		placement = Placement(plot, cell)
		figure_class = type(self)
		placed_figure = figure_class(self._layout, self._style)
		placed_figure._placements = [*self._placements, placement]

		return placed_figure

	def to_matplotlib(self) -> MatplotlibFigure:
		"""
		Return a new matplotlib figure of the Figure, to change it with matplotlib.

		Each Plot is drawn on a matplotlib subfigure. Changing the figure never changes the Figure.

		.. versionadded:: 0.1.0

		Returns
		-------
		matplotlib.figure.Figure
			The figure, with one subfigure per Plot.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> plot = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]))
		>>> figure = ndp.Figure(ndp.Layout(rows=2, columns=2)).place(plot, ndp.Cell(row=1, column=1))
		>>> matplotlib_figure = figure.to_matplotlib()
		>>> len(matplotlib_figure.subfigs), matplotlib_figure.get_size_inches().tolist()
		(1, [9.6, 7.2])
		"""
		drawing = self._describe_drawing()
		matplotlib_figure = build_figure(drawing)

		return matplotlib_figure

	@checked_arguments
	def save(self, path: FilePath, options: ImageOptions | None = None, on_conflict: Conflict = Conflict.ERROR) -> None:
		"""
		Save the Figure as an image, in the format named by the extension of the path.

		``.png`` gives an image made of pixels, ``.svg`` and ``.pdf`` images made of lines and texts that stay
		sharp at any zoom.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the image, a ``FilePath`` such as ``"chart.png"`` or ``Path("images/chart.svg")``, ending with
			``.png``, ``.svg`` or ``.pdf``.
		options
			The resolution of a PNG image, 100 dots per inch when omitted. SVG and PDF images take none.
		on_conflict
			``ERROR`` by default, refusing to overwrite an existing file, or ``REPLACE`` to overwrite it.

		Raises
		------
		InvalidTypeError
			When an argument is not of the type its annotation names.
		UnsupportedImageFormatError
			When the path does not end with ``.png``, ``.svg`` or ``.pdf``.
		RefusedSettingError
			When options are given for an SVG or PDF image.
		FileExistsError
			When a file exists at the path and ``on_conflict`` is ``ERROR``.

		Examples
		--------
		>>> import tempfile
		>>> from pathlib import Path
		>>> import numdaplot as ndp
		>>> path = Path(tempfile.mkdtemp()) / "shop.pdf"
		>>> plot = ndp.plot_line(ndp.Array.from_list([12.0, 15.5]))
		>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=2)).place(plot, ndp.Cell(row=0, column=0))
		>>> figure.save(path)
		>>> path.read_bytes()[:4]
		b'%PDF'
		"""
		drawing = self._describe_drawing()
		write_image(drawing, path, options, on_conflict)

	def show(self) -> None:
		"""
		Show the Figure: as an image in a Jupyter notebook, in a matplotlib window anywhere else.

		In a script, the window stays open until it is closed. With a matplotlib backend that opens no window,
		such as the one of a server, matplotlib warns that the figure cannot be shown: save it instead.

		.. versionadded:: 0.1.0

		Examples
		--------
		>>> import numdaplot as ndp
		>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
		>>> line_plot = ndp.plot_line(prices, style=ndp.PlotStyle(title="Line"))
		>>> bar_plot = ndp.plot_bar(prices, style=ndp.PlotStyle(title="Bars"))
		>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=2), ndp.FigureStyle(title="Prices"))
		>>> figure = figure.place(line_plot, ndp.Cell(row=0, column=0))
		>>> figure = figure.place(bar_plot, ndp.Cell(row=0, column=1))
		>>> figure.show()
		"""
		drawing = self._describe_drawing()
		show_drawing(drawing)

	def _draw_on(self, target: FigureBase) -> None:
		"""
		Draw the Figure on an empty matplotlib figure.

		.. versionadded:: 0.1.0

		Parameters
		----------
		target
			The figure drawn on.
		"""
		draw_figure(target, self._layout, self._placements, self._style.title)

	def _describe_drawing(self) -> FigureDrawing:
		"""
		Return what the Figure draws, and its size.

		.. versionadded:: 0.1.0

		Returns
		-------
		FigureDrawing
			The drawing of the Figure.
		"""
		size_inches = choose_figure_size(self._layout, self._style.size)
		drawing = FigureDrawing(self._draw_on, size_inches)

		return drawing
