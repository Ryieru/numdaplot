"""
Unit tests of EmptyTextError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.rules.empty_text_error import EMPTY_TEXT_MESSAGE, EmptyTextError


def test_empty_text_error_is_a_numdaplot_error() -> None:
	"""
	Check that EmptyTextError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(EmptyTextError, NumdaplotError)


def test_empty_text_error_explains_that_a_value_is_expected() -> None:
	"""
	Check the message of the error.

	.. versionadded:: 0.1.0
	"""
	error = EmptyTextError()

	error_text = str(error)
	assert error_text == EMPTY_TEXT_MESSAGE
