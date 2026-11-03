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
	r"""
	UTF-8, the most common encoding. Default value.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "cities.csv"
	>>> _ = path.write_text("city\nB\u00e9ziers\n", encoding="utf-8")
	>>> cities = ndp.Table.from_csv(path, ndp.CsvOptions(encoding=ndp.Encoding.UTF_8))
	>>> cities.column("city").to_list() == ["B\u00e9ziers"]
	True
	"""

	UTF_8_BOM = "utf-8-sig"
	r"""
	UTF-8 starting with a byte order mark, as written by Excel when it saves a CSV file.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "cities.csv"
	>>> _ = path.write_text("city\nB\u00e9ziers\n", encoding="utf-8-sig")
	>>> cities = ndp.Table.from_csv(path, ndp.CsvOptions(encoding=ndp.Encoding.UTF_8_BOM))
	>>> cities.column("city").to_list() == ["B\u00e9ziers"]
	True
	"""

	LATIN_1 = "latin-1"
	r"""
	Latin-1 (ISO 8859-1), used by older software in Western Europe.

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
