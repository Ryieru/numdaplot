"""
Values a chart draws from the columns of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array import Array
from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.errors.positions.dimension_error import DimensionError
from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.column_reading import count_hours, find_value_families
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily, find_family

ONE_DIMENSION = 1
TWO_DIMENSIONS = 2
FLOAT_DTYPE = numpy.dtype(numpy.float64)
VALUE_LABEL = "Value"


def read_array_values(array: Array, chart_name: str) -> ChartValues:
	"""
	Return the positions and the series a chart draws from an Array of numbers or times of day.

	Only a chart measuring times of day accepts them. Each column is a series named after its number, and each row
	is placed at its number.
	A one-dimensional Array is a single column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		An Array of numbers or times of day, of one or two dimensions.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	ChartValues
		The row numbers as positions, and one series per column.

	Raises
	------
	IncompatibleTypesError
		When the Array holds neither numbers nor times of day for a chart measuring them.
	DimensionError
		When the Array has more than two dimensions.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_values
	>>> grid = ndp.Array.from_list([[1, 2], [3, 4]])
	>>> read_array_values(grid, "LineChart").series[1].values
	array([2., 4.])
	"""
	values = read_stored_values(array)
	value_families = find_value_families(chart_name)
	require_family(values, value_families, chart_name)
	dimension_count = values.ndim
	if dimension_count > TWO_DIMENSIONS:
		raise DimensionError(chart_name, dimension_count)

	if dimension_count == ONE_DIMENSION:
		values = values.reshape(-1, 1)

	value_type = from_numpy_dtype(values.dtype)
	numbers = read_array_numbers(values, value_type)
	row_count, column_count = values.shape
	rows = numpy.arange(row_count)
	row_numbers = rows.astype(FLOAT_DTYPE)
	positions = Positions(PositionKind.NUMBERS, row_numbers, None)
	series = list[Series]()

	for i in range(column_count):
		column_name = str(i)
		column_numbers = numbers[:, i]
		column_series = Series(column_name, column_numbers)
		series.append(column_series)

	chart_values = ChartValues(positions, series, rows, VALUE_LABEL, value_type)

	return chart_values


def read_array_numbers(values: NDArray[Any], value_type: Type) -> NDArray[numpy.float64]:
	"""
	Return the values of an Array as float64 numbers, a time of day being its hours since midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The stored values of an Array of numbers or times of day.
	value_type
		The type of the values.

	Returns
	-------
	NDArray[numpy.float64]
		The numbers, of the same shape, NaN where a time of day is missing.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.array_values import read_array_numbers
	>>> read_array_numbers(numpy.array([5400000000], dtype="timedelta64[us]"), ndp.Type.TIME)
	array([1.5])
	"""
	value_family = find_family(value_type)
	if value_family == ValueFamily.TIME:
		hours = count_hours(values)
		return hours

	numbers = values.astype(FLOAT_DTYPE)

	return numbers
