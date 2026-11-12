"""
Unit tests of UnmatchedValueError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unmatched_value_error import UnmatchedValueError

VALUE = 2
EXPECTED_MESSAGE = (
	"The value 2 has no ValueChange. Add one, or give others=Unmatched.MISSING to make it missing, or "
	"others=Unmatched.KEEP to keep it."
)
EXPECTED_BRACKETS_MESSAGE = (
	"The value 2 is in no bracket. Open the first or the last bracket, or give others=Unmatched.MISSING to make it "
	"missing."
)
BRACKETS_NAME = "Brackets"
COLUMN_NAME = "sex"
OTHER_COLUMN_NAME = "age"
EXPECTED_COLUMN_MESSAGE = (
	"The value 2 of the column 'sex' has no ValueChange. Add one, or give others=Unmatched.MISSING to make it "
	"missing, or others=Unmatched.KEEP to keep it."
)


def test_unmatched_value_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnmatchedValueError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnmatchedValueError, NumdaplotError)


def test_unmatched_value_error_names_the_value() -> None:
	"""
	Check the message and the attribute.

	.. versionadded:: 0.1.0
	"""
	error = UnmatchedValueError(VALUE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.value == VALUE


def test_unmatched_value_error_advises_brackets_for_brackets() -> None:
	"""
	Check the message and the attribute of a value in no bracket.

	.. versionadded:: 0.1.0
	"""
	error = UnmatchedValueError(VALUE, BRACKETS_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_BRACKETS_MESSAGE
	assert error.setting_name == BRACKETS_NAME


def test_unmatched_value_error_names_the_column_of_the_value() -> None:
	"""
	Check that name_column adds the column to the message and keeps it as an attribute.

	.. versionadded:: 0.2.0
	"""
	error = UnmatchedValueError(VALUE)

	error.name_column(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_COLUMN_MESSAGE
	assert error.column_name == COLUMN_NAME


def test_unmatched_value_error_keeps_the_first_column_named() -> None:
	"""
	Check that a second name_column leaves the first column in the message.

	.. versionadded:: 0.2.0
	"""
	error = UnmatchedValueError(VALUE)
	error.name_column(COLUMN_NAME)

	error.name_column(OTHER_COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_COLUMN_MESSAGE
