"""
Unit tests of EmptyArrayError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.positions.empty_array_error import EmptyArrayError

STATISTIC_NAME = "Mean"
EXPECTED_MESSAGE = "Cannot compute Mean without any present value."


def test_empty_array_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyArrayError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(EmptyArrayError, NumdaplotError)


def test_empty_array_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = EmptyArrayError(STATISTIC_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_empty_array_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = EmptyArrayError(STATISTIC_NAME)

	assert error.statistic_name == STATISTIC_NAME
