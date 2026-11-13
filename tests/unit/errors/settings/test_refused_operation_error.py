"""
Unit tests of RefusedOperationError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError

OPERATION = "Brackets on an Array"
ALTERNATIVE = "take"
EXPECTED_MESSAGE = "Brackets on an Array is not available, use take instead."


def test_refused_operation_error_is_a_numdaplot_error() -> None:
	"""
	Check that RefusedOperationError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(RefusedOperationError, NumdaplotError)


def test_refused_operation_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = RefusedOperationError(OPERATION, ALTERNATIVE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_refused_operation_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = RefusedOperationError(OPERATION, ALTERNATIVE)

	assert error.operation == OPERATION
	assert error.alternative == ALTERNATIVE
