"""
Error raised when a CSV separator is not exactly one character.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SEPARATOR_MESSAGE = "Expected a separator of exactly one character, got {separator!r}."


class InvalidSeparatorError(NumdaplotError):
	"""
	Raised when the separator of ``CsvOptions`` is empty or longer than one character.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The rejected separator.

	Attributes
	----------
	separator
		The rejected separator.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.CsvOptions(separator=";;")
	... except ndp.InvalidSeparatorError as error:
	... 	print(error)
	Expected a separator of exactly one character, got ';;'.
	"""

	def __init__(self, separator: str) -> None:
		"""
		Build the error message from the separator.

		.. versionadded:: 0.1.0

		Parameters
		----------
		separator
			The rejected separator.
		"""
		message = INVALID_SEPARATOR_MESSAGE.format(separator=separator)
		super().__init__(message)

		self.separator = separator
