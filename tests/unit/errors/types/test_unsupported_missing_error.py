"""
Unit tests of UnsupportedMissingError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.types.unsupported_missing_error import UnsupportedMissingError

TYPE_NAME = "INT64"
BOOL_TYPE_NAME = "BOOL"
COLUMN_NAME = "age"
EXPECTED_MESSAGE = "INT64 values cannot be missing in an Array. Remove them, or give dtype=ndp.Type.FLOAT64."
EXPECTED_BOOL_MESSAGE = "BOOL values cannot be missing in an Array. Remove them."
EXPECTED_COLUMN_MESSAGE = (
	"The column 'age' has missing values, which an INT64 Array cannot hold. "
	"Remove them with drop_missing, or convert the column to FLOAT64."
)
EXPECTED_BOOL_COLUMN_MESSAGE = (
	"The column 'age' has missing values, which a BOOL Array cannot hold. Remove them with drop_missing."
)

MAPPING_ADVICE = "Give decimal new values, such as 10.0, which can be missing."
EXPECTED_MAPPING_MESSAGE = "INT64 values cannot be missing in an Array. " + MAPPING_ADVICE


def test_unsupported_missing_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedMissingError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedMissingError, NumdaplotError)


def test_unsupported_missing_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_missing_error_gives_no_conversion_for_booleans() -> None:
	"""
	Check that booleans, which cannot become decimals, are only advised to remove the missing values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(BOOL_TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_BOOL_MESSAGE


def test_unsupported_missing_error_names_the_column_and_its_conversion() -> None:
	"""
	Check the message of an integer column.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(TYPE_NAME, COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_COLUMN_MESSAGE


def test_unsupported_missing_error_names_the_column_without_conversion_for_booleans() -> None:
	"""
	Check the message of a boolean column.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(BOOL_TYPE_NAME, COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_BOOL_COLUMN_MESSAGE


def test_unsupported_missing_error_keeps_the_column_name() -> None:
	"""
	Check that the column name is available as an attribute, and None without column.

	.. versionadded:: 0.1.0
	"""
	column_error = UnsupportedMissingError(TYPE_NAME, COLUMN_NAME)
	list_error = UnsupportedMissingError(TYPE_NAME)

	assert column_error.column_name == COLUMN_NAME
	assert list_error.column_name is None


def test_unsupported_missing_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(TYPE_NAME)

	assert error.type_name == TYPE_NAME


def test_unsupported_missing_error_takes_the_advice_of_an_operation() -> None:
	"""
	Check that a given advice replaces the advice of from_list.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError("INT64", advice=MAPPING_ADVICE)

	error_text = str(error)
	assert error_text == EXPECTED_MAPPING_MESSAGE
