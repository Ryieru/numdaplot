"""
Settings of the removal of the rows or the columns of a Table holding missing values.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.positions.axis import Axis
from numdaplot.tables.columns.column_names import require_unique_names
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio

COLUMN_ITEM_NAME = "column"


@dataclass(frozen=True)
class MissingDrop:
	"""
	Which rows or columns holding missing values are removed, used by ``Table.drop_missing``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	axis
		``Axis.EACH_ROW`` by default to remove rows, ``Axis.EACH_COLUMN`` to remove columns.
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
	EmptyListError
		When ``columns`` is an empty list.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Pau"])
	>>> prices = ndp.Array.from_list([120.0, None, 150.0])
	>>> table = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> table.drop_missing(ndp.MissingDrop())
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1    Pau   150.0
	>>> table.drop_missing(ndp.MissingDrop(axis=ndp.Axis.EACH_COLUMN))
	    city
	    TEXT
	0  Paris
	1   Lyon
	2    Pau
	"""

	axis: Axis = Axis.EACH_ROW
	columns: list[str] | None = None
	rule: MissingMode | MissingRatio = MissingMode.ANY

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the settings hold.

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
