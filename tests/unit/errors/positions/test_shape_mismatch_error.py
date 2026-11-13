"""
Unit tests of ShapeMismatchError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError

LEFT_DIMENSIONS = [3]
RIGHT_DIMENSIONS = [2, 2]
NUMPY_SHAPE = (2, 2)
EXPECTED_MESSAGE = "Expected matching shapes, got [3] and [2, 2]."


def test_shape_mismatch_error_is_a_numdaplot_error() -> None:
	"""
	Check that ShapeMismatchError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ShapeMismatchError, NumdaplotError)


def test_shape_mismatch_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = ShapeMismatchError(LEFT_DIMENSIONS, RIGHT_DIMENSIONS)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_shape_mismatch_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = ShapeMismatchError(LEFT_DIMENSIONS, RIGHT_DIMENSIONS)

	assert error.left_dimensions == LEFT_DIMENSIONS
	assert error.right_dimensions == RIGHT_DIMENSIONS


def test_shape_mismatch_error_writes_a_numpy_shape_as_a_list() -> None:
	"""
	Check that a numpy shape, which is a tuple, is kept and shown as a list.

	.. versionadded:: 0.1.0
	"""
	error = ShapeMismatchError(LEFT_DIMENSIONS, NUMPY_SHAPE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.right_dimensions == RIGHT_DIMENSIONS
