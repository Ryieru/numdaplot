"""
Settings of the CSV files a Table writes.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.measures.decimal_count import require_decimal_count
from numdaplot.tables.files.csv.csv_separator import DEFAULT_SEPARATOR, require_separator
from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class CsvWriteOptions:
	"""
	Settings of a CSV file written by ``Table.to_csv``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The character between two values of a row, ``","`` by default.
	encoding
		The text encoding of the file, UTF-8 by default.
	decimals
		The number of decimals written for every decimal column, 0 or more. Each value is rounded and keeps its
		zeros, such as ``1.50``, so the file no longer holds the exact values. When omitted, a decimal is written
		with every digit of its value.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidSeparatorError
		When the separator is not exactly one character.
	InvalidCountError
		When ``decimals`` is negative.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "sales.csv"
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5, 8.0])})
	>>> prices.to_csv(path, ndp.CsvWriteOptions(separator=";", decimals=2))
	>>> print(path.read_text())
	price
	1.50
	8.00
	<BLANKLINE>
	"""

	separator: str = DEFAULT_SEPARATOR
	encoding: Encoding = Encoding.UTF_8
	decimals: int | None = None

	def __post_init__(self) -> None:
		"""
		Check every setting: its type, a separator of exactly one character and ``decimals`` not negative.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidSeparatorError
			When the separator is not exactly one character.
		InvalidCountError
			When ``decimals`` is negative.
		"""
		require_field_types(self)

		require_separator(self.separator)
		require_decimal_count(self.decimals)
