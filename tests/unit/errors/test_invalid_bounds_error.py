"""
Unit tests of InvalidBoundsError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.numdaplot_error import NumdaplotError

LOW_BOUND = "b"
HIGH_BOUND = "a"
EXPECTED_MESSAGE = "Expected comparable bounds with low <= high, got low='b' and high='a'."


def test_invalid_bounds_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidBoundsError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidBoundsError, NumdaplotError)


def test_invalid_bounds_error_message_shows_both_bounds_with_their_quotes() -> None:
	"""
	Check that the message shows both bounds in their Python form, so texts keep their quotes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBoundsError(LOW_BOUND, HIGH_BOUND)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_bounds_error_keeps_both_bounds() -> None:
	"""
	Check that both rejected bounds are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBoundsError(LOW_BOUND, HIGH_BOUND)

	assert error.low == LOW_BOUND
	assert error.high == HIGH_BOUND
