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
	>>> ndp.GreaterOrEqual(100)
	GreaterOrEqual(value=100)
	"""
