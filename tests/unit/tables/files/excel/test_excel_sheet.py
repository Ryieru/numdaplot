"""
Unit tests of the check of the name of an Excel sheet.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.tables.files.excel.excel_sheet import require_sheet_name

SHEET_NAME = "Sales"
LONGEST_SHEET_NAME = "A" * 31
TOO_LONG_SHEET_NAME = "A" * 32
REFUSED_SHEET_NAMES = ["", TOO_LONG_SHEET_NAME, "Sales/2026", "[Sales]", "Sales:2026"]


@pytest.mark.parametrize("sheet", [None, SHEET_NAME, LONGEST_SHEET_NAME])
def test_require_sheet_name_accepts_no_name_or_a_name_excel_accepts(sheet: str | None) -> None:
	"""
	Check that an omitted name, a usual name and a name of 31 characters raise nothing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		An accepted sheet name.
	"""
	require_sheet_name(sheet)


@pytest.mark.parametrize("sheet", REFUSED_SHEET_NAMES)
def test_require_sheet_name_rejects_a_name_excel_refuses(sheet: str) -> None:
	"""
	Check that an empty, too long or forbidden sheet name raises InvalidSheetNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		A sheet name Excel refuses.
	"""
	with pytest.raises(InvalidSheetNameError):
		require_sheet_name(sheet)
