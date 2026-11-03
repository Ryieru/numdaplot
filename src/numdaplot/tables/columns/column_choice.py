"""
Settings of the choice of the columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.column_names import require_unique_names

COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class ColumnChoice:
	"""
	Columns to keep or to drop, used by ``Table.choose_columns``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The names of the columns. The choice keeps its own copy of the list.
	mode
		``KEEP`` keeps only these columns, in the order of the list, which is the default.
		``DROP`` removes them.

	Raises
	------
	EmptyListError
		When ``columns`` is empty with ``KEEP``, which would keep nothing.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.ColumnChoice(columns=["comment"], mode=ndp.ColumnMode.DROP)
	ColumnChoice(columns=['comment'], mode=<ColumnMode.DROP: 2>)
	"""

	columns: list[str]
	mode: ColumnMode = ColumnMode.KEEP

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the choice holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyListError
			When ``columns`` is empty with ``KEEP``.
		DuplicateColumnError
			When a column name appears twice.
		"""
		keeps_nothing = self.columns == [] and self.mode == ColumnMode.KEEP
		if keeps_nothing:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_unique_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
