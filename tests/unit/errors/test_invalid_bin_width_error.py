"""
Unit tests of InvalidBinWidthError.

.. versionadded:: 0.1.0
"""

from datetime import timedelta

from numdaplot.errors.invalid_bin_width_error import InvalidBinWidthError
from numdaplot.errors.numdaplot_error import NumdaplotError

WIDTH = -5.0
EXPECTED_MESSAGE = "Expected a bin width above 0, got -5.0."
LONG_DURATION = timedelta(days=2)
EXPECTED_DURATION_MESSAGE = "Expected a bin width above 0 and at most 1 day, got 2 days, 0:00:00."


def test_invalid_bin_width_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidBinWidthError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidBinWidthError, NumdaplotError)


def test_invalid_bin_width_error_message_states_the_rejected_width() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBinWidthError(WIDTH)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_bin_width_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBinWidthError(WIDTH)

	assert error.width == WIDTH


def test_invalid_bin_width_error_names_the_limit_of_a_duration() -> None:
	"""
	Check the message of a duration beyond a day.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBinWidthError(LONG_DURATION)

	message = str(error)
	assert message == EXPECTED_DURATION_MESSAGE
	assert error.width == LONG_DURATION
