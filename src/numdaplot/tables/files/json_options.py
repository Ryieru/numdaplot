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
	>>> import numdaplot as ndp
	>>> ndp.JsonOptions(layout=ndp.JsonLayout.LINES)
	JsonOptions(layout=<JsonLayout.LINES: 2>)
	"""

	layout: JsonLayout = JsonLayout.RECORDS
