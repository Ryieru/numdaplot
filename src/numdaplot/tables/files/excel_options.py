"""
Settings of the Excel files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_sheet_name_error import InvalidSheetNameError
from numdaplot.settings.field_types import require_field_types

MAXIMUM_SHEET_LENGTH = 31
FORBIDDEN_SHEET_CHARACTERS = "[]:*?/\\"


@dataclass(frozen=True)
class ExcelOptions:
	r"""
	Settings of an Excel file, used by ``Table.from_excel`` and ``Table.to_excel``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		The name of the sheet. When omitted, the first sheet is read, and the written sheet is named ``"Sheet1"``.

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

	def __post_init__(self) -> None:
		"""
		Check that Excel accepts the sheet name.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidSheetNameError
			When the name is empty, longer than 31 characters, or holds a character Excel refuses.
		"""
		require_field_types(self)

		if self.sheet is None:
			return

		sheet_length = len(self.sheet)
		has_valid_length = 0 < sheet_length <= MAXIMUM_SHEET_LENGTH
		has_forbidden_character = any(character in FORBIDDEN_SHEET_CHARACTERS for character in self.sheet)
		is_valid = has_valid_length and not has_forbidden_character
		if not is_valid:
			raise InvalidSheetNameError(self.sheet)
