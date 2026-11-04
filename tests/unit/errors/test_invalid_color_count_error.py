"""
Unit tests of InvalidColorCountError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_color_count_error import InvalidColorCountError
from numdaplot.errors.numdaplot_error import NumdaplotError

COLOR_COUNT = 1
SERIES_COUNT = 2
EXPECTED_MESSAGE = "Expected one color per series, 2 series and 1 color(s) given."


def test_invalid_color_count_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidColorCountError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidColorCountError, NumdaplotError)


def test_invalid_color_count_error_message_states_both_counts() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColorCountError(COLOR_COUNT, SERIES_COUNT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_color_count_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColorCountError(COLOR_COUNT, SERIES_COUNT)

	assert error.color_count == COLOR_COUNT
	assert error.series_count == SERIES_COUNT
