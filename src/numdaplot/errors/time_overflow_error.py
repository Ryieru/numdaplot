"""
Error raised when dates, datetimes or durations leave the range a count of nanoseconds can hold.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

TIME_OVERFLOW_MESSAGE = "The operation {operation_name} gives values{column_text} outside the range of {range_text}."
COLUMN_TEXT = " of the column {column_name!r}"
NO_COLUMN_TEXT = ""
TYPE_RANGES = {
	"DATE": "DATE, from 1677 to 2262 in a calculation",
	"DATETIME": "DATETIME, from 1677 to 2262",
	"DURATION": "DURATION, about 292 years before or after zero",
}


class TimeOverflowError(NumdaplotError):
	"""
	Raised when a value does not fit the nanoseconds counting datetimes and durations.

	Without it, the value would become a wrong date or duration without any notice. A ``DATE`` is stored
	in days and can be outside this range, but a calculation on it cannot.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation_name
		The operator or the function, such as ``*``, ``from_list`` or ``ToDuration``.
	type_name
		Name of the ``ndp.Type`` member that cannot hold the result: ``DATE``, ``DATETIME`` or ``DURATION``.

	Attributes
	----------
	operation_name
		The operator or the function, such as ``*``, ``from_list`` or ``ToDuration``.
	type_name
		Name of the ``ndp.Type`` member that cannot hold the result.
	column_name
		Name of the Table column holding the values, or ``None`` for values given to an Array.

	Examples
	--------
	>>> from datetime import timedelta
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Array.from_list([timedelta(days=1)]) * 200000
	... except ndp.TimeOverflowError as error:
	... 	print(error)
	The operation * gives values outside the range of DURATION, about 292 years before or after zero.
	"""

	def __init__(self, operation_name: str, type_name: str) -> None:
		"""
		Build the error message from the operation and the type names.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation_name
			The operator or the function, such as ``*``, ``from_list`` or ``ToDuration``.
		type_name
			Name of the ``ndp.Type`` member that cannot hold the result.
		"""
		self.operation_name = operation_name
		self.type_name = type_name
		self.column_name: str | None = None
		message = self.write_message(NO_COLUMN_TEXT)
		super().__init__(message)

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, with the range of the type.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_text
			The words naming the column after the values, or an empty text.

		Returns
		-------
		str
			The message.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> ndp.TimeOverflowError("+", "DATETIME").write_message("")
		'The operation + gives values outside the range of DATETIME, from 1677 to 2262.'
		"""
		range_text = TYPE_RANGES[self.type_name]
		message = TIME_OVERFLOW_MESSAGE.format(
			operation_name=self.operation_name,
			column_text=column_text,
			range_text=range_text,
		)

		return message

	def name_column(self, column_name: str) -> None:
		"""
		Name the Table column holding the values in the message, unless a column is already named.

		.. versionadded:: 0.1.0

		Parameters
		----------
		column_name
			The name of the column.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> error = ndp.TimeOverflowError("convert", "DATETIME")
		>>> error.name_column("day")
		>>> print(error)
		The operation convert gives values of the column 'day' outside the range of DATETIME, from 1677 to 2262.
		"""
		if self.column_name is not None:
			return

		self.column_name = column_name
		column_text = COLUMN_TEXT.format(column_name=column_name)
		message = self.write_message(column_text)
		self.args = (message,)
