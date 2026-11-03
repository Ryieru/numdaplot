"""
Settings of the SAS transport (XPT) files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class XptOptions:
	"""
	Settings of a SAS transport (XPT) file (``.xpt``), used by ``Table.from_xpt``.

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
	... 	ndp.Table.from_xpt("missing.xpt", ndp.XptOptions(encoding=ndp.Encoding.LATIN_1))
	... except ndp.FileNotFoundError as error:
	... 	print(error)
	No file found at missing.xpt.
	"""

	encoding: Encoding = Encoding.UTF_8
