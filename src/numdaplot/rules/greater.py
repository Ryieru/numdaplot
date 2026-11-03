"""
Rule keeping the values strictly greater than a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule


class Greater(ValueRule[OrderedValue]):
	"""
	Keep the values strictly greater than a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, which is not kept itself.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Greater(100)
	Greater(value=100)
	"""
