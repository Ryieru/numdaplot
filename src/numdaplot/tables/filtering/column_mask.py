"""
Rows of a Table column satisfying a rule.

.. versionadded:: 0.1.0
"""

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.selection.rule_mask import build_rule_mask
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.rule import Rule
from numdaplot.tables.filtering.rule_moments import match_rule_time_zone
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, read_present_values
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
from numdaplot.tables.frames.time_zones import find_column_time_zone


def build_column_mask(column: Column, rule: Rule) -> NDArray[numpy.bool_]:
	"""
	Return which values of a Table column satisfy a rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	rule
		Any rule of numdaplot. A missing value only satisfies ``IsMissing``.

	Returns
	-------
	NDArray[numpy.bool_]
		True at each row whose value satisfies the rule.

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
	>>> from numdaplot.tables.filtering.column_mask import build_column_mask
	>>> build_column_mask(pandas.Series([5, None, 12], dtype="Int64"), ndp.Greater(10))
	array([False, False,  True])
	"""
	missing = find_column_missing(column)
	if isinstance(rule, IsMissing):
		return missing

	present = ~missing
	if isinstance(rule, IsPresent):
		return present

	time_zone = find_column_time_zone(column)
	matched_rule = match_rule_time_zone(rule, time_zone)
	present_values = read_present_values(column)
	with NamedColumnErrors(column):
		present_mask = build_rule_mask(present_values, matched_rule)

	mask = numpy.zeros(missing.shape, dtype=numpy.bool_)
	mask[present] = present_mask

	return mask
