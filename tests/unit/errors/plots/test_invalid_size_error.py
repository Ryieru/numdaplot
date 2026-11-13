"""
Unit tests of InvalidSizeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.invalid_size_error import InvalidSizeError

WIDTH = 0
HEIGHT = 4.8
EXPECTED_MESSAGE = "Expected a positive width and height, got 0 and 4.8."


def test_invalid_size_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidSizeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidSizeError, NumdaplotError)


def test_invalid_size_error_message_states_the_width_and_the_height() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSizeError(WIDTH, HEIGHT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_size_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidSizeError(WIDTH, HEIGHT)

	assert error.width == WIDTH
	assert error.height == HEIGHT
