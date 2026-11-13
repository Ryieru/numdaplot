"""
Unit tests of FileExistsError.

.. versionadded:: 0.1.0
"""

import builtins

from numdaplot.errors.files.file_exists_error import FileExistsError
from numdaplot.errors.numdaplot_error import NumdaplotError

PATH = "sales.csv"
EXPECTED_MESSAGE = "A file already exists at sales.csv, pass on_conflict=ndp.Conflict.REPLACE to overwrite it."


def test_file_exists_error_is_a_numdaplot_error() -> None:
	"""
	Check that FileExistsError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(FileExistsError, NumdaplotError)


def test_file_exists_error_is_the_python_error_too() -> None:
	"""
	Check that FileExistsError is caught by the Python FileExistsError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(FileExistsError, builtins.FileExistsError)


def test_file_exists_error_message_states_the_problem() -> None:
	"""
	Check the message built from the path.

	.. versionadded:: 0.1.0
	"""
	error = FileExistsError(PATH)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_file_exists_error_keeps_its_path() -> None:
	"""
	Check that the path is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = FileExistsError(PATH)

	assert error.path == PATH
