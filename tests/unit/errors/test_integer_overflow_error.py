"""
Unit tests of IntegerOverflowError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.integer_overflow_error import IntegerOverflowError
from numdaplot.errors.numdaplot_error import NumdaplotError

OPERATION_NAME = "*"
TYPE_NAME = "INT64"
EXPECTED_MESSAGE = (
	"The operation * gives values outside the range of INT64, from -9223372036854775808 to 9223372036854775807. "
	"Convert the values to FLOAT64 first, which keeps about 16 digits."
)
SMALL_TYPE_NAME = "UINT8"
EXPECTED_SMALL_MESSAGE = (
	"The operation * gives values outside the range of UINT8, from 0 to 255. Convert the values to INT64 first."
)


def test_integer_overflow_error_is_a_numdaplot_error() -> None:
	"""
	Check that IntegerOverflowError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(IntegerOverflowError, NumdaplotError)


def test_integer_overflow_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = IntegerOverflowError(OPERATION_NAME, TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_integer_overflow_error_advises_a_wider_integer_for_a_small_type() -> None:
	"""
	Check that a type narrower than 64 bits gets the advice of INT64, with its own range.

	.. versionadded:: 0.2.0
	"""
	error = IntegerOverflowError(OPERATION_NAME, SMALL_TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_SMALL_MESSAGE


def test_integer_overflow_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = IntegerOverflowError(OPERATION_NAME, TYPE_NAME)

	assert error.operation_name == OPERATION_NAME
	assert error.type_name == TYPE_NAME
