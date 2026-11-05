"""
Missing values of a Table, read to be drawn.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.plots.data.chart_values import ChartValues, Positions, Series
from numdaplot.plots.data.position_kind import PositionKind
from numdaplot.positions.axis import Axis
from numdaplot.ratios.measure import Measure
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_counts import (
	COLUMN_NAMES_COLUMN,
	MEASURE_COLUMN_NAMES,
	count_frame_missing,
	find_frame_missing,
)
from numdaplot.tables.table import Table

MEASURE_LABELS = {
	Measure.COUNT: "Missing count",
	Measure.RATIO: "Missing ratio",
}
FLOAT_DTYPE = numpy.dtype(numpy.float64)
TEXT_DTYPE = numpy.dtype(object)


def read_missing_counts(table: Table, measure: Measure) -> ChartValues:
	"""
	Return the number or the share of missing values of each column of a Table, as one series of bars.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table counted.
	measure
		``Measure.COUNT`` for the number of missing values, ``Measure.RATIO`` for their share.

	Returns
	-------
	ChartValues
		The column names as text positions, the counts as a single series, and ``"Missing count"`` or
		``"Missing ratio"`` as label of the axis of the values.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.missing_cells import read_missing_counts
	>>> prices = ndp.Array.from_list([12.0, None])
	>>> rooms = ndp.Array.from_list([2, 3])
	>>> flats = ndp.Table.from_arrays({"price": prices, "rooms": rooms})
	>>> read_missing_counts(flats, ndp.Measure.RATIO).series[0].values
	array([0.5, 0. ])
	"""
	frame = table.to_pandas()
	missing_count = MissingCount(measure=measure)
	counts_frame = count_frame_missing(frame, missing_count, Axis.EACH_COLUMN)
	count_name = MEASURE_COLUMN_NAMES[measure]
	column_names = counts_frame[COLUMN_NAMES_COLUMN].to_numpy(dtype=TEXT_DTYPE)
	counts = counts_frame[count_name].to_numpy(dtype=FLOAT_DTYPE, na_value=numpy.nan)
	column_count = len(column_names)
	rows = numpy.arange(column_count)
	positions = Positions(PositionKind.TEXTS, column_names, None)
	count_series = Series(count_name, counts)
	measure_label = MEASURE_LABELS[measure]
	count_values = ChartValues(positions, [count_series], rows, measure_label)

	return count_values


def read_missing_cells(table: Table) -> ChartValues:
	"""
	Return where the values of a Table are missing, 1 for a missing value and 0 for a present one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		The Table read.

	Returns
	-------
	ChartValues
		The row numbers as positions, and one series per column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.plots.data.missing_cells import read_missing_cells
	>>> prices = ndp.Array.from_list([12.0, None])
	>>> flats = ndp.Table.from_arrays({"price": prices})
	>>> read_missing_cells(flats).series[0].values
	array([0., 1.])
	"""
	frame = table.to_pandas()
	missing_grid = find_frame_missing(frame)
	cells = missing_grid.astype(FLOAT_DTYPE)
	column_names = frame.columns.tolist()
	row_count = len(frame)
	rows = numpy.arange(row_count)
	row_numbers = rows.astype(FLOAT_DTYPE)
	positions = Positions(PositionKind.NUMBERS, row_numbers, None)
	series = list[Series]()

	for i, column_name in enumerate(column_names):
		column_cells = cells[:, i]
		column_series = Series(column_name, column_cells)
		series.append(column_series)

	cell_values = ChartValues(positions, series, rows, None)

	return cell_values
