"""
Settings of the Excel files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExcelOptions:
	"""
	Settings of an Excel file, used by ``Table.from_excel`` and ``Table.to_excel``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		The name of the sheet. When omitted, the first sheet is read, and the written sheet is named ``Sheet1``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.ExcelOptions(sheet="Sales")
	ExcelOptions(sheet='Sales')
	"""

	sheet: str | None = None
