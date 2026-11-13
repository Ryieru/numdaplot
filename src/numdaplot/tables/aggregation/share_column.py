"""
Column whose mean is the share of the values of a Table column satisfying a rule.

.. versionadded:: 0.2.0
"""

import numpy

from numdaplot.arrays.statistics.share_values import mark_share_values
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import build_column_with_missing, find_column_missing
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.share import Share
from numdaplot.tables.filtering.column_mask import build_column_mask

# A share is the mean of the column built by build_share_column.
SHARE_MEAN = Mean()


def build_share_column(column: Column, share: Share) -> Column:
	"""
	Return 1 where a value satisfies the rule of a share, 0 where it does not, missing where it is not counted.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A Table column.
	share
		The rule, and whether missing values are counted.

	Returns
	-------
	Column
		A decimal column of the same length, whose mean is the share.

	Raises
	------
	IncompatibleTypesError
		When the rule does not apply to the type of the column.
	TimeZoneMismatchError
		When a datetime of the rule has a time zone and the column has none, or the reverse.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.share_column import build_share_column
	>>> build_share_column(pandas.Series([70, None, 30], dtype="Int64"), ndp.Share(rule=ndp.Greater(65))).tolist()
	[1.0, nan, 0.0]
	"""
	matches = build_column_mask(column, share.rule)
	missing = find_column_missing(column)
	share_values = mark_share_values(matches, missing, share.missing)
	uncounted = numpy.isnan(share_values)
	counted = ~uncounted
	counted_values = share_values[counted]
	share_column = build_column_with_missing(counted_values, uncounted)

	return share_column
