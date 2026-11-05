"""
Unit tests of OutOfDomainError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.out_of_domain_error import OutOfDomainError

FUNCTION_NAME = "SquareRoot"
VALUE = -9
EXPECTED_MESSAGE = "SquareRoot is not defined for -9."


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
	error = OutOfDomainError("Remainder", 0, True)

	error_text = str(error)
	assert error_text == "Remainder is not defined for 0 between integers. Convert the values to FLOAT64 first."
