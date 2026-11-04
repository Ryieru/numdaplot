"""
Reading and writing Stata files.

.. versionadded:: 0.1.0
"""

from pathlib import Path

import pandas

from numdaplot.tables.frames.time_zones import require_no_time_zone

STATA_OPERATION = "A Stata file"


def read_stata_file(path: Path) -> pandas.DataFrame:
	"""
	Return the columns of a Stata file (``.dta``).

	.. versionadded:: 0.1.0

	Parameters
	----------
	path
		The path of an existing Stata file.

	Returns
	-------
	pandas.DataFrame
		The columns as pandas reads them.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> from numdaplot.tables.files.stata_file import read_stata_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.dta"
	>>> pandas.DataFrame({"price": [1.5]}).to_stata(path, write_index=False)
	>>> read_stata_file(path)
	   price
	0    1.5
	"""
	frame = pandas.read_stata(path)

	return frame


def write_stata_file(frame: pandas.DataFrame, path: Path) -> None:
	"""
	Write the columns of a Table in a Stata file (``.dta``).

	Stata stores integers and booleans holding missing values as decimals, and a missing text
	as an empty text. Column names that Stata refuses, such as names with spaces, are changed
	by pandas with a warning.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	path
		The path of the file, replaced when it exists.

	Raises
	------
	TimeZoneMismatchError
		When a column holds datetimes with a time zone, which Stata files cannot store.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import pandas
	>>> from numdaplot.tables.files.stata_file import write_stata_file
	>>> path = Path(tempfile.mkdtemp()) / "sales.dta"
	>>> write_stata_file(pandas.DataFrame({"price": [1.5]}), path)
	>>> path.exists()
	True
	"""
	require_no_time_zone(frame, STATA_OPERATION)
	frame.to_stata(path, write_index=False)
