"""
Unit tests of the reading and writing of Parquet files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas
import pytest

from numdaplot.errors.missing_dependency_error import MissingDependencyError
from numdaplot.tables.files import parquet_file
from numdaplot.tables.files.parquet_file import read_parquet_file, write_parquet_file

FILE_NAME = "sales.parquet"
COUNTS = {"count": pandas.Series([1, None], dtype="Int64")}
EXPECTED_DTYPE_NAME = "Int64"
REQUIRE_PACKAGE_NAME = "require_package"


def refuse_package(package_name: str, extra_name: str) -> None:
	"""
	Fake package check that always finds the package missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	package_name
		The checked package.
	extra_name
		Its numdaplot extra.

	Raises
	------
	MissingDependencyError
		Always.
	"""
	raise MissingDependencyError(package_name, extra_name)


def test_parquet_file_keeps_the_type_of_its_columns(tmp_path: Path) -> None:
	"""
	Check that integers with a missing value are read back as nullable integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(COUNTS)

	write_parquet_file(frame, path)
	read_frame = read_parquet_file(path)

	count_column = read_frame["count"]
	dtype_name = str(count_column.dtype)
	assert dtype_name == EXPECTED_DTYPE_NAME


def test_read_parquet_file_names_the_missing_extra(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that reading without pyarrow raises MissingDependencyError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package check with one that always fails.
	tmp_path
		A temporary folder.
	"""
	monkeypatch.setattr(parquet_file, REQUIRE_PACKAGE_NAME, refuse_package)
	path = tmp_path / FILE_NAME

	with pytest.raises(MissingDependencyError):
		read_parquet_file(path)


def test_write_parquet_file_names_the_missing_extra(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that writing without pyarrow raises MissingDependencyError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package check with one that always fails.
	tmp_path
		A temporary folder.
	"""
	monkeypatch.setattr(parquet_file, REQUIRE_PACKAGE_NAME, refuse_package)
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(COUNTS)

	with pytest.raises(MissingDependencyError):
		write_parquet_file(frame, path)
