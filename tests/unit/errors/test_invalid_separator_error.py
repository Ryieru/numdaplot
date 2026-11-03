"""
Unit tests of InvalidSeparatorError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.errors.numdaplot_error import NumdaplotError

SEPARATOR = ";;"
EXPECTED_MESSAGE = "Expected a separator of exactly one character, got ';;'."


def test_invalid_separator_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidSeparatorError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidSeparatorError, NumdaplotError)


def test_invalid_separator_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSeparatorError(SEPARATOR)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_separator_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSeparatorError(SEPARATOR)

	assert error.separator == SEPARATOR
