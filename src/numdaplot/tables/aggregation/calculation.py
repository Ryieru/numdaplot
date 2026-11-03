"""
A statistic computed on a column of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.aggregation.statistic_name import name_statistic
from numdaplot.tables.columns.column_names import require_column_name

RESULT_NAME = "{column}_{function}"


@dataclass(frozen=True)
class Calculation:
	"""
	A statistic computed on a column of a Table, used by ``Aggregation``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The name of the column.
	function
		Any statistic of numdaplot, such as ``ndp.Mean()``. Missing values are ignored.
	result_name
		The name of the result column. When omitted, it is ``<column>_<function>``, such as ``price_mean``
		or ``price_quantile_90``.

	Raises
	------
	InvalidColumnNameError
		When ``result_name`` is an empty text.
	RefusedOperationError
		When ``function`` is not a statistic of numdaplot.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Calculation(column="price", function=ndp.Mean(), result_name="average_price")
	Calculation(column='price', function=Mean(), result_name='average_price')
	"""

	column: str
	function: Statistic
	result_name: str | None = None

	def __post_init__(self) -> None:
		"""
		Check that the result name, given or automatic, is valid.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidColumnNameError
			When ``result_name`` is an empty text.
		RefusedOperationError
			When ``function`` is not a statistic of numdaplot.
		"""
		result_name = find_result_name(self)
		require_column_name(result_name)


def find_result_name(calculation: Calculation) -> str:
	"""
	Return the name of the column holding the result of a calculation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculation
		The calculation.

	Returns
	-------
	str
		The given result name, or ``<column>_<function>``.

	Raises
	------
	RefusedOperationError
		When the statistic is not a statistic of numdaplot and no result name is given.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.calculation import find_result_name
	>>> find_result_name(ndp.Calculation(column="price", function=ndp.Quantile(0.9)))
	'price_quantile_90'
	"""
	if calculation.result_name is not None:
		return calculation.result_name

	function_name = name_statistic(calculation.function)
	result_name = RESULT_NAME.format(column=calculation.column, function=function_name)

	return result_name
