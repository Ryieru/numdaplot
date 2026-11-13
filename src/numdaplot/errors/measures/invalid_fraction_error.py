"""
Error raised when a fraction is outside 0 to 1.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_FRACTION_MESSAGE = "Expected a fraction between 0 and 1, got {value}."


class InvalidFractionError(NumdaplotError):
	"""
	Raised when a value expected to be a fraction is lower than 0, greater than 1 or not a number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The rejected value.

	Attributes
	----------
	value
		The rejected value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Quantile(1.5)
	... except ndp.InvalidFractionError as error:
	... 	print(error)
	Expected a fraction between 0 and 1, got 1.5.
	"""

	def __init__(self, value: float) -> None:
		"""
		Build the error message from the rejected value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value
			The rejected value.
		"""
		message = INVALID_FRACTION_MESSAGE.format(value=value)
		super().__init__(message)
		self.value = value
