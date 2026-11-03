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
	"""
	Settings of a CSV file, used by ``Table.from_csv`` and ``Table.to_csv``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The character between two values of a row, ``,`` by default.
	encoding
		The text encoding of the file, UTF-8 by default.

	Raises
	------
	InvalidSeparatorError
		When the separator is not exactly one character.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.CsvOptions(separator=";", encoding=ndp.Encoding.LATIN_1)
	CsvOptions(separator=';', encoding=<Encoding.LATIN_1: 'latin-1'>)
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
