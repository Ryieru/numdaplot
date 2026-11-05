"""
Rule keeping the values equal to a reference value.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule_values import ScalarValue
from numdaplot.rules.value_rule import ValueRule


@dataclass(frozen=True)
class Equal(ValueRule[ScalarValue]):
	"""
	Keep the values equal to a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, a ``ScalarValue`` such as ``"Paris"``, ``10`` or ``True``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> countries = ndp.Array.from_list(["FR", "DE", "FR"])
	>>> countries.check(ndp.Equal("FR"))
	Array([ True, False,  True], dtype=BOOL)
	"""

	value: ScalarValue
