"""
Unit tests of the checks of file paths.

.. versionadded:: 0.1.0
"""

import builtins
from pathlib import Path

import pytest

from numdaplot.errors.file_exists_error import FileExistsError
from numdaplot.errors.file_not_found_error import FileNotFoundError
from numdaplot.files.conflict import Conflict
from numdaplot.files.file_paths import require_existing_file, require_free_path

FILE_NAME = "sales.csv"
FILE_CONTENT = "price\n1\n"


def test_require_existing_file_accepts_a_file(tmp_path: Path) -> None:
	"""
	Check that an existing file passes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(FILE_CONTENT)

	require_existing_file(path)


def test_require_existing_file_rejects_a_missing_file(tmp_path: Path) -> None:
	"""
	Check that a missing file raises the numdaplot FileNotFoundError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME

	with pytest.raises(FileNotFoundError):
		require_existing_file(path)


def test_require_existing_file_rejects_a_folder(tmp_path: Path) -> None:
	"""
	Check that a folder is not accepted as a file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	with pytest.raises(builtins.FileNotFoundError):
		require_existing_file(tmp_path)


def test_require_free_path_accepts_a_free_path(tmp_path: Path) -> None:
	"""
	Check that a path without file passes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME

	require_free_path(path, Conflict.ERROR)


def test_require_free_path_rejects_an_existing_file(tmp_path: Path) -> None:
	"""
	Check that an existing file raises FileExistsError with Conflict.ERROR.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(FILE_CONTENT)

	with pytest.raises(FileExistsError):
		require_free_path(path, Conflict.ERROR)


def test_require_free_path_accepts_an_existing_file_to_replace(tmp_path: Path) -> None:
	"""
	Check that an existing file passes with Conflict.REPLACE.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	path.write_text(FILE_CONTENT)

	require_free_path(path, Conflict.REPLACE)
