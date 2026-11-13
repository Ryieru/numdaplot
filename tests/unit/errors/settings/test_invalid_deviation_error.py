"""
Unit tests of InvalidDeviationError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.invalid_deviation_error import InvalidDeviationError

DEVIATION = -1.5
EXPECTED_MESSAGE = "Expected a deviation of at least 0, got -1.5."


def test_invalid_deviation_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidDeviationError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidDeviationError, NumdaplotError)


def test_invalid_deviation_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidDeviationError(DEVIATION)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_deviation_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidDeviationError(DEVIATION)

	assert error.deviation == DEVIATION
