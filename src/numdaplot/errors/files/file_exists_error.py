"""
Error raised when a Table would overwrite an existing file.

.. versionadded:: 0.1.0
"""

import builtins

from numdaplot.errors.numdaplot_error import NumdaplotError

FILE_EXISTS_MESSAGE = "A file already exists at {path}, pass on_conflict=ndp.Conflict.REPLACE to overwrite it."


class FileExistsError(NumdaplotError, builtins.FileExistsError):
	"""
	Raised when a Table is written to a path where a file exists and ``on_conflict`` is ``Conflict.ERROR``.

	It is also a Python ``FileExistsError``, so code catching the Python error keeps working.

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
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "prices.csv"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])})
	>>> prices.to_csv(path)
	>>> try:
	... 	prices.to_csv(path)
	... except ndp.FileExistsError as error:
	... 	print(error)  # doctest: +ELLIPSIS
	A file already exists at .../prices.csv, pass on_conflict=ndp.Conflict.REPLACE to overwrite it.
	>>> prices.to_csv(path, on_conflict=ndp.Conflict.REPLACE)
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
		message = FILE_EXISTS_MESSAGE.format(path=path)
		super().__init__(message)

		self.path = path
