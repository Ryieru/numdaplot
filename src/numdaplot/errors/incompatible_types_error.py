"""
Error raised when an operation does not apply to the types of its values.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TYPE_NAME_SEPARATOR = " and "
INCOMPATIBLE_TYPES_MESSAGE = "Cannot apply {operation} to {type_names}."


class IncompatibleTypesError(NumdaplotError):
	"""
	Raised when an operation, a rule, a statistic or a math function does not apply to the types it receives.

	For example, a number cannot be added to a text, and ``Contains`` only applies to text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
	type_names
		Names of the ``ndp.Type`` members the operation received, in order.

	Attributes
	----------
	operation
		Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
	type_names
		Names of the ``ndp.Type`` members the operation received, in order.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2])
	>>> try:
	... 	array + "euros"
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply + to INT64 and TEXT.
	"""

	def __init__(self, operation: str, type_names: list[str]) -> None:
		"""
		Build the error message from the operation and the type names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			Name of the operation: an operator such as ``"+"``, or a rule, statistic or function name.
		type_names
			Names of the ``ndp.Type`` members the operation received, in order.
		"""
		joined_type_names = TYPE_NAME_SEPARATOR.join(type_names)
		message = INCOMPATIBLE_TYPES_MESSAGE.format(operation=operation, type_names=joined_type_names)
		super().__init__(message)

		self.operation = operation
		self.type_names = list(type_names)
