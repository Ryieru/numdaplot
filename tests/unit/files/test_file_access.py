"""
Unit tests of the errors of the file system while reading or writing a file.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pytest

from numdaplot.errors.file_access_error import FileAccessError
from numdaplot.errors.file_exists_error import FileExistsError as NumdaplotFileExistsError
from numdaplot.files.file_access import (
	READ_OPERATION,
	WRITE_OPERATION,
	FileAccessErrors,
	find_access_reason,
)

SYSTEM_REASON = "No space left on device"
SYSTEM_ERROR_NUMBER = 28
PATH_TEXT = "sales.csv"


def test_file_access_errors_turns_an_os_error_into_a_file_access_error(tmp_path: Path) -> None:
	"""
	Check the error raised, which keeps the error of the system as its cause.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / PATH_TEXT
	system_error = OSError(SYSTEM_ERROR_NUMBER, SYSTEM_REASON)

	with pytest.raises(FileAccessError) as error_info, FileAccessErrors(READ_OPERATION, path):
		raise system_error

	assert error_info.value.reason == SYSTEM_REASON
	assert error_info.value.__cause__ is system_error


def test_file_access_errors_leaves_other_errors(tmp_path: Path) -> None:
	"""
	Check that an error of the file content goes on unchanged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	with pytest.raises(ValueError), FileAccessErrors(READ_OPERATION, tmp_path):
		raise ValueError(PATH_TEXT)


def test_file_access_errors_leaves_the_errors_of_numdaplot(tmp_path: Path) -> None:
	"""
	Check that an error of numdaplot that is also an OSError keeps its class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	with pytest.raises(NumdaplotFileExistsError), FileAccessErrors(WRITE_OPERATION, tmp_path):
		raise NumdaplotFileExistsError(PATH_TEXT)


def test_file_access_errors_does_nothing_without_error(tmp_path: Path) -> None:
	"""
	Check that a block without error is not disturbed.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	with FileAccessErrors(WRITE_OPERATION, tmp_path):
		result = 1

	assert result == 1


def test_find_access_reason_names_a_missing_permission(tmp_path: Path) -> None:
	"""
	Check the reason of a PermissionError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	reason = find_access_reason(tmp_path / PATH_TEXT, PermissionError())

	assert reason == "permission denied"


def test_find_access_reason_names_a_missing_folder(tmp_path: Path) -> None:
	"""
	Check the reason of a folder that does not exist.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	folder = tmp_path / "missing"

	reason = find_access_reason(folder / PATH_TEXT, OSError())

	assert reason == f"the folder {folder} does not exist"


def test_find_access_reason_names_a_folder_that_is_a_file(tmp_path: Path) -> None:
	"""
	Check the reason of a parent that is a file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	blocking_file = tmp_path / "blocking.txt"
	blocking_file.touch()

	reason = find_access_reason(blocking_file / PATH_TEXT, OSError())

	assert reason == f"the folder {blocking_file} is a file"


def test_find_access_reason_gives_what_the_system_says(tmp_path: Path) -> None:
	"""
	Check the reason of any other error of the system.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	reason = find_access_reason(tmp_path / PATH_TEXT, OSError(SYSTEM_ERROR_NUMBER, SYSTEM_REASON))

	assert reason == SYSTEM_REASON


def test_find_access_reason_reads_an_error_without_system_text(tmp_path: Path) -> None:
	"""
	Check the reason of an error holding only a text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	reason = find_access_reason(tmp_path / PATH_TEXT, OSError(SYSTEM_REASON))

	assert reason == SYSTEM_REASON
