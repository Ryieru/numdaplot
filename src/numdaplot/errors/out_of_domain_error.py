"""
Error raised when a math function is applied to a value it is not defined for.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

OUT_OF_DOMAIN_MESSAGE = "{function_name} is not defined for {value}."
BETWEEN_INTEGERS_MESSAGE = (
	"{function_name} is not defined for {value} between integers. Convert the values to FLOAT64 first."
)


class OutOfDomainError(NumdaplotError):
	"""
	Raised when a math function or an operator receives a value it is not defined for.

	For example, the square root of a negative number, the logarithm of 0, or an integer divided by 0 with ``//``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function_name
		Name of the math function.
	value
		The first value outside the domain of the function.
	between_integers
		True when decimals would accept the value, False by default.

	Attributes
	----------
	function_name
		Name of the math function.
	value
		The first value outside the domain of the function.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([4, -9])
	>>> try:
	... 	array.apply(ndp.SquareRoot())
	... except ndp.OutOfDomainError as error:
	... 	print(error)
	SquareRoot is not defined for -9.
	"""

	def __init__(self, function_name: str, value: float, between_integers: bool = False) -> None:
		"""
		Build the error message from the function name and the value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		function_name
			Name of the math function.
		value
			The first value outside the domain of the function.
		between_integers
			True when decimals would accept the value, False by default.
		"""
		message_format = BETWEEN_INTEGERS_MESSAGE if between_integers else OUT_OF_DOMAIN_MESSAGE
		message = message_format.format(function_name=function_name, value=value)
		super().__init__(message)

		self.function_name = function_name
		self.value = value
