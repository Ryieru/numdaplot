"""
Unit tests of NotSingleValueError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.not_single_value_error import NotSingleValueError
from numdaplot.errors.numdaplot_error import NumdaplotError

VALUE_COUNT = 2
EXPECTED_MESSAGE = "Expected exactly one value, got 2."


def test_not_single_value_error_is_a_numdaplot_error() -> None:
	"""
	Check that NotSingleValueError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(NotSingleValueError, NumdaplotError)


def test_not_single_value_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = NotSingleValueError(VALUE_COUNT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_not_single_value_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = NotSingleValueError(VALUE_COUNT)

	assert error.value_count == VALUE_COUNT
