"""
Removal of the duplicated rows of a Table.

.. versionadded:: 0.1.0
"""

from typing import Literal

import pandas

from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.duplicates.keep import Keep

KEPT_ROWS = dict[Keep, Literal["first", "last", False]](
	{
		Keep.FIRST: "first",
		Keep.LAST: "last",
		Keep.NONE: False,
	}
)


def drop_duplicate_rows(frame: pandas.DataFrame, deduplication: Deduplication) -> pandas.DataFrame:
	"""
	Return the rows of a Table without its duplicated rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	deduplication
		The compared columns and the row kept in each group of duplicates.

	Returns
	-------
	pandas.DataFrame
		The remaining rows, in their order, numbered from 0.

	Raises
	------
	ColumnNotFoundError
		When a compared column does not exist.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.duplicates.deduplicated_frame import drop_duplicate_rows
	>>> frame = pandas.DataFrame({"email": ["a@x.fr", "b@x.fr", "a@x.fr"], "visit": [1, 2, 3]})
	>>> drop_duplicate_rows(frame, ndp.Deduplication(columns=["email"], keep=ndp.Keep.LAST))
	    email  visit
	0  b@x.fr      2
	1  a@x.fr      3
	"""
	if deduplication.columns is not None:
		column_names = [str(column_name) for column_name in frame.columns]
		require_known_columns(deduplication.columns, column_names)

	kept_rows = KEPT_ROWS[deduplication.keep]
	remaining_frame = frame.drop_duplicates(subset=deduplication.columns, keep=kept_rows)
	numbered_frame = remaining_frame.reset_index(drop=True)

	return numbered_frame
