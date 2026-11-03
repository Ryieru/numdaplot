"""
Error raised when the bounds of an interval are reversed or not comparable.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_BOUNDS_MESSAGE = "Expected comparable bounds with low <= high, got low={low!r} and high={high!r}."


class InvalidBoundsError(NumdaplotError):
	"""
	Raised when the low bound is greater than the high bound, or when both cannot be compared.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		The rejected low bound.
	high
		The rejected high bound.

	Attributes
	----------
	low
		The rejected low bound.
	high
		The rejected high bound.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Between(low=20, high=10)
	... except ndp.InvalidBoundsError as error:
	... 	print(error)
	Expected comparable bounds with low <= high, got low=20 and high=10.
	"""

	def __init__(self, low: object, high: object) -> None:
		"""
		Build the error message from the rejected bounds.

		.. versionadded:: 0.1.0

		Parameters
		----------
		low
			The rejected low bound.
		high
			The rejected high bound.
		"""
		message = INVALID_BOUNDS_MESSAGE.format(low=low, high=high)
		super().__init__(message)
		self.low = low
		self.high = high
