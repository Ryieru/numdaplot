"""
Error raised when nested lists do not form a regular block.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

IRREGULAR_LIST_MESSAGE = "Expected nested lists of equal lengths."


class IrregularListError(NumdaplotError):
	"""
	Raised when nested lists do not form a regular block of rows and columns.

	The lists at one level have different lengths, or mix lists and single values.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([[1, 2], [3]])
	... except ndp.IrregularListError as error:
	... 	print(error)
	Expected nested lists of equal lengths.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(IRREGULAR_LIST_MESSAGE)
