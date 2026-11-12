"""
How the columns of a Condition combine.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class ColumnMatch(Enum):
	"""
	How the columns of a ``Condition`` combine to satisfy it.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> low = ndp.Array.from_list([1.0, 5.0, 20.0])
	>>> high = ndp.Array.from_list([2.0, 30.0, 40.0])
	>>> ranges = ndp.Table.from_arrays({"low": low, "high": high})
	>>> above_ten = ndp.Condition(rule=ndp.Greater(10), mode=ndp.ColumnMatch.ALL)
	>>> ranges.filter(ndp.Filter(conditions=[above_ten]))
	      low    high
	  FLOAT64 FLOAT64
	0    20.0    40.0
	"""

	ANY = auto()
	"""
	A row satisfies the condition when at least one of the columns satisfies the rule. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> low = ndp.Array.from_list([1.0, 5.0, 20.0])
	>>> high = ndp.Array.from_list([2.0, 30.0, 40.0])
	>>> ranges = ndp.Table.from_arrays({"low": low, "high": high})
	>>> above_ten = ndp.Condition(rule=ndp.Greater(10), mode=ndp.ColumnMatch.ANY)
	>>> ranges.filter(ndp.Filter(conditions=[above_ten]))
	      low    high
	  FLOAT64 FLOAT64
	0     5.0    30.0
	1    20.0    40.0
	"""

	ALL = auto()
	"""
	A row satisfies the condition when every column satisfies the rule.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> low = ndp.Array.from_list([1.0, 5.0, 20.0])
	>>> high = ndp.Array.from_list([2.0, 30.0, 40.0])
	>>> ranges = ndp.Table.from_arrays({"low": low, "high": high})
	>>> above_ten = ndp.Condition(rule=ndp.Greater(10), mode=ndp.ColumnMatch.ALL)
	>>> ranges.filter(ndp.Filter(conditions=[above_ten]))
	      low    high
	  FLOAT64 FLOAT64
	0    20.0    40.0
	"""
