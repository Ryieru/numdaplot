"""
Renaming of the columns of a Table.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.tables.columns.column_names import require_known_columns, require_unique_names
from numdaplot.tables.columns.renaming import Renaming


def rename_frame_columns(frame: pandas.DataFrame, renaming: Renaming) -> pandas.DataFrame:
	"""
	Return the columns of a Table with new names, every change applied at once.

	Two columns can swap their names in a single renaming.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	renaming
		The new names.

	Returns
	-------
	pandas.DataFrame
		The same columns, in the same order, renamed.

	Raises
	------
	ColumnNotFoundError
		When a renamed column does not exist.
	DuplicateColumnError
		When a new name is the name of a column kept as it is.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.renamed_columns import rename_frame_columns
	>>> frame = pandas.DataFrame({"low": [1.0], "high": [9.0]})
	>>> swap = [ndp.NameChange(old_name="low", new_name="high"), ndp.NameChange(old_name="high", new_name="low")]
	>>> rename_frame_columns(frame, ndp.Renaming(changes=swap))
	   high  low
	0   1.0  9.0
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	old_names = [change.old_name for change in renaming.changes]
	require_known_columns(old_names, column_names)
	new_names_by_old_name = {change.old_name: change.new_name for change in renaming.changes}
	final_names = [new_names_by_old_name.get(column_name, column_name) for column_name in column_names]
	require_unique_names(final_names)
	renamed_frame = frame.copy(deep=False)
	renamed_frame.columns = pandas.Index(final_names)

	return renamed_frame
