"""
Choice of the columns of a Table.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.tables.columns.column_choice import ColumnChoice
from numdaplot.tables.columns.column_mode import ColumnMode
from numdaplot.tables.columns.column_names import require_known_columns


def choose_frame_columns(frame: pandas.DataFrame, choice: ColumnChoice) -> pandas.DataFrame:
	"""
	Return the columns of a Table that a choice keeps.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	choice
		The columns, and whether to keep or drop them.

	Returns
	-------
	pandas.DataFrame
		With ``KEEP``, the named columns in the order of the list; with ``DROP``, the other columns in their order.

	Raises
	------
	ColumnNotFoundError
		When a named column does not exist.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.chosen_columns import choose_frame_columns
	>>> frame = pandas.DataFrame({"city": ["Pau"], "price": [1.5]})
	>>> choose_frame_columns(frame, ndp.ColumnChoice(columns=["price", "city"]))
	price city
	0    1.5  Pau
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	require_known_columns(choice.columns, column_names)
	if choice.mode == ColumnMode.DROP:
		remaining_frame = frame.drop(columns=choice.columns)
		return remaining_frame

	kept_frame = frame.loc[:, choice.columns]

	return kept_frame
