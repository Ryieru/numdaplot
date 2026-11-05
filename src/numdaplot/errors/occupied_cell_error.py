"""
Error raised when a Plot is placed on a cell of a Figure that already holds one.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

OCCUPIED_CELL_MESSAGE = "Cell ({row}, {column}) already holds a Plot."


class OccupiedCellError(NumdaplotError):
	"""
	Raised when a Plot is placed on a cell of a ``Figure`` already covered by another Plot, even partly.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row
		The row of the first occupied cell, from 0.
	column
		The column of the first occupied cell, from 0.

	Attributes
	----------
	row
		The row of the first occupied cell, from 0.
	column
		The column of the first occupied cell, from 0.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
	>>> plot = ndp.plot_line(prices)
	>>> figure = ndp.Figure(ndp.Layout(rows=1, columns=2))
	>>> first_cell = ndp.Cell(row=0, column=0)
	>>> figure = figure.place(plot, first_cell)
	>>> try:
	... 	figure.place(plot, first_cell)
	... except ndp.OccupiedCellError as error:
	... 	print(error)
	Cell (0, 0) already holds a Plot.
	"""

	def __init__(self, row: int, column: int) -> None:
		"""
		Build the error message from the occupied cell.

		.. versionadded:: 0.1.0

		Parameters
		----------
		row
			The row of the first occupied cell, from 0.
		column
			The column of the first occupied cell, from 0.
		"""
		message = OCCUPIED_CELL_MESSAGE.format(row=row, column=column)
		super().__init__(message)
		self.row = row
		self.column = column
