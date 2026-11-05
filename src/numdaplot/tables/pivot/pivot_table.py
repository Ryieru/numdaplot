"""
Settings of a pivot table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.refused_setting_error import RefusedSettingError
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.columns.column_names import require_column_name, require_column_names, require_unique_names

ROW_COLUMN_ITEM_NAME = "row column"
RESULT_NAME_SETTING = "the result_name of its calculation"
PIVOT_TABLE_NAME = "PivotTable"


@dataclass(frozen=True)
class PivotTable:
	"""
	One row per group of rows and one column per value of a column, used by ``Table.pivot_table``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		The names of the columns whose values form the rows of the result: one row per combination of values, sorted,
		with missing values as a group of their own, last. The pivot table keeps its own copy of the list.
	columns
		The name of the column whose values become the columns of the result, sorted. It cannot hold missing values.
		The values are written as texts: ``"Paris"``, ``"8"`` for 8 and 8.0, ``"2.5"``, ``"2026-12-31"``.
	calculation
		The statistic of each cell. A combination without any row gives what the statistic gives without value: 0
		for ``Count`` and ``Sum``, a missing value for ``Mean`` or ``Max``. Its ``result_name`` is refused, since each
		result column is named after a value.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``rows`` is an empty list.
	InvalidColumnNameError
		When ``columns`` or a name in ``rows`` is an empty text.
	DuplicateColumnError
		When a name appears twice among ``rows`` and ``columns``.
	RefusedSettingError
		When the calculation has a ``result_name``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> hours = ndp.Array.from_list([8, 8, 9])
	>>> weekdays = ndp.Array.from_list(["Mon", "Tue", "Mon"])
	>>> fares = ndp.Array.from_list([7.0, 9.0, 5.0])
	>>> trips = ndp.Table.from_arrays({"hour": hours, "weekday": weekdays, "fare": fares})
	>>> total_fare = ndp.Calculation(column="fare", function=ndp.Sum())
	>>> trips.pivot_table(ndp.PivotTable(rows=["hour"], columns="weekday", calculation=total_fare))
	   hour     Mon     Tue
	  INT64 FLOAT64 FLOAT64
	0     8     7.0     9.0
	1     9     5.0     0.0
	"""

	rows: list[str]
	columns: str
	calculation: Calculation

	def __post_init__(self) -> None:
		"""
		Check the names and the calculation, and replace ``rows`` with a copy that only the pivot table holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``rows`` is an empty list.
		InvalidColumnNameError
			When ``columns`` or a name in ``rows`` is an empty text.
		DuplicateColumnError
			When a name appears twice among ``rows`` and ``columns``.
		RefusedSettingError
			When the calculation has a ``result_name``.
		"""
		require_field_types(self)

		if self.rows == []:
			raise EmptyListError(ROW_COLUMN_ITEM_NAME)

		if self.calculation.result_name is not None:
			raise RefusedSettingError(RESULT_NAME_SETTING, PIVOT_TABLE_NAME)

		require_column_names(self.rows)
		require_column_name(self.columns)
		rows_copy = list(self.rows)
		object.__setattr__(self, "rows", rows_copy)
		grouping_names = [*rows_copy, self.columns]
		require_unique_names(grouping_names)
