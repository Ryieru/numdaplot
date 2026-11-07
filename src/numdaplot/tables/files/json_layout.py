"""
Layouts of the rows of a JSON file.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class JsonLayout(Enum):
	"""
	Layout of the rows of a JSON file, used by ``JsonReadOptions`` and ``JsonWriteOptions``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.jsonl"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	>>> prices.to_json(path, ndp.JsonWriteOptions(layout=ndp.JsonLayout.LINES))
	>>> print(path.read_text())
	{"price":1.5}
	{"price":8.0}
	"""

	RECORDS = auto()
	"""
	One list holding one object per row: ``[{"city": "Paris"}, {"city": "Lyon"}]``. Default value.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "prices.json"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	>>> prices.to_json(path, ndp.JsonWriteOptions(layout=ndp.JsonLayout.RECORDS))
	>>> print(path.read_text())
	[{"price":1.5},{"price":8.0}]
	"""

	LINES = auto()
	"""
	One object per line, without enclosing list, also called JSON Lines.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "prices.json"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	>>> prices.to_json(path, ndp.JsonWriteOptions(layout=ndp.JsonLayout.LINES))
	>>> print(path.read_text())
	{"price":1.5}
	{"price":8.0}
	"""
