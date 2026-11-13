"""
Unit tests of the base class of the errors naming the column of their values.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.errors.column_value_error import NO_COLUMN_TEXT, ColumnValueError
from numdaplot.errors.numdaplot_error import NumdaplotError

FIRST_COLUMN = "sex"
SECOND_COLUMN = "age"
MESSAGE_START = "Wrong value"
EXPECTED_UNNAMED_MESSAGE = "Wrong value."
EXPECTED_NAMED_MESSAGE = "Wrong value of the column 'sex'."


class WrongValueError(ColumnValueError):
	"""
	Error about a value, written for the tests.

	.. versionadded:: 0.2.0
	"""

	def __init__(self) -> None:
		"""
		Build the message without column.

		.. versionadded:: 0.2.0
		"""
		self.column_name = None
		message = self.write_message(NO_COLUMN_TEXT)
		super().__init__(message)

	def write_message(self, column_text: str) -> str:
		"""
		Return the message, the column named before the final period.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column_text
			The words naming the column, or an empty text.

		Returns
		-------
		str
			The message.
		"""
		message = f"{MESSAGE_START}{column_text}."

		return message


def test_column_value_error_is_a_numdaplot_error() -> None:
	"""
	Check that the errors of the base class are caught by NumdaplotError.

	.. versionadded:: 0.2.0
	"""
	assert issubclass(ColumnValueError, NumdaplotError)


def test_column_value_error_leaves_its_message_to_each_error() -> None:
	"""
	Check that the base class has no message of its own to write.

	.. versionadded:: 0.2.0
	"""
	base_error = ColumnValueError(MESSAGE_START)

	with pytest.raises(NotImplementedError):
		base_error.write_message(NO_COLUMN_TEXT)


def test_name_column_writes_the_column_in_the_message() -> None:
	"""
	Check that naming the column writes the message again with it, and keeps it as an attribute.

	.. versionadded:: 0.2.0
	"""
	error = WrongValueError()

	error.name_column(FIRST_COLUMN)

	error_text = str(error)
	assert error_text == EXPECTED_NAMED_MESSAGE
	assert error.column_name == FIRST_COLUMN


def test_name_column_keeps_the_first_column_named() -> None:
	"""
	Check that a second column leaves the first one in the message.

	.. versionadded:: 0.2.0
	"""
	error = WrongValueError()
	error.name_column(FIRST_COLUMN)

	error.name_column(SECOND_COLUMN)

	error_text = str(error)
	assert error_text == EXPECTED_NAMED_MESSAGE


def test_an_error_without_column_has_a_plain_message() -> None:
	"""
	Check that an error not named keeps its message without column.

	.. versionadded:: 0.2.0
	"""
	error = WrongValueError()

	error_text = str(error)
	assert error_text == EXPECTED_UNNAMED_MESSAGE
	assert error.column_name is None
