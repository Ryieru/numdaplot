r"""
Settings of the Excel files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.excel_sheet import require_sheet_name


@dataclass(frozen=True)
class ExcelReadOptions:
	r"""
	Settings of an Excel file read by ``Table.from_excel``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		The name of the sheet read, the first sheet when omitted.
	column_names
		Whether the column names are cleaned, ``ColumnNames.CLEANED`` by default: the spaces, tabs and line breaks at
		the start and the end of each name are removed. ``ColumnNames.KEPT`` keeps the names as written.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidSheetNameError
		When the name is empty, longer than 31 characters, or holds ``[ ] : * ? / \``, which Excel refuses.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "sales.xlsx"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
	>>> prices.to_excel(path, ndp.ExcelWriteOptions(sheet="Sales"))
	>>> ndp.Table.from_excel(path, ndp.ExcelReadOptions(sheet="Sales"))
	    price
	  FLOAT64
	0     1.5
	"""

	sheet: str | None = None
	column_names: ColumnNames = ColumnNames.CLEANED

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and that Excel accepts the sheet name.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidSheetNameError
			When the name is empty, longer than 31 characters, or holds a character Excel refuses.
		"""
		require_field_types(self)

		require_sheet_name(self.sheet)
