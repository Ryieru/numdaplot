"""
Unit tests of InvalidBaseError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_base_error import InvalidBaseError
from numdaplot.errors.numdaplot_error import NumdaplotError

BASE = 1
EXPECTED_MESSAGE = "Expected a logarithm base greater than 0 and different from 1, got 1."


def test_invalid_base_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidBaseError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidBaseError, NumdaplotError)


def test_invalid_base_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBaseError(BASE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_base_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBaseError(BASE)

	assert error.base == BASE
