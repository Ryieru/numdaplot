"""
Text encodings of the files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from enum import Enum


class Encoding(Enum):
	r"""
	Text encoding of a file, used by ``CsvOptions``, ``SasOptions`` and ``XptOptions``.

	The value of each member is the name Python gives to the encoding.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "cities.csv"
	>>> _ = path.write_text("city\nB\u00e9ziers\n", encoding="latin-1")
	>>> cities = ndp.Table.from_csv(path, ndp.CsvOptions(encoding=ndp.Encoding.LATIN_1))
	>>> cities.column("city").to_list() == ["B\u00e9ziers"]
	True
	"""

	UTF_8 = "utf-8"
	"""UTF-8, the most common encoding. Default value."""

	UTF_8_BOM = "utf-8-sig"
	"""UTF-8 starting with a byte order mark, as written by Excel when it saves a CSV file."""

	LATIN_1 = "latin-1"
	"""Latin-1 (ISO 8859-1), used by older software in Western Europe."""
