"""
Unit tests of ColumnNotFoundError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError

COLUMN_NAME = "prise"
EXPECTED_MESSAGE = "No column is named 'prise'."
TABLE_NAME = "the other Table"
EXPECTED_TABLE_MESSAGE = "No column of the other Table is named 'prise'."


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


def test_column_not_found_error_names_the_table_searched() -> None:
	"""
	Check the message and the attribute when the searched Table is given.

	.. versionadded:: 0.1.0
	"""
	error = ColumnNotFoundError(COLUMN_NAME, TABLE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_TABLE_MESSAGE
	assert error.table_name == TABLE_NAME


def test_column_not_found_error_has_no_table_by_default() -> None:
	"""
	Check that the searched Table is None when omitted.

	.. versionadded:: 0.1.0
	"""
	error = ColumnNotFoundError(COLUMN_NAME)

	assert error.table_name is None
