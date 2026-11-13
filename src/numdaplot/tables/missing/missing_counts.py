"""
Count of the missing values of a Table.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.measures.count_division import divide_counts
from numdaplot.measures.measure import Measure
from numdaplot.positions.axis import Axis
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.types.numpy_mapping import to_numpy_dtype
from numdaplot.types.type import Type

COLUMN_NAMES_COLUMN = "column"
MEASURE_COLUMN_NAMES = {
	Measure.COUNT: "missing_count",
	Measure.RATIO: "missing_ratio",
}
# A numpy sum along axis 0 gives one result per column, along axis 1 one result per row.
COLUMN_SUM_AXIS = 0
ROW_SUM_AXIS = 1


def count_frame_missing(frame: pandas.DataFrame, missing_count: MissingCount, axis: Axis | None) -> pandas.DataFrame:
	"""
	Return the count of the missing values of a Table, for the whole Table, each row or each column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	missing_count
		The measure of the count.
	axis
		``EACH_ROW`` for one count per row, ``EACH_COLUMN`` for one per column, or None for the whole Table.

	Returns
	-------
	pandas.DataFrame
		A ``missing_count`` or ``missing_ratio`` column: one row for the whole Table, one row per row,
		or one row per column after a ``column`` column naming it. A ratio without any value is missing.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_counts import count_frame_missing
	>>> frame = pandas.DataFrame({"price": [1.5, None], "stock": [None, None]})
	>>> count_frame_missing(frame, ndp.MissingCount(measure=ndp.Measure.RATIO), ndp.Axis.EACH_ROW)
	   missing_ratio
	0            0.5
	1            1.0
	"""
	missing_grid = find_frame_missing(frame)
	counts, value_count = count_axis_missing(missing_grid, axis)
	measures = counts
	if missing_count.measure == Measure.RATIO:
		measures = divide_counts(counts, value_count)

	measure_name = MEASURE_COLUMN_NAMES[missing_count.measure]
	measure_column = build_column(measures)
	count_columns = dict[str, Column]()
	if axis == Axis.EACH_COLUMN:
		count_columns[COLUMN_NAMES_COLUMN] = build_name_column(frame)

	count_columns[measure_name] = measure_column
	count_frame = pandas.DataFrame(count_columns)

	return count_frame


def find_frame_missing(frame: pandas.DataFrame) -> NDArray[numpy.bool_]:
	"""
	Return which values of a Table are missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	NDArray[numpy.bool_]
		One row per row and one column per column, True at each missing value.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.missing.missing_counts import find_frame_missing
	>>> find_frame_missing(pandas.DataFrame({"price": [1.5, None]}))
	array([[False],
	       [ True]])
	"""
	missing_frame = frame.isna()
	missing_grid = missing_frame.to_numpy(dtype=numpy.bool_)

	return missing_grid


def count_axis_missing(missing_grid: NDArray[numpy.bool_], axis: Axis | None) -> tuple[NDArray[numpy.int64], int]:
	"""
	Return the number of missing values along an axis, and how many values each number is counted on.

	.. versionadded:: 0.1.0

	Parameters
	----------
	missing_grid
		True at each missing value of a Table, one row per row.
	axis
		One count per row, per column, or a single count for the whole Table when ``None``.

	Returns
	-------
	tuple[NDArray[numpy.int64], int]
		The counts, then the number of values behind each count.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_counts import count_axis_missing
	>>> count_axis_missing(numpy.array([[True, False], [True, True]]), ndp.Axis.EACH_COLUMN)
	(array([2, 1]), 2)
	"""
	row_count, column_count = missing_grid.shape
	if axis == Axis.EACH_ROW:
		row_counts = missing_grid.sum(axis=ROW_SUM_AXIS, dtype=numpy.int64)
		return row_counts, column_count

	if axis == Axis.EACH_COLUMN:
		column_counts = missing_grid.sum(axis=COLUMN_SUM_AXIS, dtype=numpy.int64)
		return column_counts, row_count

	missing_total = missing_grid.sum(dtype=numpy.int64)
	total_counts = numpy.array([missing_total], dtype=numpy.int64)

	return total_counts, missing_grid.size


def build_name_column(frame: pandas.DataFrame) -> Column:
	"""
	Return a text column holding the names of the columns of a Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	Column
		One name per row, in the order of the Table.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.missing.missing_counts import build_name_column
	>>> build_name_column(pandas.DataFrame({"city": ["Pau"], "price": [1.5]})).tolist()
	['city', 'price']
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	text_dtype = to_numpy_dtype(Type.TEXT)
	name_values = numpy.array(column_names, dtype=text_dtype)
	name_column = build_column(name_values)

	return name_column
