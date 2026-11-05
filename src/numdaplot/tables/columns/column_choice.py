"""
Settings of the choice of the columns of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.setting_types import require_list_not_text
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.column_names import require_column_names

COLUMN_ITEM_NAME = "column"
COLUMNS_SETTING = "ColumnChoice columns"


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
	InvalidSettingTypeError
		When ``columns`` is a single text instead of a list.
	EmptyListError
		When ``columns`` is empty with ``KEEP``, which would keep nothing.
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
	>>> sales.choose_columns(ndp.ColumnChoice(columns=["price"]))
	    price
	  FLOAT64
	0   120.0
	1    80.0
	2   150.0
	"""

	columns: list[str]
	mode: ColumnMode = ColumnMode.KEEP

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the choice holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``columns`` is a single text instead of a list.
		EmptyListError
			When ``columns`` is empty with ``KEEP``.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_list_not_text(COLUMNS_SETTING, self.columns)

		keeps_nothing = self.columns == [] and self.mode == ColumnMode.KEEP
		if keeps_nothing:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_column_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
