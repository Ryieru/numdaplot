"""
Error raised when a cell is outside the Layout of a Figure.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

CELL_OUT_OF_RANGE_MESSAGE = "Cell ({row}, {column}) is outside a Layout of {row_count} rows and {column_count} columns."


class CellOutOfRangeError(NumdaplotError):
	"""
	Raised when a ``Cell``, or a cell it spans, is beyond the rows or the columns of the ``Layout`` of a ``Figure``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row
		The row of the cell, from 0.
	column
		The column of the cell, from 0.
	row_count
		The number of rows of the Layout.
	column_count
		The number of columns of the Layout.

	Attributes
	----------
	row
		The row of the cell, from 0.
	column
		The column of the cell, from 0.
	row_count
		The number of rows of the Layout.
	column_count
		The number of columns of the Layout.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, 15.5, 14.0])
	>>> plot = ndp.plot_line(prices, ndp.LineChart())
	>>> figure = ndp.Figure(ndp.Layout(rows=2, columns=2))
	>>> try:
	... 	figure.place(plot, ndp.Cell(row=2, column=0))
	... except ndp.CellOutOfRangeError as error:
	... 	print(error)
	Cell (2, 0) is outside a Layout of 2 rows and 2 columns.
	"""

	def __init__(self, row: int, column: int, row_count: int, column_count: int) -> None:
		"""
		Build the error message from the cell and the size of the Layout.

		.. versionadded:: 0.1.0

		Parameters
		----------
		row
			The row of the cell, from 0.
		column
			The column of the cell, from 0.
		row_count
			The number of rows of the Layout.
		column_count
			The number of columns of the Layout.
		"""
		message = CELL_OUT_OF_RANGE_MESSAGE.format(
			row=row, column=column, row_count=row_count, column_count=column_count
		)
		super().__init__(message)
		self.row = row
		self.column = column
		self.row_count = row_count
		self.column_count = column_count
