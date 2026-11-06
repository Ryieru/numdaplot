"""
Functional tests of the errors of the file system when a Plot, a Figure or a Table uses a file.

.. versionadded:: 0.1.0
"""

import os
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

import numdaplot as ndp

READ_ONLY_MODE = 0o500
FULL_MODE = 0o700
NO_ACCESS_MODE = 0o000
READABLE_MODE = 0o600
TABLE = ndp.Table.from_arrays(
	{
		"day": ndp.Array.from_list([1.0, 2.0]),
		"price": ndp.Array.from_list([3.0, 4.0]),
	}
)
PLOT = ndp.Plot.line(TABLE, ndp.LineChart(x="day", y=["price"]))
FIGURE = ndp.Figure(ndp.Layout(rows=1, columns=1)).place(PLOT, ndp.Cell(row=0, column=0))
WRITERS = [
	pytest.param(PLOT.save, "chart.png", id="plot"),
	pytest.param(FIGURE.save, "chart.png", id="figure"),
	pytest.param(TABLE.to_csv, "sales.csv", id="csv"),
	pytest.param(TABLE.to_json, "sales.json", id="json"),
	pytest.param(TABLE.to_excel, "sales.xlsx", id="excel"),
	pytest.param(TABLE.to_parquet, "sales.parquet", id="parquet"),
	pytest.param(TABLE.to_stata, "sales.dta", id="stata"),
]
READERS = [
	pytest.param(ndp.Table.from_csv, "sales.csv", TABLE.to_csv, id="csv"),
	pytest.param(ndp.Table.from_json, "sales.json", TABLE.to_json, id="json"),
	pytest.param(ndp.Table.from_excel, "sales.xlsx", TABLE.to_excel, id="excel"),
	pytest.param(ndp.Table.from_parquet, "sales.parquet", TABLE.to_parquet, id="parquet"),
	pytest.param(ndp.Table.from_stata, "sales.dta", TABLE.to_stata, id="stata"),
]


@pytest.fixture
def read_only_folder(tmp_path: Path) -> Iterator[Path]:
	"""
	Give a folder that cannot be written, skipping the test for a user who can write anywhere.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.

	Yields
	------
	Path
		The read-only folder.
	"""
	folder = tmp_path / "read_only"
	folder.mkdir()
	folder.chmod(READ_ONLY_MODE)
	if os.access(folder, os.W_OK):
		pytest.skip("this user can write in a read-only folder")

	yield folder

	folder.chmod(FULL_MODE)


@pytest.mark.parametrize(("write", "file_name"), WRITERS)
def test_writing_into_a_missing_folder_names_the_folder(
	write: Callable[[Path], Any],
	file_name: str,
	tmp_path: Path,
) -> None:
	"""
	Check the error of each writer, and that no folder is created.

	.. versionadded:: 0.1.0

	Parameters
	----------
	write
		The function writing the file.
	file_name
		The name of the file.
	tmp_path
		A temporary folder.
	"""
	folder = tmp_path / "missing"
	path = folder / file_name

	with pytest.raises(ndp.FileAccessError) as error_info:
		write(path)

	error_text = str(error_info.value)
	assert error_text == f"Cannot write to {path}: the folder {folder} does not exist."
	assert not folder.exists()


@pytest.mark.parametrize(("write", "file_name"), WRITERS)
def test_writing_under_a_file_names_the_file(write: Callable[[Path], Any], file_name: str, tmp_path: Path) -> None:
	"""
	Check the error of each writer when the folder of the file is a file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	write
		The function writing the file.
	file_name
		The name of the file.
	tmp_path
		A temporary folder.
	"""
	blocking_file = tmp_path / "blocking.txt"
	blocking_file.touch()
	path = blocking_file / file_name

	with pytest.raises(ndp.FileAccessError) as error_info:
		write(path)

	error_text = str(error_info.value)
	assert error_text == f"Cannot write to {path}: the folder {blocking_file} is a file."


@pytest.mark.parametrize(("write", "file_name"), WRITERS)
def test_writing_without_permission_says_so(
	write: Callable[[Path], Any],
	file_name: str,
	read_only_folder: Path,
) -> None:
	"""
	Check the error of each writer in a folder that cannot be written.

	.. versionadded:: 0.1.0

	Parameters
	----------
	write
		The function writing the file.
	file_name
		The name of the file.
	read_only_folder
		A folder that cannot be written.
	"""
	path = read_only_folder / file_name

	with pytest.raises(ndp.FileAccessError) as error_info:
		write(path)

	error_text = str(error_info.value)
	assert error_text == f"Cannot write to {path}: permission denied."


@pytest.mark.parametrize(("read", "file_name", "write"), READERS)
def test_reading_without_permission_says_so(
	read: Callable[[Path], Any],
	file_name: str,
	write: Callable[[Path], Any],
	tmp_path: Path,
) -> None:
	"""
	Check the error of each reader on a file that cannot be read.

	.. versionadded:: 0.1.0

	Parameters
	----------
	read
		The function reading the file.
	file_name
		The name of the file.
	write
		The function writing the file first.
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / file_name
	write(path)
	path.chmod(NO_ACCESS_MODE)
	if os.access(path, os.R_OK):
		path.chmod(READABLE_MODE)
		pytest.skip("this user can read any file")

	with pytest.raises(ndp.FileAccessError) as error_info:
		read(path)

	path.chmod(READABLE_MODE)
	error_text = str(error_info.value)
	assert error_text == f"Cannot read {path}: permission denied."


def test_a_file_access_error_is_caught_as_both_errors(tmp_path: Path) -> None:
	"""
	Check that existing code catching an OSError keeps working.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / "missing" / "sales.csv"

	with pytest.raises(OSError):
		TABLE.to_csv(path)

	with pytest.raises(ndp.NumdaplotError):
		TABLE.to_csv(path)


def test_the_errors_of_a_missing_and_of_an_existing_file_keep_their_class(tmp_path: Path) -> None:
	"""
	Check that these two cases keep their own errors.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / "sales.csv"
	TABLE.to_csv(path)

	with pytest.raises(ndp.FileExistsError):
		TABLE.to_csv(path)

	with pytest.raises(ndp.FileNotFoundError):
		ndp.Table.from_csv(tmp_path / "missing.csv")
