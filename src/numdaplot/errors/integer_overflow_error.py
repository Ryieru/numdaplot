"""
Error raised when the result of a calculation does not fit an integer type.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INTEGER_OVERFLOW_MESSAGE = (
	"The operation {operation_name} gives values too large for {type_name}. Convert the values to FLOAT64 first."
)


class IntegerOverflowError(NumdaplotError):
	"""
	Raised when an integer result does not fit its type, which would otherwise wrap around to a wrong number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation_name
		The operator or the statistic, such as ``*`` or ``Sum``.
	type_name
		Name of the ``ndp.Type`` member that cannot hold the result.

	Attributes
	----------
	operation_name
		The operator or the statistic, such as ``*`` or ``Sum``.
	type_name
		Name of the ``ndp.Type`` member that cannot hold the result.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([2**62]) * 4
	... except ndp.IntegerOverflowError as error:
	... 	print(error)
	The operation * gives values too large for INT64. Convert the values to FLOAT64 first.
	"""

	def __init__(self, operation_name: str, type_name: str) -> None:
		"""
		Build the error message from the operation and the type names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation_name
			The operator or the statistic, such as ``*`` or ``Sum``.
		type_name
			Name of the ``ndp.Type`` member that cannot hold the result.
		"""
		message = INTEGER_OVERFLOW_MESSAGE.format(operation_name=operation_name, type_name=type_name)
		super().__init__(message)

		self.operation_name = operation_name
		self.type_name = type_name
