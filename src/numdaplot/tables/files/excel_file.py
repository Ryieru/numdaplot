"""
Reading and writing Excel files.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any, cast

import pandas

from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.files.excel_read_options import ExcelReadOptions
from numdaplot.tables.files.excel_write_options import ExcelWriteOptions
from numdaplot.tables.files.missing_texts import find_missing_settings
from numdaplot.tables.files.optional_package import require_package
from numdaplot.tables.files.pandas_backend import NULLABLE_DTYPE_BACKEND
from numdaplot.tables.frames.time_zones import require_no_time_zone

EXCEL_PACKAGE = "openpyxl"
EXCEL_EXTRA = "excel"
FIRST_SHEET = 0
DEFAULT_SHEET_NAME = "Sheet1"
HEADER_ROW_COUNT = 1
NO_MISSING_TEXTS = list[str]()
EXCEL_OPERATION = "An Excel file"


def read_excel_file(path: Path, options: ExcelReadOptions) -> pandas.DataFrame:
	"""
	Return the columns of a sheet of an Excel file whose first row holds the column names.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing Excel file.
	options
		The sheet to read, the first one when omitted, and the texts read as missing.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them, empty for an empty sheet.

	Raises
	------
	MissingDependencyError
		When ``openpyxl`` is not installed.
	TimeZoneMismatchError
		When a column holds datetimes with a time zone, which Excel files cannot store.
	InvalidColumnNameError
		When a cell of the first row is empty or is not a text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.excel_file import read_excel_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.xlsx"
	>>> pandas.DataFrame({"price": [1.5]}).to_excel(path, index=False)
	>>> read_excel_file(path, ndp.ExcelReadOptions())
	   price
	0    1.5
	"""
	require_package(EXCEL_PACKAGE, EXCEL_EXTRA)
	sheet = find_read_sheet(options)
	# The pandas stubs leave the types of the Excel engines unknown.
	excel_pandas = cast(Any, pandas)
	# A column name is never a missing value, so the first row is read without any missing text.
	header_settings = find_missing_settings(NO_MISSING_TEXTS)
	raw_header_frame = excel_pandas.read_excel(
		path, sheet_name=sheet, header=None, nrows=HEADER_ROW_COUNT, **header_settings
	)
	header_frame = cast(pandas.DataFrame, raw_header_frame)
	if header_frame.empty:
		empty_frame = pandas.DataFrame()
		return empty_frame

	header_row = header_frame.iloc[0]
	header = header_row.tolist()
	require_column_names(header)
	missing_settings = find_missing_settings(options.missing_texts)
	raw_frame = excel_pandas.read_excel(
		path, sheet_name=sheet, dtype_backend=NULLABLE_DTYPE_BACKEND, **missing_settings
	)
	frame = cast(pandas.DataFrame, raw_frame)

	return frame


def find_read_sheet(options: ExcelReadOptions) -> str | int:
	"""
	Return the sheet pandas reads: its name, or the position of the first sheet.

	.. versionadded:: 0.1.0

	Parameters
	----------
	options
		The settings of the Excel file.

	Returns
	-------
	str or int
		The name of the sheet, or 0 when no sheet is named.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.excel_file import find_read_sheet
	>>> find_read_sheet(ndp.ExcelReadOptions())
	0
	"""
	if options.sheet is None:
		return FIRST_SHEET

	return options.sheet


def write_excel_file(frame: pandas.DataFrame, path: Path, options: ExcelWriteOptions) -> None:
	"""
	Write the columns of a Table in a sheet of an Excel file, column names on the first row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.
	options
		The name of the sheet, ``"Sheet1"`` when omitted.

	Raises
	------
	MissingDependencyError
		When ``openpyxl`` is not installed.
	TimeZoneMismatchError
		When a column holds datetimes with a time zone, which Excel files cannot store.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.excel_file import write_excel_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.xlsx"
	>>> write_excel_file(pandas.DataFrame({"price": [1.5]}), path, ndp.ExcelWriteOptions(sheet="Sales"))
	>>> pandas.ExcelFile(path).sheet_names
	['Sales']
	"""
	require_no_time_zone(frame, EXCEL_OPERATION)
	require_package(EXCEL_PACKAGE, EXCEL_EXTRA)
	sheet_name = DEFAULT_SHEET_NAME
	if options.sheet is not None:
		sheet_name = options.sheet

	# The pandas stubs leave the types of the Excel engines unknown.
	excel_frame = cast(Any, frame)
	excel_frame.to_excel(path, sheet_name=sheet_name, index=False)
