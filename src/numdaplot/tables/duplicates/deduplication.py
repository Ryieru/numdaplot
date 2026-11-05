"""
Settings of the removal of duplicated rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.setting_types import require_list_not_text
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.duplicates.keep import Keep

COLUMN_ITEM_NAME = "column"
COLUMNS_SETTING = "Deduplication columns"


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
	InvalidSettingTypeError
		When ``columns`` is a single text instead of a list.
	EmptyListError
		When ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"]))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	columns: list[str] | None = None
	keep: Keep = Keep.FIRST

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the deduplication holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``columns`` is a single text instead of a list.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_list_not_text(COLUMNS_SETTING, self.columns)

		if self.columns is None:
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_column_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
