"""
Unit tests of the time and duration cells of Excel files.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import time, timedelta
from pathlib import Path
from typing import Any, cast

import openpyxl
import pandas
import pytest

from numdaplot.tables.files.excel.excel_time_cells import find_text_columns, holds_only_time_cells, restore_time_columns
from numdaplot.tables.files.pandas_backend import NULLABLE_DTYPE_BACKEND

FILE_NAME = "hours.xlsx"
FIRST_SHEET = 0
NO_MISSING_SETTINGS = dict[str, object]()
HEADER = ["hrmn", "wait", "label"]
ROWS = [[time(15, 35), timedelta(hours=30), "a"], [None, None, None], [time(8, 5), timedelta(minutes=5), "b"]]
EXPECTED_TIMES = [time(15, 35), time(8, 5)]
EXPECTED_WAITS = [timedelta(hours=30), timedelta(minutes=5)]
EXPECTED_LABELS = ["a", pandas.NA, "b"]
MIXED_HEADER = ["hrmn"]
MIXED_ROWS = [[time(15, 35)], ["unknown"]]
EXPECTED_MIXED_TEXTS = ["15:35:00", "unknown"]
NUMBER_FRAME = pandas.DataFrame({"count": [1, 2]})
TEXT_FRAME = pandas.DataFrame({"city": pandas.Series(["Pau"], dtype="string"), "count": [1]})
EXPECTED_TEXT_NAMES = ["city"]
TIME_VALUES = pandas.Series([time(8), None], dtype=object)
DURATION_VALUES = pandas.Series([timedelta(hours=1), None], dtype=object)
MIXED_VALUES = pandas.Series([time(8), "unknown"], dtype=object)
EMPTY_VALUES = pandas.Series([None, None], dtype=object)


def write_sheet(path: Path, header: list[str], rows: Sequence[Sequence[object]]) -> None:
	"""
	Write an Excel file of one sheet, the header first, then each row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file written.
	header
		The column names.
	rows
		The cells of each row.
	"""
	book = openpyxl.Workbook()
	sheet = book.active
	assert sheet is not None
	sheet.append(header)

	for row in rows:
		row_cells = list(row)
		sheet.append(row_cells)

	book.save(path)


def read_nullable_frame(path: Path) -> pandas.DataFrame:
	"""
	Return the first sheet of an Excel file read with the types of pandas that accept missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an Excel file.

	Returns
	-------
	pandas.DataFrame
		The columns of the sheet.
	"""
	# The pandas stubs leave the types of the Excel engines unknown.
	excel_pandas = cast(Any, pandas)
	raw_frame = excel_pandas.read_excel(path, dtype_backend=NULLABLE_DTYPE_BACKEND)
	frame = cast(pandas.DataFrame, raw_frame)

	return frame


def read_present_values(column: pandas.Series) -> list[object]:
	"""
	Return the present values of a column, in order.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column.

	Returns
	-------
	list[object]
		The values that are not missing.
	"""
	present_column = column.dropna()
	present_values = present_column.tolist()

	return present_values


def test_restore_time_columns_reads_time_and_duration_cells_again(tmp_path: Path) -> None:
	"""
	Check that time and duration cells become Python values, a text column staying as read.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder given by pytest.
	"""
	path = tmp_path / FILE_NAME
	write_sheet(path, HEADER, ROWS)
	frame = read_nullable_frame(path)

	restored_frame = restore_time_columns(frame, path, FIRST_SHEET, NO_MISSING_SETTINGS)

	times = read_present_values(restored_frame["hrmn"])
	waits = read_present_values(restored_frame["wait"])
	label_column = restored_frame["label"]
	labels = label_column.tolist()
	assert times == EXPECTED_TIMES
	assert waits == EXPECTED_WAITS
	assert labels == EXPECTED_LABELS


def test_restore_time_columns_keeps_times_mixed_with_texts_as_texts(tmp_path: Path) -> None:
	"""
	Check that a column of time cells and texts stays a column of texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder given by pytest.
	"""
	path = tmp_path / FILE_NAME
	write_sheet(path, MIXED_HEADER, MIXED_ROWS)
	frame = read_nullable_frame(path)

	restored_frame = restore_time_columns(frame, path, FIRST_SHEET, NO_MISSING_SETTINGS)

	hour_column = restored_frame["hrmn"]
	hours = hour_column.tolist()
	assert hours == EXPECTED_MIXED_TEXTS


def test_restore_time_columns_keeps_a_sheet_without_texts(tmp_path: Path) -> None:
	"""
	Check that a sheet without text column is returned without reading the file again.

	.. versionadded:: 0.1.0

	Parameters
	----------
	tmp_path
		A temporary folder given by pytest.
	"""
	missing_path = tmp_path / FILE_NAME

	restored_frame = restore_time_columns(NUMBER_FRAME, missing_path, FIRST_SHEET, NO_MISSING_SETTINGS)

	assert restored_frame is NUMBER_FRAME


def test_find_text_columns_names_the_text_columns_only() -> None:
	"""
	Check that only the columns of texts are named.

	.. versionadded:: 0.1.0
	"""
	text_names = find_text_columns(TEXT_FRAME)

	assert text_names == EXPECTED_TEXT_NAMES


@pytest.mark.parametrize(
	("column", "expected_result"),
	[(TIME_VALUES, True), (DURATION_VALUES, True), (MIXED_VALUES, False), (EMPTY_VALUES, False)],
)
def test_holds_only_time_cells_needs_times_only_or_durations_only(column: pandas.Series, expected_result: bool) -> None:
	"""
	Check that times only and durations only are recognized, a mix with texts and an empty column are not.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of Python values.
	expected_result
		Whether it holds time cells only.
	"""
	holds_time_cells = holds_only_time_cells(column)

	assert holds_time_cells == expected_result
