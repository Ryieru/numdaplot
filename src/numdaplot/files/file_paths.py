"""
Paths of the files numdaplot reads and writes: Tables, and images of Plots and Figures.

.. versionadded:: 0.1.0
"""

from pathlib import Path

from numdaplot.errors.files.file_exists_error import FileExistsError
from numdaplot.errors.files.file_not_found_error import FileNotFoundError
from numdaplot.files.conflict import Conflict

type FilePath = str | Path
"""
The path of a file, as a text or a ``pathlib.Path``.

It is a name used by the documentation and the annotations, not an object to create: pass the value itself,
such as ``"sales.csv"`` or ``Path("data/sales.csv")``.

.. versionadded:: 0.1.0

Examples
--------
>>> from pathlib import Path
>>> from tempfile import TemporaryDirectory
>>> import numdaplot as ndp
>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
>>> sales = ndp.Table.from_arrays({"city": cities})
>>> with TemporaryDirectory() as folder:
... 	sales.to_csv(Path(folder) / "sales.csv")
... 	ndp.Table.from_csv(Path(folder) / "sales.csv").column("city").to_list()
['Paris', 'Lyon']
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
	>>> import numdaplot as ndp
	>>> from pathlib import Path
	>>> from numdaplot.files.file_paths import require_existing_file
	>>> try:
	... 	require_existing_file(Path("missing.csv"))
	... except ndp.FileNotFoundError as error:
	... 	print(error)
	No file found at missing.csv.
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
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> from numdaplot.files.file_paths import require_free_path
	>>> with tempfile.NamedTemporaryFile(suffix=".csv") as file:
	... 	path = Path(file.name)
	... 	require_free_path(path, ndp.Conflict.REPLACE)
	... 	try:
	... 		require_free_path(path, ndp.Conflict.ERROR)
	... 	except ndp.FileExistsError:
	... 		print("refused")
	refused
	"""
	file_exists = path.exists()
	refuses_existing_file = file_exists and on_conflict == Conflict.ERROR
	if refuses_existing_file:
		path_text = str(path)
		raise FileExistsError(path_text)
