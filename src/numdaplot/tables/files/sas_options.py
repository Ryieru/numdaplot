"""
Settings of the SAS data files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class SasOptions:
	"""
	Settings of a SAS data file (``.sas7bdat``), used by ``Table.from_sas``.

	These files are read only.

	.. versionadded:: 0.1.0

	Parameters
	----------
	encoding
		The text encoding of the texts stored in the file, UTF-8 by default.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.SasOptions(encoding=ndp.Encoding.LATIN_1)
	SasOptions(encoding=<Encoding.LATIN_1: 'latin-1'>)
	"""

	encoding: Encoding = Encoding.UTF_8
