"""
A rectangular part of an Array or a Table, chosen by position.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from types import NoneType

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.empty_region_error import EmptyRegionError
from numdaplot.positions.index import Index
from numdaplot.positions.range import Range
from numdaplot.settings.setting_types import require_list_not_text, require_setting_type
from numdaplot.tables.columns.column_names import require_column_names

ROWS_SETTING = "Region rows"
ROWS_EXPECTED = "an Index, a Range or None"
ROW_TYPES = (Index, Range, NoneType)
COLUMNS_SETTING = "Region columns"
COLUMNS_EXPECTED = "an Index, a Range, a list of column names or None"
COLUMN_TYPES = (Index, Range, list, NoneType)
COLUMN_ITEM_NAME = "column"


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
	InvalidSettingTypeError
		When ``rows`` or ``columns`` is of another kind, such as a number or a single text.
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

	rows: Index | Range | None = None
	columns: Index | Range | list[str] | None = None

	def __post_init__(self) -> None:
		"""
		Check the rows and the columns, and replace a list of column names with a copy only the region holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When ``rows`` or ``columns`` is of another kind, such as a number or a single text.
		EmptyRegionError
			When ``rows`` and ``columns`` are both omitted.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_setting_type(ROWS_SETTING, ROWS_EXPECTED, self.rows, ROW_TYPES)
		require_list_not_text(COLUMNS_SETTING, self.columns)
		require_setting_type(COLUMNS_SETTING, COLUMNS_EXPECTED, self.columns, COLUMN_TYPES)
		has_no_position = self.rows is None and self.columns is None
		if has_no_position:
			raise EmptyRegionError()

		if not isinstance(self.columns, list):
			return

		if self.columns == []:
			raise EmptyListError(COLUMN_ITEM_NAME)

		require_column_names(self.columns)
		columns_copy = list(self.columns)
		object.__setattr__(self, "columns", columns_copy)
