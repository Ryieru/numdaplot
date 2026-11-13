"""
Error raised when a math function is applied to a value it is not defined for.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.column_value_error import NO_COLUMN_TEXT, ColumnValueError

OUT_OF_DOMAIN_MESSAGE = "{function_name} is not defined for {value}{column_text}."
BETWEEN_INTEGERS_MESSAGE = (
	"{function_name} is not defined for {value} between integers{column_text}. Convert the values to FLOAT64 first."
)


class OutOfDomainError(ColumnValueError):
	"""
	Raised when a math function or an operator receives a value it is not defined for.

	For example, the square root of a negative number, the logarithm of 0, or an integer divided by 0 with ``//``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The message names the Table column holding the value.

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
	between_integers
		True when decimals would accept the value.
	column_name
		Name of the Table column holding the value, or ``None`` for the values of an Array.

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

	COLUMN_TEXT = " in the column {column_name!r}"

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
		self.function_name = function_name
		self.value = value
		self.between_integers = between_integers
		self.column_name: str | None = None
		message = self.write_message(NO_COLUMN_TEXT)
		super().__init__(message)

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, with the advice to convert integers when decimals would accept the value.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column_text
			The words naming the column after the value, or an empty text.

		Returns
		-------
		str
			The message.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.OutOfDomainError("Logarithm", 0).write_message("")
		'Logarithm is not defined for 0.'
		"""
		message_format = BETWEEN_INTEGERS_MESSAGE if self.between_integers else OUT_OF_DOMAIN_MESSAGE
		message = message_format.format(function_name=self.function_name, value=self.value, column_text=column_text)

		return message
