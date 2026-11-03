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
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, read_present_values


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

	present_values = read_present_values(column)
	present_mask = build_rule_mask(present_values, rule)
	mask = numpy.zeros(missing.shape, dtype=numpy.bool_)
	mask[present] = present_mask

	return mask
