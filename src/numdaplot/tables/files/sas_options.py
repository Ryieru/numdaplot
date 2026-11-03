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
	>>> try:
	... 	ndp.Table.from_sas("missing.sas7bdat", ndp.SasOptions(encoding=ndp.Encoding.LATIN_1))
	... except ndp.FileNotFoundError as error:
	... 	print(error)
	No file found at missing.sas7bdat.
	"""

	encoding: Encoding = Encoding.UTF_8
