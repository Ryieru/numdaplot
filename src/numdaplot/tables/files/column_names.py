r"""
Whether a Table cleans the column names it reads.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColumnNames(Enum):
	r"""
	Whether the column names read from a file or a pandas DataFrame are cleaned.

	Cleaning removes what ``str.strip`` removes at the start and the end of each name: spaces, tabs, line breaks and
	non-breaking spaces. The inside of a name is never changed.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "vehicles.csv"
	>>> _ = path.write_text('"id_vehicule\n";speed\n1;50\n')
	>>> ndp.Table.from_csv(path, ndp.CsvReadOptions(separator=";")).column_names
	['id_vehicule', 'speed']
	"""

	CLEANED = auto()
	r"""
	The spaces, tabs and line breaks at the start and the end of each name are removed. Default value.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "vehicles.csv"
	>>> _ = path.write_text('" id_vehicule\n";speed\n1;50\n')
	>>> options = ndp.CsvReadOptions(separator=";", column_names=ndp.ColumnNames.CLEANED)
	>>> ndp.Table.from_csv(path, options).column_names
	['id_vehicule', 'speed']
	"""

	KEPT = auto()
	r"""
	Each name is kept as written.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "vehicles.csv"
	>>> _ = path.write_text('" id_vehicule\n";speed\n1;50\n')
	>>> options = ndp.CsvReadOptions(separator=";", column_names=ndp.ColumnNames.KEPT)
	>>> ndp.Table.from_csv(path, options).column_names
	[' id_vehicule\n', 'speed']
	"""
