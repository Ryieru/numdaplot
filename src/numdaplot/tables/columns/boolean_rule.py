"""
How a Conversion reads numbers as booleans.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class BooleanRule(Enum):
	"""
	How a ``Conversion`` of a number column to ``BOOL`` reads each number.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> visits = ndp.Table.from_arrays({"visits": ndp.Array.from_list([0, 3])})
	>>> rule = ndp.BooleanRule.NONZERO_TRUE
	>>> visits.convert(ndp.Conversion(column="visits", dtype=ndp.Type.BOOL, booleans=rule))
	  visits
	    BOOL
	0  False
	1   True
	"""

	ZERO_ONE = auto()
	"""
	0 gives ``False`` and 1 gives ``True``; any other number raises ``ValueConversionError``. Used when ``booleans``
	is omitted.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> severe = ndp.Table.from_arrays({"severe": ndp.Array.from_list([1, 0])})
	>>> severe.convert(ndp.Conversion(column="severe", dtype=ndp.Type.BOOL, booleans=ndp.BooleanRule.ZERO_ONE))
	  severe
	    BOOL
	0   True
	1  False
	"""

	NONZERO_TRUE = auto()
	"""
	0 gives ``False`` and any other number gives ``True``, as in Python.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> visits = ndp.Table.from_arrays({"visits": ndp.Array.from_list([0, 3, -1])})
	>>> rule = ndp.BooleanRule.NONZERO_TRUE
	>>> visits.convert(ndp.Conversion(column="visits", dtype=ndp.Type.BOOL, booleans=rule))
	  visits
	    BOOL
	0  False
	1   True
	2   True
	"""
