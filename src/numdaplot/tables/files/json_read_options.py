"""
Settings of the JSON files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.json_layout import JsonLayout


@dataclass(frozen=True)
class JsonReadOptions:
	r"""
	Settings of a JSON file read by ``Table.from_json``.

	JSON files are always read in UTF-8.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layout
		The layout of the rows, one list of objects by default.
	column_names
		Whether the column names are cleaned, ``ColumnNames.CLEANED`` by default: the spaces, tabs and line breaks at
		the start and the end of each name are removed. ``ColumnNames.KEPT`` keeps the names as written.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "sales.jsonl"
	>>> _ = path.write_text('{"city": "Paris", "count": 2}\n{"city": "Lyon", "count": 5}\n')
	>>> ndp.Table.from_json(path, ndp.JsonReadOptions(layout=ndp.JsonLayout.LINES))
	    city count
	    TEXT INT64
	0  Paris     2
	1   Lyon     5
	"""

	layout: JsonLayout = JsonLayout.RECORDS
	column_names: ColumnNames = ColumnNames.CLEANED

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
