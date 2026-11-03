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
	>>> ndp.XptOptions(encoding=ndp.Encoding.LATIN_1)
	XptOptions(encoding=<Encoding.LATIN_1: 'latin-1'>)
	"""

	encoding: Encoding = Encoding.UTF_8
