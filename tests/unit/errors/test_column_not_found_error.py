"""
Unit tests of ColumnNotFoundError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.numdaplot_error import NumdaplotError

COLUMN_NAME = "prise"
EXPECTED_MESSAGE = "No column is named 'prise'."


def test_column_not_found_error_is_a_numdaplot_error() -> None:
	"""
	Check that ColumnNotFoundError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ColumnNotFoundError, NumdaplotError)


def test_column_not_found_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = ColumnNotFoundError(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_column_not_found_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = ColumnNotFoundError(COLUMN_NAME)

	assert error.column_name == COLUMN_NAME
