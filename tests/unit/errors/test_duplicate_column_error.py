"""
Unit tests of DuplicateColumnError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.numdaplot_error import NumdaplotError

COLUMN_NAME = "price"
EXPECTED_MESSAGE = "The column name 'price' appears more than once."


def test_duplicate_column_error_is_a_numdaplot_error() -> None:
	"""
	Check that DuplicateColumnError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DuplicateColumnError, NumdaplotError)


def test_duplicate_column_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateColumnError(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_duplicate_column_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateColumnError(COLUMN_NAME)

	assert error.column_name == COLUMN_NAME
