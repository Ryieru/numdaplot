"""
Time and duration cells of an Excel file, which pandas reads as texts.

.. versionadded:: 0.1.0
"""

from pathlib import Path
from typing import Any, cast

import pandas
from pandas.api.types import infer_dtype

PYTHON_OBJECT_DTYPE = object
TIME_KINDS = frozenset({"time", "timedelta"})


def restore_time_columns(
	frame: pandas.DataFrame, path: Path, sheet: str | int, missing_settings: dict[str, Any]
) -> pandas.DataFrame:
	"""
	Return the columns of a sheet with the columns of time or duration cells read again as Python values.

	The types of pandas that accept missing values write a time or a duration cell as a text. Only the text columns
	are read again, as Python values: a column of times of day only, or of durations only, keeps them, and becomes a
	``TIME`` or a ``DURATION`` column. The other columns are kept as read.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the sheet, read with the types of pandas that accept missing values.
	path
		The path of the Excel file.
	sheet
		The name or the position of the sheet.
	missing_settings
		The settings of pandas reading the missing values, the same as for ``frame``.

	Returns
	-------
	pandas.DataFrame
		The same columns, a column of times or durations holding Python values.

	Examples
	--------
	>>> import tempfile
	>>> from datetime import time
	>>> from pathlib import Path
	>>> import openpyxl
	>>> import pandas
	>>> from numdaplot.tables.files.excel_time_cells import restore_time_columns
	>>> path = Path(tempfile.mkdtemp()) / "hours.xlsx"
	>>> book = openpyxl.Workbook()
	>>> book.active.append(["hrmn"])
	>>> book.active.append([time(15, 35)])
	>>> book.save(path)
	>>> frame = pandas.read_excel(path, dtype_backend="numpy_nullable")
	>>> restore_time_columns(frame, path, 0, {})["hrmn"].tolist()
	[datetime.time(15, 35)]
	"""
	text_names = find_text_columns(frame)
	if text_names == []:
		return frame

	# The pandas stubs leave the types of the Excel engines unknown.
	excel_pandas = cast(Any, pandas)
	raw_object_frame = excel_pandas.read_excel(
		path, sheet_name=sheet, dtype=PYTHON_OBJECT_DTYPE, usecols=text_names, **missing_settings
	)
	object_frame = cast(pandas.DataFrame, raw_object_frame)
	restored_frame = frame.copy()

	for text_name in text_names:
		object_column = object_frame[text_name]
		holds_time_cells = holds_only_time_cells(object_column)
		if holds_time_cells:
			restored_frame[text_name] = object_column

	return restored_frame


def find_text_columns(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the names of the text columns of a sheet read with the types of pandas that accept missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a sheet.

	Returns
	-------
	list[str]
		The names of the columns of texts, in their order.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.excel_time_cells import find_text_columns
	>>> frame = pandas.DataFrame({"city": pandas.Series(["Pau"], dtype="string"), "count": [1]})
	>>> find_text_columns(frame)
	['city']
	"""
	text_names = list[str]()

	for column_name, column in frame.items():
		if isinstance(column.dtype, pandas.StringDtype):
			text_names.append(str(column_name))

	return text_names


def holds_only_time_cells(column: pandas.Series) -> bool:
	"""
	Return whether a column of Python values holds times of day only, or durations only, besides missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column read as Python values.

	Returns
	-------
	bool
		True for ``datetime.time`` values only or ``datetime.timedelta`` values only, False for a mix with texts or
		an empty column.

	Examples
	--------
	>>> from datetime import time
	>>> import pandas
	>>> from numdaplot.tables.files.excel_time_cells import holds_only_time_cells
	>>> holds_only_time_cells(pandas.Series([time(8), None], dtype=object))
	True
	>>> holds_only_time_cells(pandas.Series([time(8), "unknown"], dtype=object))
	False
	"""
	inferred_kind = infer_dtype(column, skipna=True)
	is_time_kind = inferred_kind in TIME_KINDS

	return is_time_kind
