"""
Unit tests of FileAccessError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.files.file_access_error import FileAccessError
from numdaplot.errors.numdaplot_error import NumdaplotError

OPERATION = "write to"
PATH = "sales.csv"
REASON = "permission denied"
EXPECTED_MESSAGE = "Cannot write to sales.csv: permission denied."


def test_file_access_error_is_a_numdaplot_error_and_an_os_error() -> None:
	"""
	Check that both kinds of except clause catch it.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(FileAccessError, NumdaplotError)
	assert issubclass(FileAccessError, OSError)


def test_file_access_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = FileAccessError(OPERATION, PATH, REASON)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_file_access_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = FileAccessError(OPERATION, PATH, REASON)

	assert error.operation == OPERATION
	assert error.path == PATH
	assert error.reason == REASON
