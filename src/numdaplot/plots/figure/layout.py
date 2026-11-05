"""
Grid of cells of a Figure.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_count_error import InvalidCountError

MINIMUM_LINE_COUNT = 1


@dataclass(frozen=True)
class Layout:
	"""
	Grid of cells of a ``Figure``, each cell holding a Plot or left blank.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		The number of rows of cells, at least 1.
	columns
		The number of columns of cells, at least 1.

	Raises
	------
	InvalidCountError
		When ``rows`` or ``columns`` is lower than 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0, 17.0])
	>>> line_plot = ndp.plot_line(prices)
	>>> bar_plot = ndp.plot_bar(prices)
	>>> layout = ndp.Layout(rows=2, columns=1)
	>>> figure = ndp.Figure(layout)
	>>> figure = figure.place(line_plot, ndp.Cell(row=0, column=0))
	>>> figure = figure.place(bar_plot, ndp.Cell(row=1, column=0))
	>>> figure.show()
	"""

	rows: int
	columns: int

	def __post_init__(self) -> None:
		"""
		Check the number of rows and of columns.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidCountError
			When ``rows`` or ``columns`` is lower than 1.
		"""
		if self.rows < MINIMUM_LINE_COUNT:
			raise InvalidCountError(self.rows, MINIMUM_LINE_COUNT)

		if self.columns < MINIMUM_LINE_COUNT:
			raise InvalidCountError(self.columns, MINIMUM_LINE_COUNT)
