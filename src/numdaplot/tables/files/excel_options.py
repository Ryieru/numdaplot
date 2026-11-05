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
		The name of the sheet. When omitted, the first sheet is read, and the written sheet is named ``"Sheet1"``.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.xlsx"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
	>>> prices.to_excel(path, ndp.ExcelOptions(sheet="Sales"))
	>>> ndp.Table.from_excel(path, ndp.ExcelOptions(sheet="Sales"))
	    price
	  FLOAT64
	0     1.5
	"""

	sheet: str | None = None
