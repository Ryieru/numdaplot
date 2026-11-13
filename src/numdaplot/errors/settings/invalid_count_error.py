"""
Error raised when a count of values is too low.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_COUNT_MESSAGE = "Expected a count of at least {minimum}, got {count}."


class InvalidCountError(NumdaplotError):
	"""
	Raised when a count of values is lower than the minimum it needs.

	``Spacing`` needs at least 2 values when both bounds are included, and at least 1 otherwise.

	.. versionadded:: 0.1.0

	Parameters
	----------
	count
		The rejected count.
	minimum
		The lowest accepted count.

	Attributes
	----------
	count
		The rejected count.
	minimum
		The lowest accepted count.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Spacing(start=0, stop=1, count=0)
	... except ndp.InvalidCountError as error:
	... 	print(error)
	Expected a count of at least 2, got 0.
	"""

	def __init__(self, count: int, minimum: int) -> None:
		"""
		Build the error message from the count and the minimum.

		.. versionadded:: 0.1.0

		Parameters
		----------
		count
			The rejected count.
		minimum
			The lowest accepted count.
		"""
		message = INVALID_COUNT_MESSAGE.format(count=count, minimum=minimum)
		super().__init__(message)

		self.count = count
		self.minimum = minimum
