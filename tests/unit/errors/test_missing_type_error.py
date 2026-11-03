"""
Unit tests of MissingTypeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.missing_type_error import MissingTypeError
from numdaplot.errors.numdaplot_error import NumdaplotError

EXPECTED_MESSAGE = "Cannot guess the type of an Array without any present value, give dtype."


def test_missing_type_error_is_a_numdaplot_error() -> None:
	"""
	Check that MissingTypeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(MissingTypeError, NumdaplotError)


def test_missing_type_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = MissingTypeError()

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
