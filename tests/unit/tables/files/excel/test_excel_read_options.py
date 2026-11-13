"""
Unit tests of ExcelReadOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.files.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.excel.excel_read_options import ExcelReadOptions

SHEET_NAME = "Sales"
REFUSED_SHEET_NAME = "Sales/2026"


def test_excel_read_options_name_no_sheet_by_default() -> None:
	"""
	Check that no sheet is named by default.

	.. versionadded:: 0.1.0
	"""
	options = ExcelReadOptions()

	assert options.sheet is None


def test_excel_read_options_keep_their_sheet() -> None:
	"""
	Check that a given sheet is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	options = ExcelReadOptions(sheet=SHEET_NAME)

	assert options.sheet == SHEET_NAME


def test_excel_read_options_reject_a_sheet_name_excel_refuses() -> None:
	"""
	Check that the sheet name is checked at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidSheetNameError):
		ExcelReadOptions(sheet=REFUSED_SHEET_NAME)


def test_excel_read_options_clean_the_column_names_by_default() -> None:
	"""
	Check that the column names are cleaned by default.

	.. versionadded:: 0.1.0
	"""
	options = ExcelReadOptions()

	assert options.column_names == ColumnNames.CLEANED


def test_excel_read_options_read_the_default_missing_texts_when_omitted() -> None:
	"""
	Check that no list of missing texts is given by default.

	.. versionadded:: 0.1.0
	"""
	options = ExcelReadOptions()

	assert options.missing_texts is None


def test_excel_read_options_keep_their_own_copy_of_the_missing_texts() -> None:
	"""
	Check that changing the given list afterwards does not change the settings.

	.. versionadded:: 0.1.0
	"""
	missing_texts = ["N/A"]
	options = ExcelReadOptions(missing_texts=missing_texts)

	missing_texts.append("-")

	assert options.missing_texts == ["N/A"]
