"""
Unit tests of InvalidCountError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.invalid_count_error import InvalidCountError

COUNT = 0
MINIMUM = 2
EXPECTED_MESSAGE = "Expected a count of at least 2, got 0."


def test_invalid_count_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidCountError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidCountError, NumdaplotError)


def test_invalid_count_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidCountError(COUNT, MINIMUM)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_count_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidCountError(COUNT, MINIMUM)

	assert error.count == COUNT
	assert error.minimum == MINIMUM
