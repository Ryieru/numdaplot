"""
Unit tests of IncompatibleTypesError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.numdaplot_error import NumdaplotError

OPERATION = "+"
TYPE_NAMES = ["INT64", "TEXT"]
EXPECTED_MESSAGE = "Cannot apply + to INT64 and TEXT."


def test_incompatible_types_error_is_a_numdaplot_error() -> None:
	"""
	Check that IncompatibleTypesError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(IncompatibleTypesError, NumdaplotError)


def test_incompatible_types_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleTypesError(OPERATION, TYPE_NAMES)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_incompatible_types_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleTypesError(OPERATION, TYPE_NAMES)

	assert error.operation == OPERATION
	assert error.type_names == TYPE_NAMES


def test_incompatible_types_error_has_no_column_by_default() -> None:
	"""
	Check that a new error names no column.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleTypesError("+", ["INT64", "TEXT"])

	assert error.column_name is None


def test_name_column_names_the_first_type_of_the_message() -> None:
	"""
	Check the message once a column is named.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleTypesError("Greater", ["DATETIME", "INT64"])

	error.name_column("day")

	assert str(error) == "Cannot apply Greater to the DATETIME column 'day' and INT64."
	assert error.column_name == "day"


def test_name_column_keeps_the_first_name() -> None:
	"""
	Check that a named column does not change.

	.. versionadded:: 0.1.0
	"""
	error = IncompatibleTypesError("Mean", ["TEXT"])
	error.name_column("zone")

	error.name_column("other")

	assert str(error) == "Cannot apply Mean to the TEXT column 'zone'."
