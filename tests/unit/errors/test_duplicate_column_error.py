"""
Unit tests of DuplicateColumnError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.numdaplot_error import NumdaplotError

COLUMN_NAME = "price"
EXPECTED_MESSAGE = "The column name 'price' appears more than once."
ORIGINAL_NAMES = ["price", "price\n"]
EXPECTED_CLEANED_MESSAGE = (
	"The column names 'price' and 'price\\n' both become 'price' once cleaned. "
	"Use ColumnNames.KEPT to keep them as written."
)
ADVICE = "Rename one of them."
EXPECTED_ADVISED_MESSAGE = "The column name 'price' appears more than once. Rename one of them."


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


def test_duplicate_column_error_names_both_original_names() -> None:
	"""
	Check the message of two names that become the same once cleaned.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateColumnError(COLUMN_NAME, ORIGINAL_NAMES)

	error_text = str(error)
	assert error_text == EXPECTED_CLEANED_MESSAGE


def test_duplicate_column_error_keeps_the_original_names() -> None:
	"""
	Check that the names before cleaning are available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateColumnError(COLUMN_NAME, ORIGINAL_NAMES)

	assert error.original_names == ORIGINAL_NAMES


def test_duplicate_column_error_has_no_original_names_for_a_repeated_name() -> None:
	"""
	Check that a name written twice has no names before cleaning.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateColumnError(COLUMN_NAME)

	assert error.original_names is None


def test_duplicate_column_error_adds_its_advice_to_the_message() -> None:
	"""
	Check that the advice ends the message and is kept as an attribute.

	.. versionadded:: 0.2.0
	"""
	error = DuplicateColumnError(COLUMN_NAME, advice=ADVICE)

	error_text = str(error)
	assert error_text == EXPECTED_ADVISED_MESSAGE
	assert error.advice == ADVICE
