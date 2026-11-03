"""
Error raised when a file to read does not exist.

.. versionadded:: 0.1.0
"""

import builtins

from numdaplot.errors.numdaplot_error import NumdaplotError

FILE_NOT_FOUND_MESSAGE = "No file found at {path}."


class FileNotFoundError(NumdaplotError, builtins.FileNotFoundError):
	"""
	Raised when a Table is read from a path where there is no file.

	It is also a Python ``FileNotFoundError``, so code catching the Python error keeps working.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file, as given.

	Attributes
	----------
	path
		The path of the file, as given.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Table.from_csv("missing.csv")
	... except ndp.FileNotFoundError as error:
	... 	print(error)
	No file found at missing.csv.
	"""

	def __init__(self, path: str) -> None:
		"""
		Build the error message from the path.

		.. versionadded:: 0.1.0

		Parameters
		----------
		path
			The path of the file, as given.
		"""
		message = FILE_NOT_FOUND_MESSAGE.format(path=path)
		super().__init__(message)

		self.path = path
