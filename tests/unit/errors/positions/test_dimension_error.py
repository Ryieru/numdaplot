"""
Unit tests of DimensionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.positions.dimension_error import DimensionError

OPERATION = "An axis"
DIMENSION_COUNT = 1
EXPECTED_MESSAGE = "An axis does not apply to an Array of 1 dimension(s)."


def test_dimension_error_is_a_numdaplot_error() -> None:
	"""
	Check that DimensionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DimensionError, NumdaplotError)


def test_dimension_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = DimensionError(OPERATION, DIMENSION_COUNT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_dimension_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = DimensionError(OPERATION, DIMENSION_COUNT)

	assert error.operation == OPERATION
	assert error.dimension_count == DIMENSION_COUNT
