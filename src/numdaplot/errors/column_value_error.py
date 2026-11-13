"""
Base class of the errors about values, whose message names the Table column holding them once it is known.

.. versionadded:: 0.2.0
"""

from typing import ClassVar

from numdaplot.errors.numdaplot_error import NumdaplotError

NO_COLUMN_TEXT = ""
MISSING_MESSAGE_WRITER = "Each error naming its column writes its own message."


class ColumnValueError(NumdaplotError):
	"""
	Base class of the errors about values, whose message names the Table column holding them once it is known.

	The error is raised by code that only sees values. The code reading a Table column then calls ``name_column``,
	which writes the message again with the name of the column.

	.. versionadded:: 0.2.0

	Attributes
	----------
	column_name
		Name of the Table column holding the values, or ``None`` for the values of an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> error = ndp.TimeOverflowError("convert", "DATETIME")
	>>> error.name_column("day")
	>>> print(error)
	The operation convert gives values of the column 'day' outside the range of DATETIME, from 1677 to 2262.
	"""

	# The words naming the column inside the message, placed by write_message.
	COLUMN_TEXT: ClassVar[str] = " of the column {column_name!r}"
	column_name: str | None

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, with the words naming the column, written by each error of this base class.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column_text
			The words naming the column, or an empty text.

		Returns
		-------
		str
			The message.

		Raises
		------
		NotImplementedError
			Always, for this base class, which has no message of its own.
		"""
		raise NotImplementedError(MISSING_MESSAGE_WRITER)

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
		>>> error = ndp.UnmatchedValueError(3)
		>>> error.name_column("sex")
		>>> error.name_column("age")
		>>> print(error)
		The value 3 of the column 'sex' has no ValueChange. Add one,
		or give others=Unmatched.MISSING to make it missing, or others=Unmatched.KEEP to keep it.
		"""
		if self.column_name is not None:
			return

		self.column_name = column_name
		column_text = self.COLUMN_TEXT.format(column_name=column_name)
		message = self.write_message(column_text)
		self.args = (message,)
