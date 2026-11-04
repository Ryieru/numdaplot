"""
Error raised when the bins of a histogram have a width of 0 or less.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_BIN_WIDTH_MESSAGE = "Expected a bin width above 0, got {width}."


class InvalidBinWidthError(NumdaplotError):
	"""
	Raised when a ``BinWidth`` is 0 or negative, which would never cover the values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The rejected width.

	Attributes
	----------
	width
		The rejected width.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.BinWidth(-5.0)
	... except ndp.InvalidBinWidthError as error:
	... 	print(error)
	Expected a bin width above 0, got -5.0.
	"""

	def __init__(self, width: float) -> None:
		"""
		Build the error message from the width.

		.. versionadded:: 0.1.0

		Parameters
		----------
		width
			The rejected width.
		"""
		message = INVALID_BIN_WIDTH_MESSAGE.format(width=width)
		super().__init__(message)
		self.width = width
