"""
Paths of the files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from pathlib import Path

from numdaplot.errors.file_exists_error import FileExistsError
from numdaplot.errors.file_not_found_error import FileNotFoundError
from numdaplot.tables.conflict import Conflict

type FilePath = str | Path
"""The path of a file, as a text or a ``pathlib.Path``.

.. versionadded:: 0.1.0
"""


def require_existing_file(path: Path) -> None:
	"""
	Check that a file exists at a path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file to read.

	Raises
	------
	FileNotFoundError
		When there is no file at the path, the numdaplot error that is also the Python one.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> from numdaplot.tables.files.file_paths import require_existing_file
	>>> with tempfile.NamedTemporaryFile() as file:
	... 	require_existing_file(Path(file.name))
	"""
	is_file = path.is_file()
	if not is_file:
		path_text = str(path)
		raise FileNotFoundError(path_text)


def require_free_path(path: Path, on_conflict: Conflict) -> None:
	"""
	Check that a file can be written at a path.

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of the file to write.
	on_conflict
		``ERROR`` refuses to overwrite an existing file, ``REPLACE`` allows it.

	Raises
	------
	FileExistsError
		When a file exists at the path and ``on_conflict`` is ``ERROR``.

	Examples
	--------
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.file_paths import require_free_path
	>>> require_free_path(Path("not-written-yet.csv"), ndp.Conflict.ERROR)
	"""
	file_exists = path.exists()
	refuses_existing_file = file_exists and on_conflict == Conflict.ERROR
	if refuses_existing_file:
		path_text = str(path)
		raise FileExistsError(path_text)
