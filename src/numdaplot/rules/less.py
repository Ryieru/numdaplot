"""
Rule keeping the values strictly less than a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule


class Less(ValueRule[OrderedValue]):
	"""
	Keep the values strictly less than a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, which is not kept itself.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 100, 120])
	>>> prices.select(ndp.Less(100))
	Array([80], dtype=INT64)
	"""
