"""
Unit tests of InvalidColumnNameError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.tables.invalid_column_name_error import InvalidColumnNameError

COLUMN_NAME = 0
EXPECTED_MESSAGE = "Expected a column name as a non-empty text, got 0."


def test_invalid_column_name_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidColumnNameError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidColumnNameError, NumdaplotError)


def test_invalid_column_name_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColumnNameError(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_column_name_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColumnNameError(COLUMN_NAME)

	assert error.column_name == COLUMN_NAME
