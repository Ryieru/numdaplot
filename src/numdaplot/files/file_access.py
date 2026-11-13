"""
Errors of the file system while reading or writing a file.

.. versionadded:: 0.1.0
"""

from pathlib import Path

from numdaplot.errors.error_translation import ErrorTranslation
from numdaplot.errors.file_access_error import FileAccessError
from numdaplot.errors.numdaplot_error import NumdaplotError

READ_OPERATION = "read"
WRITE_OPERATION = "write to"
PERMISSION_REASON = "permission denied"
MISSING_FOLDER_REASON = "the folder {folder} does not exist"
FOLDER_IS_FILE_REASON = "the folder {folder} is a file"


class FileAccessErrors(ErrorTranslation):
	"""
	Context turning an error of the file system during a block into a ``FileAccessError``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operation
		What the block does: ``READ_OPERATION`` or ``WRITE_OPERATION``.
	path
		The path of the file.

	Examples
	--------
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.files.file_access import FileAccessErrors, WRITE_OPERATION
	>>> path = Path("missing_folder/sales.csv")
	>>> try:
	... 	with FileAccessErrors(WRITE_OPERATION, path):
	... 		path.write_text("sales")
	... except ndp.FileAccessError as error:
	... 	print(error)
	Cannot write to missing_folder/sales.csv: the folder missing_folder does not exist.
	"""

	def __init__(self, operation: str, path: Path) -> None:
		"""
		Keep the operation and the path of the block.

		.. versionadded:: 0.1.0

		Parameters
		----------
		operation
			What the block does: ``READ_OPERATION`` or ``WRITE_OPERATION``.
		path
			The path of the file.
		"""
		self.operation = operation
		self.path = path

	def translate_error(self, error: BaseException) -> None:
		"""
		Raise a ``FileAccessError`` for an error of the file system. Any other error goes on unchanged.

		.. versionadded:: 0.2.0

		Parameters
		----------
		error
			The error raised by the block.

		Raises
		------
		FileAccessError
			When the block raised an ``OSError`` that is not already an error of numdaplot.
		"""
		if not isinstance(error, OSError):
			return

		if isinstance(error, NumdaplotError):
			return

		reason = find_access_reason(self.path, error)
		path_text = str(self.path)
		raise FileAccessError(self.operation, path_text, reason) from error


def find_access_reason(path: Path, error: OSError) -> str:
	"""
	Return why the file system refused a file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file.
	error
		The error of the file system.

	Returns
	-------
	str
		A missing permission or a wrong folder in words, else what the system says.

	Examples
	--------
	>>> from pathlib import Path
	>>> from numdaplot.files.file_access import find_access_reason
	>>> find_access_reason(Path("missing_folder/sales.csv"), OSError("Disk is full"))
	'the folder missing_folder does not exist'
	>>> find_access_reason(Path("sales.csv"), OSError(28, "No space left on device"))
	'No space left on device'
	"""
	if isinstance(error, PermissionError):
		return PERMISSION_REASON

	folder = path.parent
	folder_exists = folder.exists()
	if not folder_exists:
		missing_folder_reason = MISSING_FOLDER_REASON.format(folder=folder)
		return missing_folder_reason

	folder_is_folder = folder.is_dir()
	if not folder_is_folder:
		folder_is_file_reason = FOLDER_IS_FILE_REASON.format(folder=folder)
		return folder_is_file_reason

	if error.strerror is not None:
		return error.strerror

	system_reason = str(error)

	return system_reason
