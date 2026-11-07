"""
Unit tests of the reading and writing of Excel files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas
import pytest

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.missing_dependency_error import MissingDependencyError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.tables.files import excel_file
from numdaplot.tables.files.excel_file import find_read_sheet, read_excel_file, write_excel_file
from numdaplot.tables.files.excel_read_options import ExcelReadOptions
from numdaplot.tables.files.excel_write_options import ExcelWriteOptions

FILE_NAME = "sales.xlsx"
SHEET_NAME = "Sales"
OTHER_SHEET_NAME = "Costs"
PRICES = {"price": [1.5, 8.0]}
COSTS = {"cost": [3.0]}
EXPECTED_PRICES = [1.5, 8.0]
EXPECTED_COSTS = [3.0]
DEFAULT_SHEET_NAMES = ["Sheet1"]
NUMBER_HEADER = {1: [1.5]}
EMPTY_FRAME = dict[str, list[float]]()
FIRST_SHEET = 0
REQUIRE_PACKAGE_NAME = "require_package"
PARIS_TIMES = (
	pandas.Series(pandas.to_datetime(["2026-07-01 10:30"])).astype("datetime64[ns]").dt.tz_localize("Europe/Paris")
)


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


def test_read_excel_file_reads_the_first_sheet_by_default(tmp_path: Path) -> None:
	"""
	Check that the first sheet is read when no sheet is named.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(PRICES)
	write_excel_file(frame, path, ExcelWriteOptions())

	read_frame = read_excel_file(path, ExcelReadOptions())

	price_column = read_frame["price"]
	prices = price_column.tolist()
	assert prices == EXPECTED_PRICES


def test_read_excel_file_reads_a_named_sheet(tmp_path: Path) -> None:
	"""
	Check that a named sheet is read by its name.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	cost_frame = pandas.DataFrame(COSTS)
	write_options = ExcelWriteOptions(sheet=OTHER_SHEET_NAME)
	options = ExcelReadOptions(sheet=OTHER_SHEET_NAME)
	write_excel_file(cost_frame, path, write_options)

	read_frame = read_excel_file(path, options)

	cost_column = read_frame["cost"]
	costs = cost_column.tolist()
	assert costs == EXPECTED_COSTS


def test_read_excel_file_rejects_a_number_as_column_name(tmp_path: Path) -> None:
	"""
	Check that a number in the first row raises InvalidColumnNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(NUMBER_HEADER)
	write_excel_file(frame, path, ExcelWriteOptions())

	with pytest.raises(InvalidColumnNameError):
		read_excel_file(path, ExcelReadOptions())


def test_read_excel_file_rejects_a_repeated_column_name(tmp_path: Path) -> None:
	"""
	Check that two cells of the first row with the same name raise DuplicateColumnError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(PRICES)
	repeated_frame = pandas.concat([frame, frame], axis="columns")
	write_excel_file(repeated_frame, path, ExcelWriteOptions())

	with pytest.raises(DuplicateColumnError):
		read_excel_file(path, ExcelReadOptions())


def test_read_excel_file_gives_no_column_for_an_empty_sheet(tmp_path: Path) -> None:
	"""
	Check that an empty sheet gives an empty DataFrame.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(EMPTY_FRAME)
	write_excel_file(frame, path, ExcelWriteOptions())

	read_frame = read_excel_file(path, ExcelReadOptions())

	assert read_frame.empty


def test_read_excel_file_names_the_missing_extra(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that reading without openpyxl raises MissingDependencyError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package check with one that always fails.
	tmp_path
		A temporary folder.
	"""
	monkeypatch.setattr(excel_file, REQUIRE_PACKAGE_NAME, refuse_package)
	path = tmp_path / FILE_NAME

	with pytest.raises(MissingDependencyError):
		read_excel_file(path, ExcelReadOptions())


def test_find_read_sheet_gives_the_first_sheet_without_name() -> None:
	"""
	Check that no name gives the position of the first sheet.

	.. versionadded:: 0.1.0
	"""
	sheet = find_read_sheet(ExcelReadOptions())

	assert sheet == FIRST_SHEET


def test_find_read_sheet_gives_the_named_sheet() -> None:
	"""
	Check that a name is given as it is.

	.. versionadded:: 0.1.0
	"""
	options = ExcelReadOptions(sheet=SHEET_NAME)

	sheet = find_read_sheet(options)

	assert sheet == SHEET_NAME


def test_write_excel_file_names_the_sheet_sheet1_by_default(tmp_path: Path) -> None:
	"""
	Check the name of the written sheet when none is given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(PRICES)

	write_excel_file(frame, path, ExcelWriteOptions())

	excel_book = pandas.ExcelFile(path)
	assert excel_book.sheet_names == DEFAULT_SHEET_NAMES


def test_write_excel_file_names_the_missing_extra(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
	"""
	Check that writing without openpyxl raises MissingDependencyError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the package check with one that always fails.
	tmp_path
		A temporary folder.
	"""
	monkeypatch.setattr(excel_file, REQUIRE_PACKAGE_NAME, refuse_package)
	path = tmp_path / FILE_NAME
	frame = pandas.DataFrame(PRICES)

	with pytest.raises(MissingDependencyError):
		write_excel_file(frame, path, ExcelWriteOptions())


def test_write_excel_file_rejects_a_datetime_column_with_a_time_zone(tmp_path: Path) -> None:
	"""
	Check that Excel files refuse zone columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder.
	"""
	path = tmp_path / FILE_NAME
	time_frame = pandas.DataFrame({"time": PARIS_TIMES})

	with pytest.raises(TimeZoneMismatchError):
		write_excel_file(time_frame, path, ExcelWriteOptions())
