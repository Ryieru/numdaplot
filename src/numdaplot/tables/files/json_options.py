"""
Settings of the JSON files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.files.json_layout import JsonLayout


@dataclass(frozen=True)
class JsonOptions:
	r"""
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
	>>> path = folder / "sales.jsonl"
	>>> _ = path.write_text('{"city": "Paris", "count": 2}\n{"city": "Lyon", "count": 5}\n')
	>>> ndp.Table.from_json(path, ndp.JsonOptions(layout=ndp.JsonLayout.LINES))
	    city count
	    TEXT INT64
	0  Paris     2
	1   Lyon     5
	"""

	layout: JsonLayout = JsonLayout.RECORDS
