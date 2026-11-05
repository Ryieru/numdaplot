"""
Computation of any statistic on the values of an Array.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.axis_number import find_numpy_axis
from numdaplot.arrays.calculation.counting_statistics import (
	compute_count,
	compute_count_distinct,
	compute_most_frequent,
	compute_most_frequent_count,
)
from numdaplot.arrays.calculation.location_statistics import (
	compute_maximum,
	compute_mean,
	compute_median,
	compute_minimum,
	compute_quantile,
	compute_standard_deviation,
	compute_sum,
)
from numdaplot.arrays.creation.numpy_conversion import normalize_text
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.errors.empty_array_error import EmptyArrayError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.positions.axis import Axis
from numdaplot.settings.setting_types import require_object_not_class
from numdaplot.statistics.count import Count
from numdaplot.statistics.count_distinct import CountDistinct
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.most_frequent import MostFrequent
from numdaplot.statistics.most_frequent_count import MostFrequentCount
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum

type StatisticFunction = Callable[[NDArray[Any], int | None, Statistic], Any]


@dataclass(frozen=True)
class StatisticCalculation:
	"""
	How a statistic is computed on the values of an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The function computing the statistic, given the values, the numpy axis and the statistic.
	accepted_families
		The families of types the statistic applies to.
	needs_present_value
		Whether the statistic needs at least one present value per slice.
	"""

	function: StatisticFunction
	accepted_families: frozenset[ValueFamily]
	needs_present_value: bool


ALL_FAMILIES = frozenset(ValueFamily)
NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
NUMBER_AND_BOOL_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.BOOL})
STATISTIC_CALCULATIONS = {
	Sum: StatisticCalculation(compute_sum, NUMBER_AND_BOOL_FAMILIES, needs_present_value=False),
	Mean: StatisticCalculation(compute_mean, NUMBER_AND_BOOL_FAMILIES, needs_present_value=True),
	Median: StatisticCalculation(compute_median, NUMBER_FAMILIES, needs_present_value=True),
	Min: StatisticCalculation(compute_minimum, ALL_FAMILIES, needs_present_value=True),
	Max: StatisticCalculation(compute_maximum, ALL_FAMILIES, needs_present_value=True),
	Count: StatisticCalculation(compute_count, ALL_FAMILIES, needs_present_value=False),
	CountDistinct: StatisticCalculation(compute_count_distinct, ALL_FAMILIES, needs_present_value=False),
	StandardDeviation: StatisticCalculation(compute_standard_deviation, NUMBER_FAMILIES, needs_present_value=True),
	Quantile: StatisticCalculation(compute_quantile, NUMBER_FAMILIES, needs_present_value=True),
	MostFrequent: StatisticCalculation(compute_most_frequent, ALL_FAMILIES, needs_present_value=True),
	MostFrequentCount: StatisticCalculation(compute_most_frequent_count, ALL_FAMILIES, needs_present_value=False),
}
SINGLE_VALUE_DIMENSIONS = (1,)
UNKNOWN_STATISTIC_OPERATION = "The statistic {statistic_name}"
UNKNOWN_STATISTIC_ALTERNATIVE = "a statistic of numdaplot"
STATISTIC_SETTING = "compute statistic"
STATISTIC_EXPECTED = "a statistic such as ndp.Mean()"


def compute_statistic(values: NDArray[Any], statistic: Statistic, axis: Axis | None) -> NDArray[Any]:
	"""
	Return a statistic of the present values, for the whole Array or for each row or column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	statistic
		Any statistic of numdaplot.
	axis
		``EACH_ROW`` for one result per row, ``EACH_COLUMN`` for one per column,
		``None`` for a single result.

	Returns
	-------
	NDArray
		A single value in one dimension when ``axis`` is ``None``, otherwise one value per row or column.

	Raises
	------
	InvalidSettingTypeError
		When ``statistic`` is a class, written without its parentheses.
	IncompatibleTypesError
		When the statistic does not apply to the type of the values.
	DimensionError
		When an axis is given for an Array that is not two-dimensional.
	EmptyArrayError
		When the statistic needs a present value and a slice has none.
	RefusedOperationError
		When the statistic is not a statistic of numdaplot.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.statistic_values import compute_statistic
	>>> compute_statistic(numpy.array([[1, 2], [3, 4]]), ndp.Sum(), ndp.Axis.EACH_ROW)
	array([3, 7])
	"""
	require_object_not_class(STATISTIC_SETTING, STATISTIC_EXPECTED, statistic)

	statistic_class = type(statistic)
	statistic_name = statistic_class.__name__
	if statistic_class not in STATISTIC_CALCULATIONS:
		operation = UNKNOWN_STATISTIC_OPERATION.format(statistic_name=statistic_name)
		raise RefusedOperationError(operation, UNKNOWN_STATISTIC_ALTERNATIVE)

	calculation = STATISTIC_CALCULATIONS[statistic_class]
	require_family(values, calculation.accepted_families, statistic_name)
	numpy_axis = find_numpy_axis(axis, values.ndim)
	if calculation.needs_present_value:
		require_present_values(values, numpy_axis, statistic_name)

	result = calculation.function(values, numpy_axis, statistic)
	result_values = numpy.asarray(result)
	if numpy_axis is None:
		result_values = result_values.reshape(SINGLE_VALUE_DIMENSIONS)

	normalized_values = normalize_text(result_values)

	return normalized_values


def require_present_values(values: NDArray[Any], axis: int | None, statistic_name: str) -> None:
	"""
	Check that the whole Array, or each slice along an axis, holds at least one present value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	axis
		The numpy axis to reduce, or ``None`` for the whole Array.
	statistic_name
		Name of the statistic, shown in the error message.

	Raises
	------
	EmptyArrayError
		When the Array, or one of its slices, has no present value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.statistic_values import require_present_values
	>>> try:
	... 	require_present_values(numpy.array([numpy.nan]), None, "Mean")
	... except ndp.EmptyArrayError as error:
	... 	print(error)
	Cannot compute Mean without any present value.
	"""
	missing = find_missing(values)
	present = ~missing
	present_counts = numpy.sum(present, axis=axis)
	empty_slices = present_counts == 0
	has_empty_slice = numpy.any(empty_slices)
	if has_empty_slice:
		raise EmptyArrayError(statistic_name)
