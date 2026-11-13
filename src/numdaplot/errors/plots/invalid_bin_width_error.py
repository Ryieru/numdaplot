"""
Error raised when the bins of a histogram have a width of 0 or less, or a duration beyond a day.

.. versionadded:: 0.1.0
"""

from datetime import timedelta

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_BIN_WIDTH_MESSAGE = "Expected a bin width above 0, got {width}."
INVALID_BIN_DURATION_MESSAGE = "Expected a bin width above 0 and at most 1 day, got {width}."


class InvalidBinWidthError(NumdaplotError):
	"""
	Raised when a ``BinWidth`` is 0 or negative, or a duration beyond a day.

	Such a width would never cover the values, or be wider than every time of day.

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
	>>> from datetime import timedelta
	>>> try:
	... 	ndp.BinWidth(timedelta(days=2))
	... except ndp.InvalidBinWidthError as error:
	... 	print(error)
	Expected a bin width above 0 and at most 1 day, got 2 days, 0:00:00.
	"""

	def __init__(self, width: float | timedelta) -> None:
		"""
		Build the error message from the width.

		.. versionadded:: 0.1.0

		Parameters
		----------
		width
			The rejected width.
		"""
		message_format = INVALID_BIN_WIDTH_MESSAGE
		if isinstance(width, timedelta):
			message_format = INVALID_BIN_DURATION_MESSAGE

		message = message_format.format(width=width)
		super().__init__(message)
		self.width = width
