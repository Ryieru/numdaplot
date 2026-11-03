"""
Error raised when a pandas DataFrame has an index holding information.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_INDEX_MESSAGE = (
	"A Table has no index, call reset_index() on the pandas DataFrame first to keep its index as a column."
)


class UnsupportedIndexError(NumdaplotError):
	"""
	Raised by ``Table.from_pandas`` when the index of the pandas DataFrame is not the plain row numbers 0, 1, 2...

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> import pandas
	>>> frame = pandas.DataFrame({"price": [1, 2]}, index=["Paris", "Lyon"])
	>>> try:
	... 	ndp.Table.from_pandas(frame)
	... except ndp.UnsupportedIndexError as error:
	... 	print(error)
	A Table has no index, call reset_index() on the pandas DataFrame first to keep its index as a column.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(UNSUPPORTED_INDEX_MESSAGE)
