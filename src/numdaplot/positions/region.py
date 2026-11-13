"""
A rectangular part of an Array or a Table, chosen by position.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.column_names import copy_column_names
from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.empty_region_error import EmptyRegionError
from numdaplot.positions.first import First
from numdaplot.positions.index import Index
from numdaplot.positions.last import Last
from numdaplot.positions.range import Range


@dataclass(frozen=True)
class Region:
	"""
	A rectangular part of an Array or a Table, chosen by position, used by ``take`` and ``replace``.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts ``First`` and ``Last`` for the rows and the columns.

	Parameters
	----------
	rows
		The rows to take: one ``Index``, a ``Range``, or the ``First`` or ``Last`` rows. Every row when omitted, but a
		Region needs rows, columns or both.
	columns
		The columns to take: one ``Index``, a ``Range``, the ``First`` or ``Last`` columns, or a list of column names
		for a Table. Every column when omitted. The region keeps its own copy of a list of names.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyRegionError
		When ``rows`` and ``columns`` are both omitted.
	EmptyListError
		When ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> grid = ndp.Array.from_list([[1, 2, 3], [4, 5, 6]])
	>>> grid.take(ndp.Region(rows=ndp.Index(0), columns=ndp.Range(start=1, stop=2)))
	Array([[2, 3]], dtype=INT64)
	"""

	rows: Index | Range | First | Last | None = None
	columns: Index | Range | First | Last | list[str] | None = None

	def __post_init__(self) -> None:
		"""
		Check the rows and the columns, and replace a list of column names with a copy only the region holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyRegionError
			When ``rows`` and ``columns`` are both omitted.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_field_types(self)

		has_no_position = self.rows is None and self.columns is None
		if has_no_position:
			raise EmptyRegionError()

		if not isinstance(self.columns, list):
			return

		columns_copy = copy_column_names(self.columns)
		object.__setattr__(self, "columns", columns_copy)
