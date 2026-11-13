"""
Error raised when an operation is not available on an Array, a Table or a Plot.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

REFUSED_OPERATION_MESSAGE = "{operation} is not available, use {alternative} instead."


class RefusedOperationError(NumdaplotError):
	"""
	Raised when a Python operation is not available on an Array, a Table or a Plot, such as ``<`` or ``len``.

	Calling the constructor of an Array, a Table or a Plot raises it too.

	The message names the numdaplot method to use instead.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		Description of the refused operation, naming what it applies to.
	alternative
		Description of what to use instead.

	Attributes
	----------
	operation
		Description of the refused operation, naming what it applies to.
	alternative
		Description of what to use instead.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2])
	>>> try:
	... 	array < 2
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Comparing an Array with < is not available, use select or check with a rule such as ndp.Less instead.
	"""

	def __init__(self, operation: str, alternative: str) -> None:
		"""
		Build the error message from the operation and the alternative.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			Description of the refused operation, naming what it applies to.
		alternative
			Description of what to use instead.
		"""
		message = REFUSED_OPERATION_MESSAGE.format(operation=operation, alternative=alternative)
		super().__init__(message)

		self.operation = operation
		self.alternative = alternative
