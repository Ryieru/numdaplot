"""
Error raised when a searched text is empty.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_TEXT_MESSAGE = "Expected a non-empty text to search for."


class EmptyTextError(NumdaplotError):
	"""
	Raised when a rule receives an empty text to search for, which every text would contain.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Contains("")
	... except ndp.EmptyTextError as error:
	... 	print(error)
	Expected a non-empty text to search for.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(EMPTY_TEXT_MESSAGE)
