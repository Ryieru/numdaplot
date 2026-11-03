"""
Error raised when a list of accepted values is empty.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

EMPTY_VALUES_MESSAGE = "Expected at least one accepted value, got an empty list."


class EmptyValuesError(NumdaplotError):
	"""
	Raised when a rule receives an empty list of accepted values, which would never keep anything.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.IsIn([])
	... except ndp.EmptyValuesError as error:
	... 	print(error)
	Expected at least one accepted value, got an empty list.
	"""

	def __init__(self) -> None:
		"""
		Build the error message.

		.. versionadded:: 0.1.0
		"""
		super().__init__(EMPTY_VALUES_MESSAGE)
