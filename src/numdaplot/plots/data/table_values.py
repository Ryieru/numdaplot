"""
Values a chart draws from the columns of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.column_reading import read_numbers, read_positions
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.table import Table


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
		The columns of numbers drawn, one series each.
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
		When ``x`` holds booleans or durations, or a ``y`` column does not hold numbers.

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
	frame = table.to_pandas()
	column_names = frame.columns.tolist()
	require_known_columns(y_names, column_names)
	positions = read_table_positions(frame, x_name, chart_name)
	missing_positions = find_missing_positions(positions)
	rows = numpy.flatnonzero(~missing_positions)
	if positions.kind != PositionKind.TEXTS:
		rows = numpy.arange(len(frame))

	kept_positions = Positions(positions.kind, positions.values[rows], positions.name)
	series = list[Series]()

	for y_name in y_names:
		numbers = read_numbers(frame[y_name], chart_name)
		drawn_numbers = numpy.where(missing_positions, numpy.nan, numbers)
		kept_numbers = drawn_numbers[rows]
		column_series = Series(y_name, kept_numbers)
		series.append(column_series)

	value_name = None
	y_count = len(y_names)
	if y_count == 1:
		value_name = y_names[0]

	chart_values = ChartValues(kept_positions, series, rows, value_name)

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
