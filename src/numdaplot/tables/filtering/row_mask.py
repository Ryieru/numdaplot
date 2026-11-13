"""
Rows of a Table satisfying a Filter.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.tables.filtering.column_mask import build_column_mask
from numdaplot.tables.filtering.column_match import ColumnMatch
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.filtering.filter_mode import FilterMode

MASK_AXIS = 0


def build_filter_mask(frame: pandas.DataFrame, row_filter: Filter) -> NDArray[numpy.bool_]:
	"""
	Return which rows of a Table satisfy a Filter.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	row_filter
		The conditions and how they combine.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each row to keep.

	Raises
	------
	ColumnNotFoundError
		When a condition names a column the Table does not have.
	IncompatibleTypesError
		When a rule does not apply to the type of one of its columns.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.row_mask import build_filter_mask
	>>> frame = pandas.DataFrame({"price": [5.0, 12.0]})
	>>> build_filter_mask(frame, ndp.Filter(conditions=[ndp.Condition(rule=ndp.Greater(10))]))
	array([False,  True])
	"""
	condition_masks = [build_condition_mask(frame, condition) for condition in row_filter.conditions]
	requires_all = row_filter.mode == FilterMode.ALL
	row_count = len(frame)
	filter_mask = combine_masks(condition_masks, requires_all, row_count)

	return filter_mask


def build_condition_mask(frame: pandas.DataFrame, condition: Condition) -> NDArray[numpy.bool_]:
	"""
	Return which rows of a Table satisfy a Condition.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	condition
		The rule, its columns, and how the columns combine.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each row satisfying the condition.

	Raises
	------
	ColumnNotFoundError
		When the condition names a column the Table does not have.
	IncompatibleTypesError
		When the rule does not apply to the type of one of the columns.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.row_mask import build_condition_mask
	>>> frame = pandas.DataFrame({"low": [1.0, 5.0], "high": [2.0, 9.0]})
	>>> build_condition_mask(frame, ndp.Condition(rule=ndp.Greater(1.5), mode=ndp.ColumnMatch.ALL))
	array([False,  True])
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	if condition.columns is not None:
		require_known_columns(condition.columns, column_names)
		column_names = condition.columns

	column_masks = list[NDArray[numpy.bool_]]()

	for column_name in column_names:
		column = frame[column_name]
		column_mask = build_column_mask(column, condition.rule)
		column_masks.append(column_mask)

	requires_all = condition.mode == ColumnMatch.ALL
	row_count = len(frame)
	condition_mask = combine_masks(column_masks, requires_all, row_count)

	return condition_mask


def combine_masks(masks: list[NDArray[numpy.bool_]], requires_all: bool, row_count: int) -> NDArray[numpy.bool_]:
	"""
	Return the rows satisfying every mask, or at least one mask.

	.. versionadded:: 0.1.0

	Parameters
	----------
	masks
		One mask per condition or per column, each as long as the Table.
	requires_all
		True to keep the rows satisfying every mask, False for at least one.
	row_count
		The number of rows of the Table, used when there is no mask.

	Returns
	-------
	NDArray[numpy.bool_]
		The combined mask. Without any mask, every row satisfies "every mask" and none satisfies "at least one".

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.filtering.row_mask import combine_masks
	>>> combine_masks([numpy.array([True, False]), numpy.array([True, True])], True, 2)
	array([ True, False])
	"""
	mask_count = len(masks)
	stacked_masks = numpy.array(masks, dtype=numpy.bool_)
	mask_grid = stacked_masks.reshape(mask_count, row_count)
	if requires_all:
		every_mask = numpy.logical_and.reduce(mask_grid, axis=MASK_AXIS)
		return every_mask

	any_mask = numpy.logical_or.reduce(mask_grid, axis=MASK_AXIS)

	return any_mask
