"""
Checks of the column settings of a chart against the data it draws.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.errors.invalid_chart_data_error import InvalidChartDataError
from numdaplot.errors.unsupported_data_error import UnsupportedDataError
from numdaplot.plots.data.array_values import read_array_values
from numdaplot.plots.data.chart_values import ChartValues
from numdaplot.plots.data.table_values import read_table_values
from numdaplot.tables.table import Table

TABLE_NAME = "a Table"
ARRAY_NAME = "an Array"
X_SETTING = "x"
Y_SETTING = "y"


def require_no_column_settings(chart_name: str, column_settings: dict[str, object]) -> None:
	"""
	Check that a chart drawing an Array names no column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class, shown in the error message.
	column_settings
		Each column setting of the chart by name, such as ``{"x": None, "y": None}``.

	Raises
	------
	InvalidChartDataError
		At the first setting that is not None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_data import require_no_column_settings
	>>> try:
	... 	require_no_column_settings("LineChart", {"x": "day", "y": None})
	... except ndp.InvalidChartDataError as error:
	... 	print(error)
	LineChart takes no x for an Array.
	"""
	for setting_name, setting_value in column_settings.items():
		if setting_value is not None:
			raise InvalidChartDataError(chart_name, setting_name, ARRAY_NAME, False)


def require_column_setting[SettingValue](
	chart_name: str, setting_name: str, setting_value: SettingValue | None
) -> SettingValue:
	"""
	Check that a chart drawing a Table has a column setting it needs, and return it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	chart_name
		Name of the chart class, shown in the error message.
	setting_name
		Name of the setting, such as ``y``.
	setting_value
		The value of the setting.

	Returns
	-------
	SettingValue
		The value, known not to be None.

	Raises
	------
	InvalidChartDataError
		When the value is None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_data import require_column_setting
	>>> try:
	... 	require_column_setting("LineChart", "y", None)
	... except ndp.InvalidChartDataError as error:
	... 	print(error)
	LineChart needs y for a Table.
	"""
	if setting_value is None:
		raise InvalidChartDataError(chart_name, setting_name, TABLE_NAME, True)

	return setting_value


def read_chart_values(
	data: Table | Array, x_name: str | None, y_names: list[str] | None, chart_name: str
) -> ChartValues:
	"""
	Return the positions and the series a line or bar chart draws from a Table or an Array.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array drawn.
	x_name
		The ``x`` column of a Table, None for its row numbers and for an Array.
	y_names
		The ``y`` columns of a Table, None for an Array.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	ChartValues
		The values read by ``read_table_values`` or ``read_array_values``.

	Raises
	------
	InvalidChartDataError
		When a Table has no ``y`` columns, or an Array has ``x`` or ``y`` columns.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_data import read_chart_values
	>>> prices = ndp.Array.from_list([12.0, 15.5])
	>>> sales = ndp.Table.from_arrays({"price": prices})
	>>> read_chart_values(sales, None, ["price"], "LineChart").value_name
	'price'
	"""
	if isinstance(data, Array):
		column_settings = dict[str, object]({X_SETTING: x_name, Y_SETTING: y_names})
		require_no_column_settings(chart_name, column_settings)
		array_values = read_array_values(data, chart_name)
		return array_values

	required_y_names = require_column_setting(chart_name, Y_SETTING, y_names)
	table_values = read_table_values(data, x_name, required_y_names, chart_name)

	return table_values


def require_table(data: Table | Array, owner_name: str) -> Table:
	"""
	Check that a chart or a plot function that reads columns by name draws a Table, and return it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data
		The Table or the Array given.
	owner_name
		Name of the chart class or of the plot function, shown in the error message.

	Returns
	-------
	Table
		The data, known to be a Table.

	Raises
	------
	UnsupportedDataError
		When the data is an Array.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.chart_data import require_table
	>>> sales = ndp.Array.from_list([120.0, 80.0])
	>>> try:
	... 	require_table(sales, "PieChart")
	... except ndp.UnsupportedDataError as error:
	... 	print(error)
	PieChart cannot draw an Array, use a Table.
	"""
	if isinstance(data, Array):
		raise UnsupportedDataError(owner_name, ARRAY_NAME)

	return data
