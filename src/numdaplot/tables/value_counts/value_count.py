"""
Settings of the count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.measures.measure import Measure
from numdaplot.tables.columns.column_names import require_column_name, require_optional_column_name


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
	weights
		A column of numbers telling how many units each row stands for, such as the weights of a survey. Each value
		then counts the sum of the weights of its rows, as decimals, in ``weighted_count`` or ``weighted_ratio``. A
		row without weight is left out, and a negative weight raises ``InvalidWeightError``. Every row counts once
		when omitted.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	InvalidColumnNameError
		When ``column`` or ``weights`` is an empty text.

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
	>>> weights = ndp.Array.from_list([100.0, 300.0, 100.0, None])
	>>> weighted_answers = answers.add_column(ndp.NewColumn(name="weight", values=weights))
	>>> weighted_answers.count_values(ndp.ValueCount(column="sex", measure=ndp.Measure.RATIO, weights="weight"))
	      sex weighted_ratio
	  FLOAT64        FLOAT64
	0     1.0            0.6
	1     2.0            0.4
	"""

	column: str
	measure: Measure = Measure.COUNT
	weights: str | None = None

	def __post_init__(self) -> None:
		"""
		Check the type of every setting, and that the column names are non-empty texts.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		InvalidColumnNameError
			When ``column`` or ``weights`` is an empty text.
		"""
		require_field_types(self)

		require_column_name(self.column)
		require_optional_column_name(self.weights)
