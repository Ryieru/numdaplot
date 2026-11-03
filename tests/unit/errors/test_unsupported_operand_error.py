"""
Unit tests of UnsupportedOperandError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError

TYPE_NAME = "list"
EXPECTED_MESSAGE = "Expected an Array or a single value, got list."


def test_unsupported_operand_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedOperandError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedOperandError, NumdaplotError)


def test_unsupported_operand_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedOperandError(TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_operand_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedOperandError(TYPE_NAME)

	assert error.type_name == TYPE_NAME
