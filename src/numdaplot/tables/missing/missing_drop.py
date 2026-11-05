"""
Settings of the removal of the rows or the columns of a Table holding missing values.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_column_names
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio

COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class MissingDrop:
	"""
	Which rows or columns holding missing values are removed, used by ``Table.drop_missing``.

	The axis, rows or columns, is given to ``Table.drop_missing`` itself.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The names of the columns looked at, every column when omitted. Rows are removed according to
		their values in these columns; columns are only removed among them, the others are always kept.
		The settings keep their own copy of the list.
	rule
		How many missing values make a row or a column removed: a single one by default, all of them with
		``MissingMode.ALL``, or a share of them with ``MissingRatio``. In a Table without rows, no column
		is removed.

	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, 150.0])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> table.drop_missing()
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1    Pau   150.0
	>>> table.drop_missing(ndp.MissingDrop(columns=["price"]), axis=ndp.Axis.EACH_COLUMN)
	    city
	    TEXT
	0  Paris
	1   Lyon
	2    Pau
	"""

	columns: list[str] | None = None
	rule: MissingMode | MissingRatio = MissingMode.ANY

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the settings hold.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_field_types(self)

		if self.columns is None:
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_column_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
