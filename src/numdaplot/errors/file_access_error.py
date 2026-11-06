"""
Error raised when the file system refuses to read or to write a file.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

FILE_ACCESS_MESSAGE = "Cannot {operation} {path}: {reason}."


class FileAccessError(NumdaplotError, OSError):
	"""
	Raised when a file cannot be read or written: missing folder, missing permission, full disk and so on.

	It is also a Python ``OSError``. A missing file and an existing file have their own errors,
	``FileNotFoundError`` and ``FileExistsError``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		What was attempted: ``"read"`` or ``"write to"``.
	path
		The path of the file.
	reason
		Why it failed.

	Attributes
	----------
	operation
		What was attempted: ``"read"`` or ``"write to"``.
	path
		The path of the file.
	reason
		Why it failed.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
	>>> try:
	... 	prices.to_csv("missing_folder/prices.csv")
	... except ndp.FileAccessError as error:
	... 	print(error)
	Cannot write to missing_folder/prices.csv: the folder missing_folder does not exist.
	"""

	def __init__(self, operation: str, path: str, reason: str) -> None:
		"""
		Build the error message from the operation, the path and the reason.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			What was attempted: ``"read"`` or ``"write to"``.
		path
			The path of the file.
		reason
			Why it failed.
		"""
		message = FILE_ACCESS_MESSAGE.format(operation=operation, path=path, reason=reason)
		super().__init__(message)

		self.operation = operation
		self.path = path
		self.reason = reason
