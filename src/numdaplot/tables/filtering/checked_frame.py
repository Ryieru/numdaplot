"""
Values of a Table satisfying a rule.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import build_column
from numdaplot.rules.rule import Rule
from numdaplot.tables.filtering.column_mask import build_column_mask


def check_frame(frame: pandas.DataFrame, rule: Rule) -> pandas.DataFrame:
	"""
	Return which values of every column of a Table satisfy a rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	rule
		Any rule of numdaplot. A missing value only satisfies ``IsMissing``.

	Returns
	-------
	pandas.DataFrame
		The same column names and rows, each value replaced by True or False.

	Raises
	------
	IncompatibleTypesError
		When the rule does not apply to the type of one of the columns.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.checked_frame import check_frame
	>>> check_frame(pandas.DataFrame({"price": [1.5, None]}), ndp.IsMissing())
	   price
	0  False
	1   True
	"""
	checked_columns = dict[str, Column]()

	for column_name in frame.columns:
		column = frame[column_name]
		column_mask = build_column_mask(column, rule)
		checked_name = str(column_name)
		checked_columns[checked_name] = build_column(column_mask)

	row_count = len(frame)
	row_numbers = pandas.RangeIndex(row_count)
	checked = pandas.DataFrame(checked_columns, index=row_numbers)

	return checked
