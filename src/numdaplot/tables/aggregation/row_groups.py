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
	rows_by_group = numpy.argsort(group_numbers, kind=STABLE_SORT)
	group_sizes = numpy.bincount(group_numbers, minlength=group_count)
	group_ends = numpy.cumsum(group_sizes)
	group_starts = group_ends[:-1]
	row_groups = numpy.split(rows_by_group, group_starts)

	return row_groups
