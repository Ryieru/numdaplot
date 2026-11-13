"""
Replacement of columns of a Table by a change made to each of them.

.. versionadded:: 0.2.0
"""

from collections.abc import Callable

import pandas

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.column_storage.column import Column
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors


def replace_frame_columns(
	frame: pandas.DataFrame,
	column_names: list[str],
	column_change: Callable[[Column], Column],
) -> pandas.DataFrame:
	"""
	Return the columns of a Table with some of them replaced by a change, each at its place.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	column_names
		The names of the columns to change, in the order the change is made.
	column_change
		Returns the new column from a column, numbered from 0.

	Returns
	-------
	pandas.DataFrame
		A new DataFrame, the other columns unchanged.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist, before any column is changed.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.columns.replaced_columns import replace_frame_columns
	>>> frame = pandas.DataFrame({"price": [1.5, 8.0], "city": ["Pau", "Dax"]})
	>>> replace_frame_columns(frame, ["price"], lambda column: column * 2)
	   price city
	0    3.0  Pau
	1   16.0  Dax
	"""
	frame_column_names = [str(column_name) for column_name in frame.columns]
	require_known_columns(column_names, frame_column_names)
	changed_frame = frame.copy(deep=False)

	for column_name in column_names:
		column = frame[column_name]
		with NamedColumnErrors(column):
			changed_column = column_change(column)

		changed_frame[column_name] = changed_column

	return changed_frame
