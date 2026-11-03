"""
Unit tests of InvalidFractionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_fraction_error import InvalidFractionError
from numdaplot.errors.numdaplot_error import NumdaplotError

REJECTED_FRACTION = 1.5
EXPECTED_MESSAGE = "Expected a fraction between 0 and 1, got 1.5."


def test_invalid_fraction_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidFractionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidFractionError, NumdaplotError)


def test_invalid_fraction_error_message_names_the_rejected_value() -> None:
	"""
	Check that the message states the rejected value.

	.. versionadded:: 0.1.0
	"""
	error = InvalidFractionError(REJECTED_FRACTION)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_fraction_error_keeps_the_rejected_value() -> None:
	"""
	Check that the rejected value is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = InvalidFractionError(REJECTED_FRACTION)

	assert error.value == REJECTED_FRACTION
