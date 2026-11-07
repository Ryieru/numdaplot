r"""
Settings of the Stata files a Table reads.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.files.column_names import ColumnNames


@dataclass(frozen=True)
class StataReadOptions:
	r"""
	Settings of a Stata file (``.dta``) read by ``Table.from_stata``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		Whether the column names are cleaned, ``ColumnNames.CLEANED`` by default: the spaces, tabs and line breaks at
		the start and the end of each name are removed. ``ColumnNames.KEPT`` keeps the names as written.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> import tempfile
	>>> from pathlib import Path
	>>> import numdaplot as ndp
	>>> path = Path(tempfile.mkdtemp()) / "sales.dta"
	>>> ndp.Table.from_arrays({"price": ndp.Array.from_list([1.5])}).to_stata(path)
	>>> options = ndp.StataReadOptions(column_names=ndp.ColumnNames.KEPT)
	>>> ndp.Table.from_stata(path, options).column_names
	['price']
	"""

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
