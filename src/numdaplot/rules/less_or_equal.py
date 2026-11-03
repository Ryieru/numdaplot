"""
Rule keeping the values less than or equal to a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule


class LessOrEqual(ValueRule[OrderedValue]):
	"""
	Keep the values less than or equal to a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, which is kept itself.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 100, 120])
	>>> prices.select(ndp.LessOrEqual(100))
	Array([ 80, 100], dtype=INT64)
	"""
