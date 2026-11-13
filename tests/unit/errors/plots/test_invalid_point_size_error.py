"""
Unit tests of InvalidPointSizeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.invalid_point_size_error import InvalidPointSizeError

POINT_SIZE = -1.0
EXPECTED_MESSAGE = "Expected a point size above 0, got -1.0."


def test_invalid_point_size_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidPointSizeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidPointSizeError, NumdaplotError)


def test_invalid_point_size_error_message_states_the_problem() -> None:
	"""
	Check the message built from the size.

	.. versionadded:: 0.1.0
	"""
	error = InvalidPointSizeError(POINT_SIZE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_point_size_error_keeps_the_size() -> None:
	"""
	Check that the size is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = InvalidPointSizeError(POINT_SIZE)

	assert error.point_size == POINT_SIZE
