"""
Base class of the rules that compare each value to a single reference value.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule import Rule


@dataclass(frozen=True)
class ValueRule[ReferenceValue](Rule):
	"""
	Base class of the rules that compare each value to a single reference value.

	Two rules are equal only when they have the same class and the same reference value,
	so ``Greater(1)`` and ``Less(1)`` are different.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The reference value each tested value is compared to.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> limit = ndp.Greater(100)
	>>> limit.value
	100
	>>> ndp.Array.from_list([80, 120]).select(limit)
	Array([120], dtype=INT64)
	"""

	value: ReferenceValue
