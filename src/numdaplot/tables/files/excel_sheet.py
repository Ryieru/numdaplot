r"""
Check of the name of an Excel sheet.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_sheet_name_error import InvalidSheetNameError

MAXIMUM_SHEET_LENGTH = 31
FORBIDDEN_SHEET_CHARACTERS = frozenset("[]:*?/\\")


def require_sheet_name(sheet: str | None) -> None:
	r"""
	Check that Excel accepts a sheet name, when it is given.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		The name of the sheet, or None for the default sheet.

	Raises
	------
	InvalidSheetNameError
		When the name is empty, longer than 31 characters, or holds ``[ ] : * ? / \``, which Excel refuses.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.excel_sheet import require_sheet_name
	>>> try:
	... 	require_sheet_name("Sales/2026")
	... except ndp.InvalidSheetNameError as error:
	... 	print(error)
	Expected a sheet name of 1 to 31 characters without [ ] : * ? / \, got 'Sales/2026'.
	"""
	if sheet is None:
		return

	sheet_length = len(sheet)
	has_valid_length = 0 < sheet_length <= MAXIMUM_SHEET_LENGTH
	sheet_characters = set(sheet)
	forbidden_characters = sheet_characters & FORBIDDEN_SHEET_CHARACTERS
	forbidden_count = len(forbidden_characters)
	has_forbidden_character = forbidden_count > 0
	is_valid = has_valid_length and not has_forbidden_character
	if not is_valid:
		raise InvalidSheetNameError(sheet)
