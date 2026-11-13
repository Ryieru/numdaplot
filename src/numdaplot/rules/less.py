"""
Rule keeping the values strictly less than a reference value.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numdaplot.rules.rule_values import OrderedValue
from numdaplot.rules.value_rule import ValueRule

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array


@dataclass(frozen=True)
class Less(ValueRule["OrderedValue | Array"]):
	"""
	Keep the values strictly less than a reference value.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an Array, each value being compared with the value at its position.

	Parameters
	----------
	value
		The reference value, an ``OrderedValue`` such as ``10``, ``"M"`` or ``date(2026, 1, 31)``, which is not kept
		itself. Or an Array of the same shape as the tested values, one value per row for a Table column: each value is
		then compared with the value at its position, and a missing value of the Array matches nothing.

	Raises
	------
	InvalidTypeError
		When ``value`` is neither a single value nor an Array, such as a list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([80, 100, 120])
	>>> prices.select(ndp.Less(100))
	Array([80], dtype=INT64)
	"""

	value: OrderedValue | Array
