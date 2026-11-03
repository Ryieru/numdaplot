"""
Error raised when an Array is combined with something else than an Array or a single value.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

UNSUPPORTED_OPERAND_MESSAGE = "Expected an Array or a single value, got {type_name}."


class UnsupportedOperandError(NumdaplotError):
	"""
	Raised when an Array is combined with a numpy array, a list or any object that is not a single value.

	Convert a numpy array with ``Array.from_numpy`` and a list with ``Array.from_list`` first.

	.. versionadded:: 0.1.0

	Parameters
	----------
	type_name
		Name of the Python type of the rejected operand.

	Attributes
	----------
	type_name
		Name of the Python type of the rejected operand.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2])
	>>> try:
	... 	array + [10, 20]
	... except ndp.UnsupportedOperandError as error:
	... 	print(error)
	Expected an Array or a single value, got list.
	"""

	def __init__(self, type_name: str) -> None:
		"""
		Build the error message from the type name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		type_name
			Name of the Python type of the rejected operand.
		"""
		message = UNSUPPORTED_OPERAND_MESSAGE.format(type_name=type_name)
		super().__init__(message)

		self.type_name = type_name
