"""
Error raised when a value is given twice where each value must be unique.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

DUPLICATE_VALUE_MESSAGE = "The value {value!r} appears more than once."


class DuplicateValueError(NumdaplotError):
	"""
	Raised when a value is given twice where each value must be unique.

	For example, the same old value in two ``ValueChange`` of a ``ValueMapping``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The repeated value.

	Attributes
	----------
	value
		The repeated value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ValueMapping(changes=[ndp.ValueChange(2, "Femme"), ndp.ValueChange(2, "F")])
	... except ndp.DuplicateValueError as error:
	... 	print(error)
	The value 2 appears more than once.
	"""

	def __init__(self, value: object) -> None:
		"""
		Build the error message from the repeated value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value
			The repeated value.
		"""
		message = DUPLICATE_VALUE_MESSAGE.format(value=value)
		super().__init__(message)

		self.value = value
