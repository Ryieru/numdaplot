"""
Look of a whole Figure.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.plots.style.size import Size


@dataclass(frozen=True)
class FigureStyle:
	"""
	Look of a whole Figure: its title and its size, used by ``Figure``.

	The look of each Plot belongs to its ``PlotStyle``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	title
		The title above the grid, no title when omitted.
	size
		The width and the height of the whole Figure, 4.8 by 3.6 inches per cell when omitted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> plot = ndp.plot_line(prices)
	>>> style = ndp.FigureStyle(title="Prices", size=ndp.Size(width=8, height=3))
	>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=1), style)
	>>> figure = figure.place(plot, ndp.Cell(row=0, column=0))
	>>> figure.show()
	"""

	title: str | None = None
	size: Size | None = None
