"""
Error raised when a standard deviation is negative.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_DEVIATION_MESSAGE = "Expected a deviation of at least 0, got {deviation}."


class InvalidDeviationError(NumdaplotError):
	"""
	Raised when a normal distribution is given a negative standard deviation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	deviation
		The rejected standard deviation.

	Attributes
	----------
	deviation
		The rejected standard deviation.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Normal(mean=0, deviation=-1)
	... except ndp.InvalidDeviationError as error:
	... 	print(error)
	Expected a deviation of at least 0, got -1.
	"""

	def __init__(self, deviation: float) -> None:
		"""
		Build the error message from the deviation.

		.. versionadded:: 0.1.0

		Parameters
		----------
		deviation
			The rejected standard deviation.
		"""
		message = INVALID_DEVIATION_MESSAGE.format(deviation=deviation)
		super().__init__(message)

		self.deviation = deviation
