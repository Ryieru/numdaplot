"""
Settings of the removal of duplicated rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.duplicates.keep import Keep

COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class Deduplication:
	"""
	Which rows count as duplicates and which one is kept, used by ``Table.drop_duplicates``.

	Two missing values are equal when comparing rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The names of the columns compared, every column when omitted.
		The deduplication keeps its own copy of the list.
	keep
		The row kept in each group of duplicates, the first one by default.

	Raises
	------
	EmptyListError
		When ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Deduplication(columns=["email"], keep=ndp.Keep.LAST)
	Deduplication(columns=['email'], keep=<Keep.LAST: 2>)
	"""

	columns: list[str] | None = None
	keep: Keep = Keep.FIRST

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the deduplication holds.

		.. versionadded:: 0.1.0

		Raises
		------
		EmptyListError
			When ``columns`` is an empty list.
		DuplicateColumnError
			When a column name appears twice.
		"""
		if self.columns is None:
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_unique_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
