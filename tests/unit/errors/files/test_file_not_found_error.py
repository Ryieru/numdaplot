"""
Unit tests of FileNotFoundError.

.. versionadded:: 0.1.0
"""

import builtins

from numdaplot.errors.files.file_not_found_error import FileNotFoundError
from numdaplot.errors.numdaplot_error import NumdaplotError

PATH = "sales.csv"
EXPECTED_MESSAGE = "No file found at sales.csv."


def test_file_not_found_error_is_a_numdaplot_error() -> None:
	"""
	Check that FileNotFoundError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(FileNotFoundError, NumdaplotError)


def test_file_not_found_error_is_the_python_error_too() -> None:
	"""
	Check that FileNotFoundError is caught by the Python FileNotFoundError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(FileNotFoundError, builtins.FileNotFoundError)


def test_file_not_found_error_message_states_the_problem() -> None:
	"""
	Check the message built from the path.

	.. versionadded:: 0.1.0
	"""
	error = FileNotFoundError(PATH)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_file_not_found_error_keeps_its_path() -> None:
	"""
	Check that the path is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = FileNotFoundError(PATH)

	assert error.path == PATH
