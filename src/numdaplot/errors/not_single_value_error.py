"""
Error raised when a single value is asked from an Array holding another number of values.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

NOT_SINGLE_VALUE_MESSAGE = "Expected exactly one value, got {value_count}."


class NotSingleValueError(NumdaplotError):
	"""
	Raised when ``to_value`` is called on an Array that does not hold exactly one value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value_count
		Number of values held by the Array.

	Attributes
	----------
	value_count
		Number of values held by the Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2])
	>>> try:
	... 	array.to_value()
	... except ndp.NotSingleValueError as error:
	... 	print(error)
	Expected exactly one value, got 2.
	"""

	def __init__(self, value_count: int) -> None:
		"""
		Build the error message from the value count.

		.. versionadded:: 0.1.0

		Parameters
		----------
		value_count
			Number of values held by the Array.
		"""
		message = NOT_SINGLE_VALUE_MESSAGE.format(value_count=value_count)
		super().__init__(message)

		self.value_count = value_count
