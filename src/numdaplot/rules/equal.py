"""
Rule keeping the values equal to a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import ScalarValue
from numdaplot.rules.value_rule import ValueRule


class Equal(ValueRule[ScalarValue]):
	"""
	Keep the values equal to a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Equal("FR")
	Equal(value='FR')
	"""
