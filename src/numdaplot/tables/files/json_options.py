"""
Settings of the JSON files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.files.json_layout import JsonLayout


@dataclass(frozen=True)
class JsonOptions:
	"""
	Settings of a JSON file, used by ``Table.from_json`` and ``Table.to_json``.

	JSON files are always read and written in UTF-8.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layout
		The layout of the rows, one list of objects by default.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.json"
	>>> _ = path.write_text('[{"city": "Paris", "count": 2}]')
	>>> ndp.Table.from_json(path, ndp.JsonOptions())
	city count
	TEXT INT64
	0  Paris     2
	"""

	layout: JsonLayout = JsonLayout.RECORDS
