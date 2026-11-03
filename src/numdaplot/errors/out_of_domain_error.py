"""
Error raised when a math function is applied to a value it is not defined for.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

OUT_OF_DOMAIN_MESSAGE = "{function_name} is not defined for {value}."


class OutOfDomainError(NumdaplotError):
	"""
	Raised when a math function receives a value it is not defined for.

	For example, the square root of a negative number, or the logarithm of 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function_name
		Name of the math function.
	value
		The first value outside the domain of the function.

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

	def __init__(self, function_name: str, value: float) -> None:
		"""
		Build the error message from the function name and the value.

		.. versionadded:: 0.1.0

		Parameters
		----------
		function_name
			Name of the math function.
		value
			The first value outside the domain of the function.
		"""
		message = OUT_OF_DOMAIN_MESSAGE.format(function_name=function_name, value=value)
		super().__init__(message)

		self.function_name = function_name
		self.value = value
