"""
Unit tests of InvalidPositionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_position_error import InvalidPositionError
from numdaplot.errors.numdaplot_error import NumdaplotError

POSITION = 5
SIZE = 3
EXPECTED_MESSAGE = "Expected a whole position between -3 and 2, got 5."


def test_invalid_position_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidPositionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidPositionError, NumdaplotError)


def test_invalid_position_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidPositionError(POSITION, SIZE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_position_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidPositionError(POSITION, SIZE)

	assert error.position == POSITION
	assert error.size == SIZE
