"""
Error raised when a Table has no column of a given name.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

COLUMN_NOT_FOUND_MESSAGE = "No column is named {column_name!r}."
TABLE_COLUMN_NOT_FOUND_MESSAGE = "No column of {table_name} is named {column_name!r}."


class ColumnNotFoundError(NumdaplotError):
	"""
	Raised when an operation names a column that the Table does not have.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The name that matches no column.
	table_name
		The Table searched, such as ``"the other Table"`` of a join. When omitted, only one Table is involved.

	Attributes
	----------
	column_name
		The name that matches no column.
	table_name
		The Table searched, or None.

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

	def __init__(self, column_name: str, table_name: str | None = None) -> None:
		"""
		Build the error message from the column name, and from the Table searched when it is given.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name that matches no column.
		table_name
			The Table searched. When omitted, only one Table is involved.
		"""
		message = COLUMN_NOT_FOUND_MESSAGE.format(column_name=column_name)
		if table_name is not None:
			message = TABLE_COLUMN_NOT_FOUND_MESSAGE.format(table_name=table_name, column_name=column_name)

		super().__init__(message)

		self.column_name = column_name
		self.table_name = table_name
