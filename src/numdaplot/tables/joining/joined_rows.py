"""
The rows of two Tables that a join puts side by side.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.tables.joining.join_mode import JoinMode

NO_ROW = -1
ROW_DTYPE = numpy.dtype(numpy.intp)
ROWS_AXIS = 1
KEEPS_UNMATCHED_ROWS = frozenset({JoinMode.LEFT, JoinMode.OUTER})
KEEPS_UNMATCHED_OTHER_ROWS = frozenset({JoinMode.RIGHT, JoinMode.OUTER})
INNER_MERGE = "inner"
STABLE_SORT = "stable"


def pair_rows(
	key_frame: pandas.DataFrame, other_key_frame: pandas.DataFrame, mode: JoinMode
) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
	"""
	Return the row numbers of both Tables that each row of a join puts side by side.

	The rows of the joined Table come first, in their order, each with its matches in the order of the other Table,
	then the unmatched rows of the other Table, in their order. A row with a missing key never matches.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of the joined Table.
	other_key_frame
		The key columns of the other Table, of the same names and types.
	mode
		Which rows are kept.

	Returns
	-------
	tuple[NDArray[numpy.intp], NDArray[numpy.intp]]
		The row number of each Table for each row of the result, -1 where a Table has no row.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.joining.joined_rows import pair_rows
	>>> key_frame = pandas.DataFrame({"id": [1, 2, None]})
	>>> other_key_frame = pandas.DataFrame({"id": [3, 1]})
	>>> pair_rows(key_frame, other_key_frame, ndp.JoinMode.OUTER)
	(array([ 0,  1,  2, -1]), array([ 1, -1, -1,  0]))
	"""
	rows, other_rows = match_rows(key_frame, other_key_frame)
	if mode in KEEPS_UNMATCHED_ROWS:
		row_count = len(key_frame)
		rows, other_rows = add_unmatched_rows(rows, other_rows, row_count)

	if mode in KEEPS_UNMATCHED_OTHER_ROWS:
		other_row_count = len(other_key_frame)
		other_rows, rows = add_unmatched_other_rows(other_rows, rows, other_row_count)

	return rows, other_rows


def match_rows(
	key_frame: pandas.DataFrame, other_key_frame: pandas.DataFrame
) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
	"""
	Return the pairs of rows whose keys are all present and equal, sorted by row of the joined Table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of the joined Table.
	other_key_frame
		The key columns of the other Table, of the same names and types.

	Returns
	-------
	tuple[NDArray[numpy.intp], NDArray[numpy.intp]]
		The row number in each Table of each pair.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.joining.joined_rows import match_rows
	>>> match_rows(pandas.DataFrame({"id": [1, 1, None]}), pandas.DataFrame({"id": [1, None]}))
	(array([0, 1]), array([0, 0]))
	"""
	key_count = len(key_frame.columns)
	key_labels = list(range(key_count))
	row_label = key_count
	other_row_label = key_count + 1
	numbered_keys = number_present_rows(key_frame, row_label)
	other_numbered_keys = number_present_rows(other_key_frame, other_row_label)
	merged_rows = numbered_keys.merge(other_numbered_keys, how=INNER_MERGE, on=key_labels)
	row_column = merged_rows[row_label]
	other_row_column = merged_rows[other_row_label]
	merged_row_numbers = row_column.to_numpy(dtype=ROW_DTYPE)
	merged_other_row_numbers = other_row_column.to_numpy(dtype=ROW_DTYPE)
	# numpy.lexsort sorts by the last array first.
	pair_order = numpy.lexsort((merged_other_row_numbers, merged_row_numbers))
	rows = merged_row_numbers[pair_order]
	other_rows = merged_other_row_numbers[pair_order]

	return rows, other_rows


def number_present_rows(key_frame: pandas.DataFrame, row_label: int) -> pandas.DataFrame:
	"""
	Return the rows whose keys are all present, with their row numbers after the keys.

	The keys are labeled by their position, so that no key name can meet the label of the row numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	key_frame
		The key columns of a Table.
	row_label
		The label of the row numbers, after the labels of the keys.

	Returns
	-------
	pandas.DataFrame
		The keys labeled 0, 1... and the row numbers labeled ``row_label``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.joining.joined_rows import number_present_rows
	>>> number_present_rows(pandas.DataFrame({"id": [1, None, 3]}), 1)[1].tolist()
	[0, 2]
	"""
	key_count = len(key_frame.columns)
	row_count = len(key_frame)
	missing_keys = key_frame.isna()
	has_missing_key = missing_keys.any(axis=ROWS_AXIS)
	missing_rows = has_missing_key.to_numpy()
	present_rows = ~missing_rows
	row_numbers = numpy.arange(row_count, dtype=ROW_DTYPE)
	numbered_frame = key_frame.copy()
	numbered_frame.columns = pandas.RangeIndex(key_count)
	numbered_frame[row_label] = row_numbers
	present_frame = numbered_frame[present_rows]

	return present_frame


def add_unmatched_rows(
	rows: NDArray[numpy.intp], other_rows: NDArray[numpy.intp], row_count: int
) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
	"""
	Return the pairs of rows with each unmatched row of the joined Table placed at its row, without other row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rows
		The rows of the joined Table of each pair, sorted.
	other_rows
		The rows of the other Table of each pair.
	row_count
		The number of rows of the joined Table.

	Returns
	-------
	tuple[NDArray[numpy.intp], NDArray[numpy.intp]]
		Every row of the joined Table in its order, -1 as other row where it has no match.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.joining.joined_rows import add_unmatched_rows
	>>> add_unmatched_rows(numpy.array([1, 1]), numpy.array([0, 2]), 3)
	(array([0, 1, 1, 2]), array([-1,  0,  2, -1]))
	"""
	all_rows = numpy.arange(row_count, dtype=ROW_DTYPE)
	unmatched_rows = numpy.setdiff1d(all_rows, rows)
	unmatched_count = len(unmatched_rows)
	no_other_rows = numpy.full(unmatched_count, NO_ROW, dtype=ROW_DTYPE)
	joined_rows = numpy.concatenate([rows, unmatched_rows])
	joined_other_rows = numpy.concatenate([other_rows, no_other_rows])
	row_order = numpy.argsort(joined_rows, kind=STABLE_SORT)
	ordered_rows = joined_rows[row_order]
	ordered_other_rows = joined_other_rows[row_order]

	return ordered_rows, ordered_other_rows


def add_unmatched_other_rows(
	other_rows: NDArray[numpy.intp], rows: NDArray[numpy.intp], other_row_count: int
) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
	"""
	Return the pairs of rows followed by the unmatched rows of the other Table, in their order, without row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	other_rows
		The rows of the other Table of each pair.
	rows
		The rows of the joined Table of each pair.
	other_row_count
		The number of rows of the other Table.

	Returns
	-------
	tuple[NDArray[numpy.intp], NDArray[numpy.intp]]
		The rows of the other Table, then the rows of the joined Table, -1 for each unmatched row added.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.joining.joined_rows import add_unmatched_other_rows
	>>> add_unmatched_other_rows(numpy.array([1]), numpy.array([0]), 3)
	(array([1, 0, 2]), array([ 0, -1, -1]))
	"""
	all_other_rows = numpy.arange(other_row_count, dtype=ROW_DTYPE)
	unmatched_other_rows = numpy.setdiff1d(all_other_rows, other_rows)
	unmatched_count = len(unmatched_other_rows)
	no_rows = numpy.full(unmatched_count, NO_ROW, dtype=ROW_DTYPE)
	joined_other_rows = numpy.concatenate([other_rows, unmatched_other_rows])
	joined_rows = numpy.concatenate([rows, no_rows])

	return joined_other_rows, joined_rows
