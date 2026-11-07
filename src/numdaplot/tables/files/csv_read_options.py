"""
Settings of the CSV files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.files.column_names import ColumnNames
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
	column_names
		Whether the column names are cleaned, ``ColumnNames.CLEANED`` by default: the spaces, tabs and line breaks at
		the start and the end of each name are removed. ``ColumnNames.KEPT`` keeps the names as written.
	missing_texts
		The texts read as missing values, compared with the whole value of each cell. When omitted, the texts pandas
		reads as missing: ``""``, ``"#N/A"``, ``"#N/A N/A"``, ``"#NA"``, ``"-1.#IND"``, ``"-1.#QNAN"``, ``"-NaN"``,
		``"-nan"``, ``"1.#IND"``, ``"1.#QNAN"``, ``"<NA>"``, ``"N/A"``, ``"NA"``, ``"NULL"``, ``"NaN"``, ``"None"``,
		``"n/a"``, ``"nan"`` and ``"null"``. A given list replaces them: ``[]`` reads no value as missing, not even
		an empty one, so a column of numbers with an empty value is read as texts.

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
	>>> _ = path.write_text("city;code\nParis;N/A\nLyon;\n")
	>>> ndp.Table.from_csv(path, ndp.CsvReadOptions(separator=";", missing_texts=[""]))
	    city code
	    TEXT TEXT
	0  Paris  N/A
	1   Lyon <NA>
	"""

	separator: str = DEFAULT_SEPARATOR
	encoding: Encoding = Encoding.UTF_8
	column_names: ColumnNames = ColumnNames.CLEANED
	missing_texts: list[str] | None = None

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

		if self.missing_texts is not None:
			missing_texts_copy = list(self.missing_texts)
			object.__setattr__(self, "missing_texts", missing_texts_copy)
