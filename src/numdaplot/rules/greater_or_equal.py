"""
Rule keeping the values greater than or equal to a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule


class GreaterOrEqual(ValueRule[OrderedValue]):
	"""
	Keep the values greater than or equal to a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, which is kept itself.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 100, 120])
	>>> prices.select(ndp.GreaterOrEqual(100))
	Array([100, 120], dtype=INT64)
	"""
