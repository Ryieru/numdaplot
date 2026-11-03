"""
Renaming of the columns of a Table.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.tables.columns.column_names import require_known_columns, require_unique_names
from numdaplot.tables.columns.renaming import Renaming

RENAMING_ITEM_NAME = "renaming"


def rename_frame_columns(frame: pandas.DataFrame, renamings: list[Renaming]) -> pandas.DataFrame:
	"""
	Return the columns of a Table with new names, all renamings applied at once.

	Two columns can swap their names in a single call.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	renamings
		The new names, at least one.

	Returns
	-------
	pandas.DataFrame
		The same columns, in the same order, renamed.

	Raises
	------
	EmptyListError
		When ``renamings`` is empty.
	DuplicateColumnError
		When a column is renamed twice, or two columns would end with the same name.
	ColumnNotFoundError
		When a renamed column does not exist.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.renamed_columns import rename_frame_columns
	>>> frame = pandas.DataFrame({"low": [1.0], "high": [9.0]})
	>>> swap = [ndp.Renaming(old_name="low", new_name="high"), ndp.Renaming(old_name="high", new_name="low")]
	>>> rename_frame_columns(frame, swap)
	high  low
	0   1.0  9.0
	"""
	if renamings == []:
		raise EmptyListError(RENAMING_ITEM_NAME)

	column_names = [str(column_name) for column_name in frame.columns]
	old_names = [renaming.old_name for renaming in renamings]
	require_unique_names(old_names)
	require_known_columns(old_names, column_names)
	new_names_by_old_name = {renaming.old_name: renaming.new_name for renaming in renamings}
	final_names = [new_names_by_old_name.get(column_name, column_name) for column_name in column_names]
	require_unique_names(final_names)
	renamed_frame = frame.copy(deep=False)
	renamed_frame.columns = pandas.Index(final_names)

	return renamed_frame
