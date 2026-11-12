"""
Settings of the count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.ratios.measure import Measure
from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import require_column_name


@dataclass(frozen=True)
class ValueCount:
	"""
	The column whose values are counted, and how, used by ``Table.count_values``.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		The name of the column.
	measure
		The number of rows holding each value by default, or with ``Measure.RATIO`` their fraction of every row.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``column`` is an empty text.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> answers = ndp.Table.from_arrays({"sex": ndp.Array.from_list([2.0, 1.0, 2.0, None])})
	>>> answers.count_values(ndp.ValueCount(column="sex", measure=ndp.Measure.RATIO))
	      sex value_ratio
	  FLOAT64     FLOAT64
	0     2.0        0.50
	1     1.0        0.25
	2     NaN        0.25
	"""

	column: str
	measure: Measure = Measure.COUNT

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and that the column name is a non-empty text.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``column`` is an empty text.
		"""
		require_field_types(self)

		require_column_name(self.column)
