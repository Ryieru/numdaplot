"""
Removal of the rows or the columns of a Table holding missing values.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.positions.axis import Axis
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.missing.missing_counts import (
	COLUMN_SUM_AXIS,
	ROW_SUM_AXIS,
	divide_counts,
	find_frame_missing,
)
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio
from numdaplot.tables.missing.ratio_comparison import RatioComparison


def drop_frame_missing(frame: pandas.DataFrame, missing_drop: MissingDrop) -> pandas.DataFrame:
	"""
	Return a Table without its rows or its columns holding too many missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	missing_drop
		The axis, the columns looked at and the rule deciding what is removed.

	Returns
	-------
	pandas.DataFrame
		The remaining rows, in their order and numbered from 0, or the remaining columns, in their order.

	Raises
	------
	ColumnNotFoundError
		When a looked at column does not exist.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_removal import drop_frame_missing
	>>> frame = pandas.DataFrame({"price": [1.5, None, 3.0]})
	>>> drop_frame_missing(frame, ndp.MissingDrop())
	   price
	0    1.5
	1    3.0
	"""
	looked_names = [str(column_name) for column_name in frame.columns]
	if missing_drop.columns is not None:
		require_known_columns(missing_drop.columns, looked_names)
		looked_names = missing_drop.columns

	looked_frame = frame[looked_names]
	if missing_drop.axis == Axis.EACH_COLUMN:
		remaining_columns = drop_missing_columns(frame, looked_frame, missing_drop.rule)
		return remaining_columns

	remaining_rows = drop_missing_rows(frame, looked_frame, missing_drop.rule)

	return remaining_rows


def drop_missing_rows(
	frame: pandas.DataFrame,
	looked_frame: pandas.DataFrame,
	rule: MissingMode | MissingRatio,
) -> pandas.DataFrame:
	"""
	Return a Table without the rows holding too many missing values in some of its columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	looked_frame
		The columns whose missing values are counted on each row.
	rule
		How many missing values make a row removed.

	Returns
	-------
	pandas.DataFrame
		The remaining rows, in their order, numbered from 0.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_removal import drop_missing_rows
	>>> frame = pandas.DataFrame({"price": [1.5, None], "stock": [None, None]}, dtype="float64")
	>>> drop_missing_rows(frame, frame, ndp.MissingMode.ALL)
	   price  stock
	0    1.5    NaN
	"""
	missing_grid = find_frame_missing(looked_frame)
	row_counts = missing_grid.sum(axis=ROW_SUM_AXIS, dtype=numpy.int64)
	looked_column_count = len(looked_frame.columns)
	dropped = find_dropped(row_counts, looked_column_count, rule)
	kept = ~dropped
	kept_frame = frame[kept]
	numbered_frame = kept_frame.reset_index(drop=True)

	return numbered_frame


def drop_missing_columns(
	frame: pandas.DataFrame,
	looked_frame: pandas.DataFrame,
	rule: MissingMode | MissingRatio,
) -> pandas.DataFrame:
	"""
	Return a Table without the columns holding too many missing values, among some of its columns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	looked_frame
		The columns that may be removed.
	rule
		How many missing values make a column removed.

	Returns
	-------
	pandas.DataFrame
		The remaining columns, in their order.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_removal import drop_missing_columns
	>>> frame = pandas.DataFrame({"price": [1.5, None], "stock": [None, None]}, dtype="float64")
	>>> drop_missing_columns(frame, frame, ndp.MissingMode.ALL)
	   price
	0    1.5
	1    NaN
	"""
	missing_grid = find_frame_missing(looked_frame)
	column_counts = missing_grid.sum(axis=COLUMN_SUM_AXIS, dtype=numpy.int64)
	row_count = len(looked_frame)
	dropped = find_dropped(column_counts, row_count, rule)
	looked_names = [str(column_name) for column_name in looked_frame.columns]
	dropped_names = [name for name, is_dropped in zip(looked_names, dropped, strict=True) if is_dropped]
	remaining_frame = frame.drop(columns=dropped_names)

	return remaining_frame


def find_dropped(
	counts: NDArray[numpy.int64],
	value_count: int,
	rule: MissingMode | MissingRatio,
) -> NDArray[numpy.bool_]:
	"""
	Return which rows or columns hold too many missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	counts
		The number of missing values of each row or column.
	value_count
		The number of values of each row or column.
	rule
		How many missing values make a row or a column removed.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each row or column to remove, never True when there is no value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_removal import find_dropped
	>>> find_dropped(numpy.array([0, 1, 2]), 2, ndp.MissingMode.ALL)
	array([False, False,  True])
	>>> find_dropped(numpy.array([0, 1, 2]), 2, ndp.MissingRatio(ratio=0.5, comparison=ndp.RatioComparison.ABOVE))
	array([False, False,  True])
	"""
	if value_count == 0:
		nothing_dropped = numpy.zeros(counts.shape, dtype=numpy.bool_)
		return nothing_dropped

	if isinstance(rule, MissingRatio):
		ratio_dropped = find_ratio_dropped(counts, value_count, rule)
		return ratio_dropped

	if rule == MissingMode.ALL:
		all_missing = counts == value_count
		return all_missing

	any_missing = counts > 0

	return any_missing


def find_ratio_dropped(
	counts: NDArray[numpy.int64],
	value_count: int,
	missing_ratio: MissingRatio,
) -> NDArray[numpy.bool_]:
	"""
	Return which rows or columns reach a ratio of missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	counts
		The number of missing values of each row or column.
	value_count
		The number of values of each row or column, at least 1.
	missing_ratio
		The threshold and how a ratio is compared with it.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each row or column whose ratio reaches the threshold.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.missing.missing_removal import find_ratio_dropped
	>>> find_ratio_dropped(numpy.array([0, 1, 2]), 2, ndp.MissingRatio(ratio=0.5))
	array([False,  True,  True])
	"""
	ratios = divide_counts(counts, value_count)
	if missing_ratio.comparison == RatioComparison.ABOVE:
		above_ratio = ratios > missing_ratio.ratio
		return above_ratio

	at_least_ratio = ratios >= missing_ratio.ratio

	return at_least_ratio
