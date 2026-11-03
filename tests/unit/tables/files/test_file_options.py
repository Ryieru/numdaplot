"""
Unit tests of JsonOptions, ExcelOptions, SasOptions and XptOptions.

.. versionadded:: 0.1.0
"""

from numdaplot.tables.files.encoding import Encoding
from numdaplot.tables.files.excel_options import ExcelOptions
from numdaplot.tables.files.json_layout import JsonLayout
from numdaplot.tables.files.json_options import JsonOptions
from numdaplot.tables.files.sas_options import SasOptions
from numdaplot.tables.files.xpt_options import XptOptions

SHEET_NAME = "Sales"


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
