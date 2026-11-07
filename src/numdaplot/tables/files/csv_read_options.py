"""
Settings of the CSV files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.files.csv_separator import DEFAULT_SEPARATOR, require_separator
from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class CsvReadOptions:
	r"""
	Settings of a CSV file read by ``Table.from_csv``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The character between two values of a row, ``","`` by default.
	encoding
		The text encoding of the file, UTF-8 by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidSeparatorError
		When the separator is not exactly one character.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
	>>> _ = path.write_text("city;price\nParis;1.5\nLyon;8.0\n")
	>>> ndp.Table.from_csv(path, ndp.CsvReadOptions(separator=";"))
	    city   price
	    TEXT FLOAT64
	0  Paris     1.5
	1   Lyon     8.0
	"""

	separator: str = DEFAULT_SEPARATOR
	encoding: Encoding = Encoding.UTF_8

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and that the separator is exactly one character.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidSeparatorError
			When the separator is not exactly one character.
		"""
		require_field_types(self)

		require_separator(self.separator)
