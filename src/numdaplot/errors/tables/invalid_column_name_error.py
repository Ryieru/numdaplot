"""
Error raised when a column name is not a non-empty text.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_COLUMN_NAME_MESSAGE = "Expected a column name as a non-empty text, got {column_name!r}."


class InvalidColumnNameError(NumdaplotError):
	"""
	Raised when a column name is empty or is not a text, such as a number in a pandas DataFrame.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_name
		The rejected name.

	Attributes
	----------
	column_name
		The rejected name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.NameChange(old_name="price", new_name="")
	... except ndp.InvalidColumnNameError as error:
	... 	print(error)
	Expected a column name as a non-empty text, got ''.
	"""

	def __init__(self, column_name: object) -> None:
		"""
		Build the error message from the column name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The rejected name.
		"""
		message = INVALID_COLUMN_NAME_MESSAGE.format(column_name=column_name)
		super().__init__(message)

		self.column_name = column_name
