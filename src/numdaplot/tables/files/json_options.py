"""
Settings of the JSON files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.settings.field_types import require_field_types
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
	decimals
		The number of decimals written for every decimal column, 0 or more, ``Table.to_json`` only. Each value is
		rounded and keeps its zeros, such as ``1.50``, so the file no longer holds the exact values. When omitted, a
		decimal is written with every digit of its value.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidCountError
		When ``decimals`` is negative.

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
	decimals: int | None = None

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and that ``decimals`` is not negative.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidCountError
			When ``decimals`` is negative.
		"""
		require_field_types(self)

		if self.decimals is not None and self.decimals < 0:
			raise InvalidCountError(self.decimals, 0)
