"""
Error raised when a custom date pattern cannot read dates.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_DATE_FORMAT_MESSAGE = (
	"Expected a date pattern with a day, a month or a year code and no time zone code, got {pattern!r}."
)


class InvalidDateFormatError(NumdaplotError):
	"""
	Raised when a custom date pattern has no day, month or year code, or has a time zone code.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pattern
		The rejected pattern.

	Attributes
	----------
	pattern
		The rejected pattern.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.CustomDateFormat("%H:%M")
	... except ndp.InvalidDateFormatError as error:
	... 	print(error)
	Expected a date pattern with a day, a month or a year code and no time zone code, got '%H:%M'.
	"""

	def __init__(self, pattern: str) -> None:
		"""
		Build the error message from the rejected pattern.

		.. versionadded:: 0.1.0

		Parameters
		----------
		pattern
			The rejected pattern.
		"""
		message = INVALID_DATE_FORMAT_MESSAGE.format(pattern=pattern)
		super().__init__(message)
		self.pattern = pattern
