"""
Unit tests of JsonOptions, ExcelOptions, SasOptions and XptOptions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.excel_options import ExcelOptions
from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_options import JsonOptions
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.xpt_options import XptOptions

SHEET_NAME = "Sales"
LONGEST_SHEET_NAME = "A" * 31
TOO_LONG_SHEET_NAME = "A" * 32


def test_json_options_use_one_list_of_records_by_default() -> None:
	"""
	Check the default layout.

	.. versionadded:: 0.1.0
	"""
	options = JsonOptions()

	assert options.layout == JsonLayout.RECORDS


def test_excel_options_read_the_first_sheet_by_default() -> None:
	"""
	Check that no sheet is named by default.

	.. versionadded:: 0.1.0
	"""
	options = ExcelOptions()

	assert options.sheet is None


def test_excel_options_keep_their_sheet() -> None:
	"""
	Check that a given sheet is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	options = ExcelOptions(sheet=SHEET_NAME)

	assert options.sheet == SHEET_NAME


def test_sas_and_xpt_options_use_utf_8_by_default() -> None:
	"""
	Check the default encoding of SAS data and SAS transport files.

	.. versionadded:: 0.1.0
	"""
	sas_options = SasOptions()
	xpt_options = XptOptions()

	assert sas_options.encoding == Encoding.UTF_8
	assert xpt_options.encoding == Encoding.UTF_8


@pytest.mark.parametrize("sheet", ["", TOO_LONG_SHEET_NAME, "Sales/2026", "[Sales]", "Sales:2026"])
def test_excel_options_reject_a_sheet_name_excel_refuses(sheet: str) -> None:
	"""
	Check that an empty, too long or forbidden sheet name raises InvalidSheetNameError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		A sheet name Excel refuses.
	"""
	with pytest.raises(InvalidSheetNameError):
		ExcelOptions(sheet=sheet)


def test_excel_options_accept_a_name_of_thirty_one_characters() -> None:
	"""
	Check that the longest name Excel accepts passes.

	.. versionadded:: 0.1.0
	"""
	options = ExcelOptions(sheet=LONGEST_SHEET_NAME)

	assert options.sheet == LONGEST_SHEET_NAME
