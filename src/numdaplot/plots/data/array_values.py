"""
Values a chart draws from the columns of an Array.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.array import Array
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.position_kind import PositionKind

NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
ONE_DIMENSION = 1
TWO_DIMENSIONS = 2
FLOAT_DTYPE = numpy.dtype(numpy.float64)
VALUE_LABEL = "Value"


def read_array_values(array: Array, chart_name: str) -> ChartValues:
	"""
	Return the positions and the series a chart draws from an Array of numbers.

	Each column is a series named after its number, and each row is placed at its number.
	A one-dimensional Array is a single column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		An Array of numbers, of one or two dimensions.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	ChartValues
		The row numbers as positions, and one series per column.

	Raises
	------
	IncompatibleTypesError
		When the Array does not hold numbers.
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
	values = array.to_numpy()
	require_family(values, NUMBER_FAMILIES, chart_name)
	dimension_count = values.ndim
	if dimension_count > TWO_DIMENSIONS:
		raise DimensionError(chart_name, dimension_count)

	if dimension_count == ONE_DIMENSION:
		values = values.reshape(-1, 1)

	numbers = values.astype(FLOAT_DTYPE)
	row_count, column_count = numbers.shape
	rows = numpy.arange(row_count)
	row_numbers = rows.astype(FLOAT_DTYPE)
	positions = Positions(PositionKind.NUMBERS, row_numbers, None)
	series = list[Series]()

	for i in range(column_count):
		column_name = str(i)
		column_numbers = numbers[:, i]
		column_series = Series(column_name, column_numbers)
		series.append(column_series)

	chart_values = ChartValues(positions, series, rows, VALUE_LABEL)

	return chart_values
