"""
Settings of the SAS transport (XPT) files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.files.column_names import ColumnNames
from numdaplot.tables.files.encoding import Encoding


@dataclass(frozen=True)
class XptReadOptions:
	"""
	Settings of a SAS transport (XPT) file (``.xpt``) read by ``Table.from_xpt``.

	These files are read only.

	The example reads
	[paxraw_d_short.xpt](https://github.com/Ryieru/numdaplot/blob/main/tests/data/paxraw_d_short.xpt),
	a SAS transport file of 100 rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	encoding
		The text encoding of the texts stored in the file, UTF-8 by default.
	column_names
		Whether the column names are cleaned, ``ColumnNames.CLEANED`` by default: the spaces, tabs and line breaks at
		the start and the end of each name are removed. ``ColumnNames.KEPT`` keeps the names as written.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> latin_1 = ndp.XptReadOptions(encoding=ndp.Encoding.LATIN_1)
	>>> activity = ndp.Table.from_xpt("paxraw_d_short.xpt", latin_1)
	>>> activity.row_count
	100
	>>> activity.column_names
	['SEQN', 'PAXSTAT', 'PAXCAL', 'PAXDAY', 'PAXN', 'PAXHOUR', 'PAXMINUT', 'PAXINTEN', 'PAXSTEP']
	"""

	encoding: Encoding = Encoding.UTF_8
	column_names: ColumnNames = ColumnNames.CLEANED

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)
