"""
Groups of rows of a Table sharing the same values in some columns.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

STABLE_SORT = "stable"


def find_row_groups(frame: pandas.DataFrame, group_by: list[str] | None) -> list[NDArray[Any]]:
	"""
	Return the rows of each group, groups sorted by their values, the group of missing values last.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	group_by
		The names of the columns forming the groups, or ``None`` for a single group of every row.

	Returns
	-------
	list[NDArray]
		The positions of the rows of each group, in the order of the Table.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.aggregation.row_groups import find_row_groups
	>>> find_row_groups(pandas.DataFrame({"city": ["Pau", "Lyon", "Pau"]}), ["city"])
	[array([1]), array([0, 2])]
	"""
	row_count = len(frame)
	if group_by is None:
		every_row = numpy.arange(row_count)
		return [every_row]

	# Some versions of the pandas stubs leave the parameter types of groupby unknown.
	grouped_frame = cast(Any, frame)
	grouped_rows = grouped_frame.groupby(group_by, sort=True, dropna=False, observed=True)
	group_count = cast(int, grouped_rows.ngroups)
	if group_count == 0:
		return []

	raw_group_numbers = grouped_rows.ngroup()
	group_number_column = cast("pandas.Series[int]", raw_group_numbers)
	group_numbers = group_number_column.to_numpy()
	every_row = numpy.arange(row_count)
	row_groups = split_positions(every_row, group_numbers, group_count)

	return row_groups


def split_positions(positions: NDArray[Any], group_numbers: NDArray[Any], group_count: int) -> list[NDArray[Any]]:
	"""
	Return the positions of each group, in their order, a group without position being empty.

	.. versionadded:: 0.1.0

	Parameters
	----------
	positions
		The positions of rows.
	group_numbers
		The number of the group of each position, from 0.
	group_count
		The number of groups.

	Returns
	-------
	list[NDArray]
		One array per group, ``group_count`` in all.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.aggregation.row_groups import split_positions
	>>> split_positions(numpy.array([4, 7, 9]), numpy.array([2, 0, 2]), 3)
	[array([7]), array([], dtype=int64), array([4, 9])]
	"""
	order = numpy.argsort(group_numbers, kind=STABLE_SORT)
	sorted_positions = positions[order]
	group_sizes = numpy.bincount(group_numbers, minlength=group_count)
	group_ends = numpy.cumsum(group_sizes)
	group_starts = group_ends[:-1]
	position_groups = numpy.split(sorted_positions, group_starts)

	return position_groups
