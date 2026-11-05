"""
Error raised when an Excel sheet name is not accepted by Excel.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SHEET_NAME_MESSAGE = "Expected a sheet name of 1 to 31 characters without [ ] : * ? / \\, got {sheet!r}."


class InvalidSheetNameError(NumdaplotError):
	r"""
	Raised when the sheet of ``ExcelOptions`` is empty, longer than 31 characters, or holds ``[ ] : * ? / \``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sheet
		The rejected sheet name.

	Attributes
	----------
	sheet
		The rejected sheet name.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ExcelOptions(sheet="Sales/2026")
	... except ndp.InvalidSheetNameError as error:
	... 	print(error)
	Expected a sheet name of 1 to 31 characters without [ ] : * ? / \, got 'Sales/2026'.
	"""

	def __init__(self, sheet: str) -> None:
		"""
		Build the error message from the sheet name.

		.. versionadded:: 0.1.0

		Parameters
		----------
		sheet
			The rejected sheet name.
		"""
		message = INVALID_SHEET_NAME_MESSAGE.format(sheet=sheet)
		super().__init__(message)

		self.sheet = sheet
