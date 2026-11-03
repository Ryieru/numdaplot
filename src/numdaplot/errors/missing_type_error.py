"""
Error raised when the type of an Array cannot be guessed.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

MISSING_TYPE_MESSAGE = "Cannot guess the type of an Array without any present value, give dtype."


class MissingTypeError(NumdaplotError):
	"""
	Raised when the type of a new Array cannot be guessed.

	The Array is created without any present value and without ``dtype``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([])
	... except ndp.MissingTypeError as error:
	... 	print(error)
	Cannot guess the type of an Array without any present value, give dtype.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(MISSING_TYPE_MESSAGE)
