"""
Rule keeping the values different from a reference value.

.. versionadded:: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from numdaplot.rules.rule_values import ScalarValue
from numdaplot.rules.value_rule import ValueRule

if TYPE_CHECKING:
	from numdaplot.arrays.array import Array


@dataclass(frozen=True)
class NotEqual(ValueRule["ScalarValue | Array"]):
	"""
	Keep the values different from a reference value.

	Missing values are not kept: use ``IsMissing`` to test them.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Accepts an Array, each value being compared with the value at its position.

	Parameters
	----------
	value
		The reference value, a ``ScalarValue`` such as ``"Paris"``, ``10`` or ``True``. Or an Array of the same shape as
		the tested values, one value per row for a Table column: each value is then compared with the value at its
		position, and a missing value of the Array matches nothing.

	Raises
	------
	RefusedOperationError
		When ``value`` is None: ``IsPresent`` tests the missing values.
	InvalidTypeError
		When ``value`` is neither a single value nor an Array, such as a list.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> countries = ndp.Array.from_list(["FR", "DE", "FR"])
	>>> countries.select(ndp.NotEqual("FR"))
	Array(['DE'], dtype=TEXT)
	"""

	MISSING_VALUE_RULE: ClassVar[str | None] = "IsPresent"

	value: ScalarValue | Array
