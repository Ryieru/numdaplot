"""
Error raised when a logarithm base is not usable.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_BASE_MESSAGE = "Expected a logarithm base greater than 0 and different from 1, got {base}."


class InvalidBaseError(NumdaplotError):
	"""
	Raised when a logarithm base is lower than or equal to 0, or equal to 1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	base
		The rejected base.

	Attributes
	----------
	base
		The rejected base.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Logarithm(base=1)
	... except ndp.InvalidBaseError as error:
	... 	print(error)
	Expected a logarithm base greater than 0 and different from 1, got 1.
	"""

	def __init__(self, base: float) -> None:
		"""
		Build the error message from the base.

		.. versionadded:: 0.1.0

		Parameters
		----------
		base
			The rejected base.
		"""
		message = INVALID_BASE_MESSAGE.format(base=base)
		super().__init__(message)

		self.base = base
