"""
Rule keeping the values different from a reference value.

.. versionadded:: 0.1.0
"""

from numdaplot.rules.rule_values import ScalarValue
from numdaplot.rules.value_rule import ValueRule


class NotEqual(ValueRule[ScalarValue]):
	"""
	Keep the values different from a reference value.

	Missing values are not kept: use ``IsMissing`` to test them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> countries = ndp.Array.from_list(["FR", "DE", "FR"])
	>>> countries.select(ndp.NotEqual("FR"))
	Array(['DE'], dtype=TEXT)
	"""
