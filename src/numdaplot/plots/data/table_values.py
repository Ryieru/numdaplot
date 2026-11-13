"""
Values a chart draws from the columns of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.data_types.type import Type
from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.column_reading import read_positions, read_values, require_same_family
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.table import Table
from numdaplot.tables.table_data import read_stored_frame

MAXIMUM_NAMED_COLUMNS = 3
NAME_SEPARATOR = ", "
SHORTENED_NAMES = "{joined_names} and {other_count} more"


def read_table_values(table: Table, x_name: str | None, y_names: list[str], chart_name: str) -> ChartValues:
	"""
	Return the positions and the series a chart draws from a Table.

	A row whose ``x`` number or moment is missing draws no value, so it breaks a line. A row whose ``x`` text
	is missing is left out, having no label.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table drawn.
	x_name
		The column of the positions, or None for the row numbers.
	y_names
		The columns drawn, one series each: numbers, or times of day for a chart measuring them.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	ChartValues
		The positions, and one series per ``y`` column.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist.
	IncompatibleTypesError
		When ``x`` holds booleans or durations, a ``y`` column holds neither numbers nor times of day for a chart
		measuring them, or the ``y`` columns mix numbers and times of day.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.table_values import read_table_values
	>>> sales = ndp.Table.from_pandas(pandas.DataFrame({"city": ["Paris", None, "Pau"], "price": [12.0, 15.5, None]}))
	>>> chart_values = read_table_values(sales, "city", ["price"], "BarChart")
	>>> chart_values.positions.values
	array(['Paris', 'Pau'], dtype=object)
	>>> chart_values.series[0].values
	array([12., nan])
	"""
	frame = read_stored_frame(table)
	column_names = frame.columns.tolist()
	require_known_columns(y_names, column_names)
	positions = read_table_positions(frame, x_name, chart_name)
	missing_positions = find_missing_positions(positions)
	rows = numpy.flatnonzero(~missing_positions)
	if positions.kind != PositionKind.TEXTS:
		rows = numpy.arange(len(frame))

	kept_positions = Positions(positions.kind, positions.values[rows], positions.name)
	column_series, value_type = read_series(frame, y_names, chart_name)
	series = list[Series]()

	for one_series in column_series:
		drawn_numbers = numpy.where(missing_positions, numpy.nan, one_series.values)
		kept_numbers = drawn_numbers[rows]
		kept_series = Series(one_series.name, kept_numbers)
		series.append(kept_series)

	value_name = name_columns(y_names)
	chart_values = ChartValues(kept_positions, series, rows, value_name, value_type)

	return chart_values


def read_table_positions(frame: pandas.DataFrame, x_name: str | None, chart_name: str) -> Positions:
	"""
	Return the ``x`` values of a chart drawing a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the Table.
	x_name
		The column of the positions, or None for the row numbers.
	chart_name
		Name of the chart class, shown in error messages.

	Returns
	-------
	Positions
		The values of the column, or the row numbers from 0.

	Raises
	------
	ColumnNotFoundError
		When the ``x`` column does not exist.
	IncompatibleTypesError
		When the ``x`` column holds booleans or durations.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.table_values import read_table_positions
	>>> read_table_positions(pandas.DataFrame({"price": [12.0, 15.5]}), None, "LineChart").values
	array([0., 1.])
	"""
	if x_name is None:
		row_count = len(frame)
		row_numbers = numpy.arange(row_count, dtype=numpy.float64)
		row_positions = Positions(PositionKind.NUMBERS, row_numbers, None)
		return row_positions

	column_names = frame.columns.tolist()
	require_known_columns([x_name], column_names)
	kind, values = read_positions(frame[x_name], chart_name)
	column_positions = Positions(kind, values, x_name)

	return column_positions


def find_missing_positions(positions: Positions) -> NDArray[numpy.bool_]:
	"""
	Return which ``x`` values are missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The ``x`` values of a chart.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each NaN number, NaT moment or missing text.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.plots.data.chart_values import Positions
	>>> from numdaplot.plots.data.position_kind import PositionKind
	>>> from numdaplot.plots.data.table_values import find_missing_positions
	>>> find_missing_positions(Positions(PositionKind.TEXTS, numpy.array(["Paris", None]), "city"))
	array([False,  True])
	"""
	missing_values = pandas.isna(positions.values)

	return missing_values


def read_series(frame: pandas.DataFrame, column_names: list[str], chart_name: str) -> tuple[list[Series], Type]:
	"""
	Return each column of values of a Table as a series named after it, with the type of the first column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of the Table.
	column_names
		The columns read, at least one, known to exist.
	chart_name
		Name of the chart class, shown in the error message.

	Returns
	-------
	tuple[list[Series], Type]
		One series per column, NaN where a value is missing, a time of day being its hours since midnight, and
		the type of the first column.

	Raises
	------
	IncompatibleTypesError
		When a column holds neither numbers nor times of day for a chart measuring them, or the columns mix
		numbers and times of day.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.plots.data.table_values import read_series
	>>> frame = pandas.DataFrame({"price": [12.0, None]})
	>>> series, value_type = read_series(frame, ["price"], "BoxChart")
	>>> series[0].values, value_type
	(array([12., nan]), <Type.FLOAT64: 10>)
	"""
	series = list[Series]()
	first_name = column_names[0]
	first_column = frame[first_name]
	value_type = find_column_type(first_column)

	for column_name in column_names:
		column = frame[column_name]
		values = read_values(column, chart_name)
		require_same_family(column, value_type, chart_name)
		column_series = Series(column_name, values)
		series.append(column_series)

	return series, value_type


def name_columns(column_names: list[str]) -> str:
	"""
	Return the names of the columns a chart draws, which name its values in the default title.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column_names
		The columns drawn, at least one.

	Returns
	-------
	str
		The names one after the other. Beyond 3 columns, the first 3 and the number of the others.

	Examples
	--------
	>>> from numdaplot.plots.data.table_values import name_columns
	>>> name_columns(["price"]), name_columns(["price", "cost"])
	('price', 'price, cost')
	>>> name_columns(["price", "cost", "tax", "tip"])
	'price, cost, tax and 1 more'
	"""
	named_columns = column_names[:MAXIMUM_NAMED_COLUMNS]
	joined_names = NAME_SEPARATOR.join(named_columns)
	other_count = len(column_names) - MAXIMUM_NAMED_COLUMNS
	if other_count <= 0:
		return joined_names

	shortened_names = SHORTENED_NAMES.format(joined_names=joined_names, other_count=other_count)

	return shortened_names
