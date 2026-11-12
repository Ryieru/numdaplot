"""
Unit tests of OutOfDomainError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.out_of_domain_error import OutOfDomainError

FUNCTION_NAME = "SquareRoot"
VALUE = -9
EXPECTED_MESSAGE = "SquareRoot is not defined for -9."
COLUMN_NAME = "score"
OTHER_COLUMN_NAME = "grade"
EXPECTED_COLUMN_MESSAGE = "SquareRoot is not defined for -9 in the column 'score'."
REMAINDER_NAME = "Remainder"
EXPECTED_BETWEEN_INTEGERS_MESSAGE = (
	"Remainder is not defined for 0 between integers. Convert the values to FLOAT64 first."
)
EXPECTED_BETWEEN_INTEGERS_COLUMN_MESSAGE = (
	"Remainder is not defined for 0 between integers in the column 'score'. Convert the values to FLOAT64 first."
)


def test_out_of_domain_error_is_a_numdaplot_error() -> None:
	"""
	Check that OutOfDomainError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(OutOfDomainError, NumdaplotError)


def test_out_of_domain_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = OutOfDomainError(FUNCTION_NAME, VALUE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_out_of_domain_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = OutOfDomainError(FUNCTION_NAME, VALUE)

	assert error.function_name == FUNCTION_NAME
	assert error.value == VALUE


def test_out_of_domain_error_gives_the_conversion_between_integers() -> None:
	"""
	Check the message of a value that decimals would accept.

	.. versionadded:: 0.1.0
	"""
	error = OutOfDomainError(REMAINDER_NAME, 0, True)

	error_text = str(error)
	assert error_text == EXPECTED_BETWEEN_INTEGERS_MESSAGE


def test_out_of_domain_error_names_the_column_of_the_value() -> None:
	"""
	Check that name_column adds the column to the message and keeps it as an attribute.

	.. versionadded:: 0.2.0
	"""
	error = OutOfDomainError(FUNCTION_NAME, VALUE)

	error.name_column(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_COLUMN_MESSAGE
	assert error.column_name == COLUMN_NAME


def test_out_of_domain_error_keeps_the_first_column_named() -> None:
	"""
	Check that a second name_column leaves the first column in the message.

	.. versionadded:: 0.2.0
	"""
	error = OutOfDomainError(FUNCTION_NAME, VALUE)
	error.name_column(COLUMN_NAME)

	error.name_column(OTHER_COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_COLUMN_MESSAGE


def test_out_of_domain_error_names_the_column_before_the_conversion_advice() -> None:
	"""
	Check that the column comes before the advice to convert integers.

	.. versionadded:: 0.2.0
	"""
	error = OutOfDomainError(REMAINDER_NAME, 0, True)

	error.name_column(COLUMN_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_BETWEEN_INTEGERS_COLUMN_MESSAGE
