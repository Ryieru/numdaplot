"""
Settings of the CSV files a Table reads and writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_separator_error import InvalidSeparatorError
from numdaplot.tables.files.encoding import Encoding

DEFAULT_SEPARATOR = ","
SEPARATOR_LENGTH = 1


@dataclass(frozen=True)
class CsvOptions:
	r"""
	Settings of a CSV file, used by ``Table.from_csv`` and ``Table.to_csv``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The character between two values of a row, ``","`` by default.
	encoding
		The text encoding of the file, UTF-8 by default.

	Raises
	------
	InvalidSeparatorError
		When the separator is not exactly one character.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> folder = Path(tempfile.mkdtemp())
	>>> path = folder / "sales.csv"
	>>> _ = path.write_text("city;price\nParis;1.5\nLyon;8.0\n")
	>>> ndp.Table.from_csv(path, ndp.CsvOptions(separator=";"))
	    city   price
	    TEXT FLOAT64
	0  Paris     1.5
	1   Lyon     8.0
	"""

	separator: str = DEFAULT_SEPARATOR
	encoding: Encoding = Encoding.UTF_8

	def __post_init__(self) -> None:
		"""
		Check that the separator is exactly one character.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSeparatorError
			When the separator is not exactly one character.
		"""
		separator_length = len(self.separator)
		if separator_length != SEPARATOR_LENGTH:
			raise InvalidSeparatorError(self.separator)
