"""
Settings of the JSON files a Table writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.measures.decimal_count import require_decimal_count
from numdaplot.tables.files.json.json_layout import JsonLayout


@dataclass(frozen=True)
class JsonWriteOptions:
	"""
	Settings of a JSON file written by ``Table.to_json``.

	JSON files are always written in UTF-8.

	.. versionadded:: 0.1.0

	Parameters
	----------
	layout
		The layout of the rows, one list of objects by default.
	decimals
		The number of decimals written for every decimal column, 0 or more. Each value is rounded and keeps its
		zeros, such as ``1.50``, so the file no longer holds the exact values. When omitted, a decimal is written
		with every digit of its value.

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
	>>> path = Path(tempfile.mkdtemp()) / "sales.jsonl"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	>>> prices.to_json(path, ndp.JsonWriteOptions(layout=ndp.JsonLayout.LINES, decimals=2))
	>>> print(path.read_text())
	{"price":1.50}
	{"price":8.00}
	<BLANKLINE>
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

		require_decimal_count(self.decimals)
