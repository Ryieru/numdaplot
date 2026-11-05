"""
Rule keeping the values less than or equal to a reference value.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule


@dataclass(frozen=True)
class LessOrEqual(ValueRule[OrderedValue]):
	"""
	Keep the values less than or equal to a reference value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value, an ``OrderedValue`` such as ``10``, ``"M"`` or ``date(2026, 1, 31)``, which is kept itself.

	Raises
	------
	InvalidTypeError
		When ``value`` is not a single value, such as an Array or a list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 100, 120])
	>>> prices.select(ndp.LessOrEqual(100))
	Array([ 80, 100], dtype=INT64)
	"""

	value: OrderedValue
