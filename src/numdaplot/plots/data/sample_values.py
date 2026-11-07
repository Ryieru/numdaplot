"""
Values a histogram or a box chart sums up, read from a Table or an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array import Array
from numdaplot.data_types.type import Type
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_data import require_column_setting, require_no_column_settings
from numdaplot.plots.data.chart_values import Series
from numdaplot.plots.data.column_reading import read_texts
from numdaplot.plots.data.table_values import name_columns, read_series
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.table import Table
from numdaplot.tables.table_data import read_stored_frame

COLUMNS_SETTING = "columns"
GROUP_SETTING = "group_by"


@dataclass(frozen=True, eq=False)
class SampleValues:
	"""
	The columns of numbers or times of day a histogram or a box chart sums up, and the groups splitting their rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	series
		One series per column, NaN where a value is missing, a time of day being its hours since midnight.
	groups
		The group of each row, None where it is missing, or None without ``group_by``.
	group_name
		The ``group_by`` column, or None.
	value_name
		The default label of the axis of the values: the name of the single column of a Table, None otherwise.
	value_type
		The type of the first series, of the family of every series: numbers or times of day.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_values import Series
	>>> from numdaplot.plots.data.sample_values import SampleValues
	>>> SampleValues([Series("price", numpy.array([12.0]))], None, None, "price", ndp.Type.FLOAT64).value_name
	'price'
	"""

	series: list[Series]
	groups: NDArray[Any] | None
	group_name: str | None
	value_name: str | None
	value_type: Type


def read_sample_values(
	data: Table | Array, column_names: list[str] | None, group_name: str | None, chart_name: str
) -> SampleValues:
	"""
	Return the columns a histogram or a box chart sums up, and their groups.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	column_names
		The columns of a Table, None for an Array, whose columns are all read.
	group_name
		The ``group_by`` column of a Table, holding texts, booleans or times of day, or None.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	SampleValues
		One series per column, and the group of each row.

	Raises
	------
	InvalidChartDataError
		When a Table has no columns, or an Array has columns or ``group_by``.
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When a column holds neither numbers nor times of day, the columns mix them, or ``group_by`` holds
		neither texts, booleans nor times of day.
	DimensionError
		When an Array has more than two dimensions.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.sample_values import read_sample_values
	>>> cities = ndp.Array.from_list(["Paris", "Lyon"])
	>>> prices = ndp.Array.from_list([12.0, 9.5])
	>>> flats = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> read_sample_values(flats, ["price"], "city", "BoxChart").groups
	array(['Paris', 'Lyon'], dtype=object)
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object]({COLUMNS_SETTING: column_names, GROUP_SETTING: group_name})
		require_no_column_settings(chart_name, column_settings)
		array_values = read_array_values(data, chart_name)
		array_samples = SampleValues(array_values.series, None, None, array_values.value_name, array_values.value_type)
		return array_samples

	required_names = require_column_setting(chart_name, COLUMNS_SETTING, column_names)
	frame = read_stored_frame(data)
	known_names = frame.columns.tolist()
	require_known_columns(required_names, known_names)
	series, value_type = read_series(frame, required_names, chart_name)
	value_name = name_columns(required_names)
	groups = None
	if group_name is not None:
		require_known_columns([group_name], known_names)
		groups = read_texts(frame[group_name], chart_name)

	table_samples = SampleValues(series, groups, group_name, value_name, value_type)

	return table_samples


def drop_missing_numbers(numbers: NDArray[numpy.float64]) -> NDArray[numpy.float64]:
	"""
	Return the numbers that are present, in their order.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		Numbers, NaN where a value is missing.

	Returns
	-------
	NDArray[numpy.float64]
		The numbers without NaN.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.sample_values import drop_missing_numbers
	>>> drop_missing_numbers(numpy.array([3.0, numpy.nan, 1.0]))
	array([3., 1.])
	"""
	present = ~numpy.isnan(numbers)
	present_numbers = numbers[present]

	return present_numbers
