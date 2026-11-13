"""
A function applied to columns of a Table.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.column_names import copy_column_names
from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.dates.time_function import TimeFunction
from numdaplot.math_functions.math_function import MathFunction


@dataclass(frozen=True)
class TableApplication:
	"""
	A function applied to each value of columns of a Table, used by ``Table.apply``.

	Each column is replaced at its place, under its name. A missing value stays missing, and an integer or boolean
	column keeps its type when a ``ValueMapping`` gives it missing values.

	.. versionadded:: 0.2.0

	Parameters
	----------
	function
		A ``MathFunction``, such as ``ndp.SquareRoot()``, a ``TimeFunction``, such as
		``ndp.DatePart(unit=ndp.DatePartUnit.MONTH)``, or a ``ValueMapping``, as ``Array.apply`` takes.
	columns
		The names of the columns, at least one, each once. The application keeps its own copy of the list.

	Raises
	------
	InvalidTypeError
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
	>>> first_answers = ndp.Array.from_list([1, 7, 2])
	>>> second_answers = ndp.Array.from_list([9, 3, 1])
	>>> survey = ndp.Table.from_arrays({"q1": first_answers, "q2": second_answers})
	>>> unknown_answers = [ndp.ValueChange(7, None), ndp.ValueChange(9, None)]
	>>> mapping = ndp.ValueMapping(changes=unknown_answers, others=ndp.Unmatched.KEEP)
	>>> survey.apply(ndp.TableApplication(function=mapping, columns=["q1", "q2"]))
	     q1    q2
	  INT64 INT64
	0     1  <NA>
	1  <NA>     3
	2     2     1
	"""

	function: MathFunction | TimeFunction | ValueMapping
	columns: list[str]

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the application holds.

		.. versionadded:: 0.2.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_field_types(self)

		columns_copy = copy_column_names(self.columns)
		object.__setattr__(self, "columns", columns_copy)
