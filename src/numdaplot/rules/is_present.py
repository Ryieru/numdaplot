"""
Rule keeping the values that are not missing.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.rules.rule import Rule


@dataclass(frozen=True)
class IsPresent(Rule):
	"""
	Keep the values that are not missing. It is the opposite of ``IsMissing``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> temperatures = ndp.Array.from_list([12.5, None, 18.0])
	>>> temperatures.select(ndp.IsPresent())
	Array([12.5, 18. ], dtype=FLOAT64)
	"""
