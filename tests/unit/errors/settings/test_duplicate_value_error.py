"""
Unit tests of DuplicateValueError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.settings.duplicate_value_error import DuplicateValueError

VALUE = 2
EXPECTED_MESSAGE = "The value 2 appears more than once."


def test_duplicate_value_error_is_a_numdaplot_error() -> None:
	"""
	Check that DuplicateValueError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(DuplicateValueError, NumdaplotError)


def test_duplicate_value_error_names_the_value() -> None:
	"""
	Check the message and the attribute.

	.. versionadded:: 0.1.0
	"""
	error = DuplicateValueError(VALUE)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE
	assert error.value == VALUE
