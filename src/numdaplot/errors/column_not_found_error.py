"""
Error raised when a Table has no column of a given name.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

COLUMN_NOT_FOUND_MESSAGE = "No column is named {column_name!r}."


class ColumnNotFoundError(NumdaplotError):
	"""
	Raised when an operation names a column that the Table does not have.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The name that matches no column.

	Attributes
	----------
	column_name
		The name that matches no column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([1, 2])})
	>>> try:
	... 	table.column("prise")
	... except ndp.ColumnNotFoundError as error:
	... 	print(error)
	No column is named 'prise'.
	"""

	def __init__(self, column_name: str) -> None:
		"""
		Build the error message from the column name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name that matches no column.
		"""
		message = COLUMN_NOT_FOUND_MESSAGE.format(column_name=column_name)
		super().__init__(message)

		self.column_name = column_name
