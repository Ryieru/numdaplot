"""
Unit tests of InvalidShapeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_shape_error import InvalidShapeError
from numdaplot.errors.numdaplot_error import NumdaplotError

DIMENSIONS = [3, -1]
EXPECTED_MESSAGE = "Expected at least one dimension and no negative dimension, got [3, -1]."


def test_invalid_shape_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidShapeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidShapeError, NumdaplotError)


def test_invalid_shape_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidShapeError(DIMENSIONS)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_shape_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidShapeError(DIMENSIONS)

	assert error.dimensions == DIMENSIONS
