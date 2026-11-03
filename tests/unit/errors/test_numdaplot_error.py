"""
Unit tests of NumdaplotError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

ERROR_MESSAGE = "Something went wrong."


def test_numdaplot_error_is_an_exception() -> None:
	"""
	Check that NumdaplotError can be raised and caught as any exception.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(NumdaplotError, Exception)


def test_numdaplot_error_keeps_its_message() -> None:
	"""
	Check that the message given to NumdaplotError is the text of the error.

	.. versionadded:: 0.1.0
	"""
	error = NumdaplotError(ERROR_MESSAGE)

	error_text = str(error)
	assert error_text == ERROR_MESSAGE
