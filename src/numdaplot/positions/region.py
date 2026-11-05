"""
A rectangular part of an Array or a Table, chosen by position.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_region_error import EmptyRegionError
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range


@dataclass(frozen=True)
class Region:
	"""
	A rectangular part of an Array or a Table, chosen by position, used by ``take`` and ``replace``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		The rows to take: one ``Index`` or a ``Range``. Every row when omitted, but a Region needs rows,
		columns or both.
	columns
		The columns to take: one ``Index``, a ``Range``, or a list of column names for a Table.
		Every column when omitted. The region keeps its own copy of a list of names.

	Raises
	------
	EmptyRegionError
		When ``rows`` and ``columns`` are both omitted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> grid = ndp.Array.from_list([[1, 2, 3], [4, 5, 6]])
	>>> grid.take(ndp.Region(rows=ndp.Index(0), columns=ndp.Range(start=1, stop=2)))
	Array([[2, 3]], dtype=INT64)
	"""

	rows: Index | Range | None = None
	columns: Index | Range | list[str] | None = None

	def __post_init__(self) -> None:
		"""
		Check that rows or columns are chosen, and replace a list of column names with a copy only the region holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyRegionError
			When ``rows`` and ``columns`` are both omitted.
		"""
		has_no_position = self.rows is None and self.columns is None
		if has_no_position:
			raise EmptyRegionError()

		if not isinstance(self.columns, list):
			return

		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
