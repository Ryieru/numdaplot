"""
Error raised when a column name appears more than once.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_COLUMN_MESSAGE = "The column name {column_name!r} appears more than once."


class DuplicateColumnError(NumdaplotError):
	"""
	Raised when a column name appears twice.

	For example in a file header, in a list of columns, or when renaming or adding a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The repeated name.

	Attributes
	----------
	column_name
		The repeated name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ColumnChoice(columns=["price", "price"])
	... except ndp.DuplicateColumnError as error:
	... 	print(error)
	The column name 'price' appears more than once.
	"""

	def __init__(self, column_name: str) -> None:
		"""
		Build the error message from the column name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The repeated name.
		"""
		message = DUPLICATE_COLUMN_MESSAGE.format(column_name=column_name)
		super().__init__(message)

		self.column_name = column_name
